#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  functions.py
#
#  Copyright 2021 Kleydson Stenio <kleydson.stenio@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from numpy import ndarray, array, where, min as mini, hstack, vstack, polyfit, trapz, mean, std, zeros_like, linspace, column_stack, zeros
from scipy.optimize import least_squares
from PySide2.QtCore import Signal
from typing import List, Tuple
from env.equations import *


def isopeaks(wavelength: ndarray, counts: ndarray, elements: List, lower: List, upper: List, center: List, linear: bool, anorm: bool, progress: Signal) -> Tuple[ndarray, ndarray]:
	# Allocate data
	new_wavelength = array([[None] * 3] * len(elements))
	new_counts = array([array([None for X in range(len(counts))]) for Y in range(len(elements))], dtype=object)
	# Cut data for each element in iso table
	for i, e in enumerate(elements):
		cut = where((wavelength >= lower[i]) & (wavelength <= upper[i]))[0]
		x = wavelength[cut]
		for j, c in enumerate(counts):
			y = c[cut, :]
			x_, y_ = hstack((x[:2], x[-2:])), vstack((y[:2], y[-2:]))
			# Corrects data in new isolated matrix
			for k in range(y.shape[1]):
				if linear:
					# Trace a line to correct inclination
					coefficients = polyfit(x_, y_[:, k], 1)
					y[:, k] -= coefficients[1] + coefficients[0] * x
					# If asked, also normalizes by the area
					if anorm:
						y[:, k] /= trapz(coefficients[1] + coefficients[0] * x, x)
				else:
					y_min = mini(y[:, k])
					if y_min > 0:
						y[:, k] -= y_min
					elif y_min < 0:
						y[:, k] += -1 * y_min
					else:
						pass
			# Saves new count
			new_counts[i][j] = y
		# Saves new wavelength
		new_wavelength[i][:] = e, array(([lower[i], upper[i], center[i]]), dtype=object), x
		progress.emit(i)
	return new_wavelength, new_counts

def fit_guess(x: ndarray, y: ndarray, peaks: int, center: List, shape_id: str, asymmetry=None):
	guess = []
	for i in range(peaks):
		# Ratio for values
		r, d = 1 - 0.4*(i/peaks), x[-1] - x[0]
		# Height/Area, Width, Center, Asymmetry
		guess.append(r * max(y)) # Intensity is the highest value
		guess.append(r * d / 4) # Width approximation by 1/4 of interval
		if 'voigt' in shape_id.lower():
			guess[-2] = r * max(y) * d / 2  # Area approximation by triangle
			guess.append(r * d / 4) # Width approximation by 1/4 of interval
		if 'fixed' not in shape_id.lower():
			guess.append(center[i]) # Center (user entered value)
		if ('asymmetric' in shape_id.lower()) or ('asym' in shape_id.lower() and 'center fixed' in shape_id.lower()):
			guess.append(asymmetry)  # Asymmetry (auto or user entered value)
	return guess

def residuals(guess, x, y, shape_id, **kwargs):
	function_kwargs = {'Center': kwargs['Center'], 'Asymmetry': kwargs['Asymmetry']}
	if shape_id == 'Trapezoidal rule':
		return zeros_like(y)
	else:
		return y - kwargs[shape_id](x, *guess, **function_kwargs)

def fit_values(ny, shape, param):
	if 'Voigt' in shape:
		a, wl, wg = param[:3]
		w = 0.5346*wl + (0.2166*(wl**2) + wg**2)**0.5
		h = max(ny)
	else:
		h, w = param[:2]
		if 'Lorentzian' in shape:
			a = (h*w*pi)/2
		elif 'Gaussian' in shape:
			a = (2*h*w)*((pi/2)**0.5)
		else:
			a = 0
	return h, w, a

def fit_results(x, y, optimized, shape, npeaks, sdict):
	solution, residual, nfev, convergence = optimized.x, optimized.fun, optimized.nfev, optimized.success
	individuals_solution = array_split(nabs(solution), npeaks)
	# With optimized, we can have the x-axis
	if shape != 'Trapezoidal rule':
		nx = linspace(x[0], x[-1], 1000)
		# creates the total result
		total = zeros((nx.size, npeaks + 1))
		results = []
		for i, individuals in enumerate(individuals_solution):
			indv_dict = {'Center': [sdict['Center'][i]], 'Asymmetry': sdict['Asymmetry']}
			total[:, i] = sdict[shape](nx, *individuals, **indv_dict)
			results.append(fit_values(total[:, i], shape, individuals))
		total[:, -1] = nsum(total[:, :-1], 1)
	else:
		nx, total = x, column_stack((y, y))
		nfev, convergence = 1, True
		results = array(([max(y), (x[-1]-x[0])/4, trapz(y, x)])) # h, w, a
	return column_stack((x, y, residual)), nx, total, shape, results, nfev, convergence

def fitpeaks(iso_wavelengths: ndarray, iso_counts: ndarray, parameters: List, mean1st: bool, progress: Signal):
	# Creates exit array
	# needs: y, nx, ny
	fit_w_counts = array([[[None] * 7] * len(iso_counts[0])] * len(iso_wavelengths))
	# Goes in element level: same size as iso_wavelengths
	for i, w in enumerate(iso_wavelengths):
		# Extra relevant information:
		#   w[0] = Element
		#   w[1] = lower, upper, center
		#   w[2] = wavelengths (x data)
		#   parameters[i][0] = shape
		#   parameters[i][1] = asymmetry
		#
		# Gets a dict for shapes and fit equations
		shape, asym = parameters[i]
		x, center = w[2], w[1][2]
		scd = equations_translator(center=center, asymmetry=asym)
		# Now goes into sample level: size of each i-th iso_wavelengths
		for j, ci in enumerate(iso_counts[i]):
			# Regarding modes, we have mean 1st or area 1st, which defines how results are exported
			if mean1st:
				# If mean1st is True, take the mean of iso_counts[i][j] and pass it to perform fit
				average_spectrum = mean(ci, axis=1)
				guess = fit_guess(x=x, y=average_spectrum, peaks=len(center), center=center, shape_id=shape, asymmetry=asym)
				optimized = least_squares(residuals, guess,
				                          args=(x, average_spectrum, shape),
				                          kwargs=scd, ftol=1e-7, gtol=1e-7,
				                          xtol=1e-7, max_nfev=1000)
				# Gets the result based on optimized solution
				results = fit_results(x, average_spectrum, optimized, shape, len(center), scd)
				# Finally, saves result
				fit_w_counts[i][j][:] = results # average_spectrum, nx, ny
			else:
				# If mean1st is False, area1st is select, and so we will need to iterates over each individual spectrum
				average_spectrum, shoots, result, residual, npeaks = mean(ci, axis=1), ci.shape[1], None, None, len(center)
				[nfev, conv] = [zeros(shoots) for z in range(2)]
				if shape != 'Trapezoidal rule':
					[height, width, area] = [zeros((shoots, npeaks)) for z in range(3)]
				else:
					[height, width, area] = [zeros(shoots) for z in range(3)]
				for k in range(shoots):
					guess = fit_guess(x=x, y=ci[:, k],
					                  peaks=npeaks, center=center,
					                  shape_id=shape, asymmetry=asym)
					k_optimized = least_squares(residuals, guess,
					                          args=(
					                          x, average_spectrum, shape),
					                          kwargs=scd, ftol=1e-7, gtol=1e-7,
					                          xtol=1e-7, max_nfev=1000)
					results = fit_results(x, average_spectrum, k_optimized, shape, len(center), scd)
					# saves values
					nfev[k], conv[k] = results[5], results[6]
					if shape != 'Trapezoidal rule':
						for l in range(npeaks):
							height[k, l], width[k, l], area[k, l] = results[4][l]
					else:
						height[k], width[k], area[k] = results[4]
					if k == 0:
						# 1st loop
						nx = results[1]
						residual = results[0][:, 2]
						result = results[2]
					else:
						# other loops
						residual += results[0][:, 2]
						for l in range(results[2].shape[1]):
							result[:, l] += results[2][:, l]
				# Outside the k-loop, we need to reorganize data for saving
				[nfev_avg, conv_avg] = [(mean(x).round(2), std(x).round(2)) for x in [nfev, conv]]
				[height_avg, width_avg, area_avg] = [(mean(x, axis=0), std(x, axis=0)) for x in [height, width, area]]
				h, w, a = [], [], []
				for l in range(npeaks):
					if shape != 'Trapezoidal rule':
						h.append((height_avg[0][l], height_avg[1][l]))
						w.append((width_avg[0][l], width_avg[1][l]))
						a.append((area_avg[0][l], area_avg[1][l]))
					else:
						h.append((height_avg[0], height_avg[1]))
						w.append((width_avg[0], width_avg[1]))
						a.append((area_avg[0], area_avg[1]))
						break
				results = [(x, y, z) for x, y, z in zip(h, w, a)]
				residual /= shoots
				result /= shoots
				# Finally, saves result
				fit_w_counts[i][j][:] = column_stack((x, average_spectrum, residual)), nx, result, shape, results, nfev_avg, conv_avg
			progress.emit(j)
	return fit_w_counts

def equations_translator(center: List, asymmetry: float):
	shapes_and_curves_dict = {'Lorentzian' : lorentz,
	                          'Lorentzian [center fixed]' : lorentz_fixed_center,
	                          'Asymmetric Lorentzian' : lorentz_asymmetric,
	                          'Asym. Lorentzian [center fixed]' : lorentz_asymmetric_fixed_center,
	                          'Asym. Lorentzian [center/as. fixed]' : lorentz_asymmetric_fixed_center_asymmetry,
	                          'Gaussian' : gauss,
	                          'Gaussian [center fixed]' : gauss_fixed_center,
	                          'Voigt Profile': voigt,
	                          'Voigt Profile [center fixed]': voigt_fixed_center,
	                          'Trapezoidal rule': trapz,
	                          'Center': center,
	                          'Asymmetry': asymmetry}
	return shapes_and_curves_dict