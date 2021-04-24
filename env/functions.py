#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  ./env/functions.py
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

# Imports
from env.equations import *
from pandas import Series
from PySide2.QtCore import Signal
from scipy.optimize import least_squares, OptimizeResult
from numpy import array, where, min as mini, hstack, vstack, polyfit, trapz, mean, zeros_like, linspace, column_stack, zeros
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


# Peak isolation functions
def isopeaks(wavelength: ndarray, counts: ndarray, elements: list, lower: list, upper: list, center: list, linear: bool, anorm: bool, progress: Signal) -> tuple:
	"""
	Isolates peaks based on input from user.

	:param wavelength: full spectrum wavelength
	:param counts: count array for all samples (each element is a matrix)
	:param elements: list of elements to be isolated
	:param lower: lower wavelength for the i-th element
	:param upper: upper wavelength for the i-th element
	:param center: center wavelength(s) for the i-th element (it might be a list for multi peak element)
	:param linear: boolean to enable or disable normalization by the baseline
	:param anorm: boolean to enable or disable normalization by the area of the baseline
	:param progress: PySide Signal object (for multithreading)
	:return: tuple of results: new_wavelength, new_counts, elements, lower, upper, center
	"""
	# Allocate data
	new_wavelength = array([None] * len(elements))
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
		new_wavelength[i] = x
		progress.emit(i)
	return new_wavelength, new_counts, array(elements), array(lower), array(upper), array(center, dtype=object)


# Peak fitting functions
def fit_guess(x: ndarray, y: ndarray, peaks: int, center: list, shape_id: str, asymmetry=None) -> list:
	"""
	Creates fit guess for peak fitting. The method will vary depending on the shape of the signal.

	:param x: values of the wavelength
	:param y: values of the intensities
	:param peaks: number of peaks
	:param center: list containing the center wavelength (size == peaks)
	:param shape_id: string containing the shape of the signal
	:param asymmetry: value for the asymmetry of the signal (for Asymmetric Lorentzian)
	:return: list with the initial guess
	"""
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

def residuals(guess: list, x: ndarray, y: ndarray, shape_id: str, **kwargs) -> ndarray:
	"""
	Special function to be used side-by-side with least_squares, allowing the minimization of guess.
	This function acts like a decorator for the fit_results function.

	:param guess: initial guess (== the parameters to be minimized)
	:param x: wavelength array
	:param y: intensities array (observed values)
	:param shape_id: the shape of the signal
	:param kwargs: extra arguments to be passed away
	:return: difference between the observed (y) and the fitted (passed as dict)
	"""
	function_kwargs = {'Center': kwargs['Center'], 'Asymmetry': kwargs['Asymmetry']}
	if shape_id == 'Trapezoidal rule':
		return zeros_like(y)
	else:
		return y - kwargs[shape_id](x, *guess, **function_kwargs)

def fit_values(ny: ndarray, shape: str, param: ndarray) -> tuple:
	"""
	Function to return the fitted values of an individual peak after fitting is performed.

	:param ny: fitted intensities
	:param shape: shape of the signal
	:param param: params of the fit (optimized values of guess)
	:return: values of height, width and area for the passed peak
	"""
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

def fit_results(x: ndarray, y:ndarray, optimized: OptimizeResult, shape: str, npeaks: int, sdict: dict) -> tuple:
	"""
	Function to return all of the results of multi peak for an element.

	:param x: wavelength array
	:param y: intensities array (observed values)
	:param optimized: parameters of the multi peak fitting (size depends on number of peaks)
	:param shape: shape of the signal
	:param npeaks: number of peaks
	:param sdict: special dict created by the equation_translator
	:return: result of multi peak fitting: data[y, residual], total_fit[every_peak, ..., sum of peaks], heights, widths, areas
	"""
	# Organizes variables
	solution, residual = optimized.x, optimized.fun
	individuals_solution = array_split(nabs(solution), npeaks)
	[heights, widths, areas] = [zeros(npeaks) for val in range(3)]
	# With optimized, we can have the new  linspace x-axis
	if shape != 'Trapezoidal rule':
		nx = linspace(x[0], x[-1], 1000)
		# creates the total result
		total_fit = zeros((nx.size, npeaks + 1))
		for i, individuals in enumerate(individuals_solution):
			indv_dict = {'Center': [sdict['Center'][i]], 'Asymmetry': sdict['Asymmetry']}
			total_fit[:, i] = sdict[shape](nx, *individuals, **indv_dict)
			heights[i], widths[i], areas[i] = fit_values(total_fit[:, i], shape, individuals)
		total_fit[:, -1] = nsum(total_fit[:, :-1], 1)
	else:
		total_fit = column_stack((y, y))
		heights[:], widths[:], areas[:] = max(y), (x[-1]-x[0])/4, trapz(y, x)
	return column_stack((y, residual)), total_fit, heights, widths, areas

def fitpeaks(iso_wavelengths: ndarray, iso_counts: ndarray, shape: list, asymmetry: list, isolated: dict, mean1st: bool, progress: Signal) -> tuple:
	"""
	Main function to create multi element and multi peak fitting for a large sample set.

	:param iso_wavelengths: array of arrays, where each individual one is the isolated wavelength
	:param iso_counts: array of array of matrices, where each individual one are the intensities for each sample and element: [element...[samples...[counts[wavelengths, shoots]]]]
	:param shape: list of shapes for each element
	:param asymmetry: list of asymmetries (only !=0 for Asym. Lorentzian [center/as. fixed])
	:param isolated: Spectra.isolated structure/dict that carries values of count, nsamples, element, center, upper and lower for all peaks
	:param mean1st: boolean that says of fit method is mean first or area first
	:param progress: PySide Signal object (for multithreading)
	:return: tuple of results to be added to the Spectra.fit dict of results (nfevs, convegences, data, total, heights, widths, areas, areas_std, shape)
	"""
	# Creates empty arrays to save all needed elements while fitting is being performed
	# Sizes and types will be different, depending the properties we are going to save:
	#   nfevs: 1D array (size of elements), type is int
	#   convergence: 1D array (size of elements), type is bool
	#   data: 3D array (rows = wavelengths of isolated peak, columns = 2 [observed and residuals], depth = number of samples) inside 1D tuple (size of elements)
	#   total: 3D array (rows = 1000 [linspace size] , columns = number of peaks + 1 [for sum], depth = number of samples) inside 1D tuple (size of elements)
	#   areas (+std), widths, heights: 2D array (rows = number of samples, columns = number of peaks) inside a 1D tuple (size of elements)
	nfevs = zeros((isolated['Count'], isolated['NSamples']), dtype=int)
	convegences = zeros((isolated['Count'], isolated['NSamples']), dtype=bool)
	data = [zeros((isolated['NSamples'], iw.size, 2), dtype=float) for iw in iso_wavelengths]
	total = [zeros((isolated['NSamples'], 1000, len(c) + 1), dtype=float) if s != 'Trapezoidal rule' else zeros((isolated['NSamples'], iw.size, 2), dtype=float) for c, s, iw in zip(isolated['Center'], shape, iso_wavelengths)]
	[areas, areas_std, widths, heights] = [[zeros((isolated['NSamples'], len(c)), dtype=float) for c in isolated['Center']] for val in range(4)]
	shape = array(shape)
	# Defines values for tolerances
	tols = [1e-7, 1e-7, 1e-7, 1000]
	# Goes in element level: same size as iso_wavelengths
	for i, w in enumerate(iso_wavelengths):
		# Gets a dict for shapes and fit equations
		center = isolated['Center'][i]
		scd = equations_translator(center=center, asymmetry=asymmetry[i])
		# Now goes into sample level: size of each i-th iso_wavelengths
		for j, ci in enumerate(iso_counts[i]):
			# Regarding modes, we have mean 1st or area 1st, which defines how results are exported
			if mean1st:
				# If mean1st is True, take the mean of iso_counts[i][j] and pass it to perform fit
				average_spectrum = mean(ci, axis=1)
				guess = fit_guess(x=w, y=average_spectrum, peaks=len(center), center=center, shape_id=shape[i], asymmetry=asymmetry[i])
				optimized = least_squares(residuals, guess,
				                          args=(w, average_spectrum, shape[i]),
				                          kwargs=scd, ftol=tols[0], gtol=tols[1],
				                          xtol=tols[2], max_nfev=tols[3])
				# Gets the result based on optimized solution
				# The function returns:
				#   [0] data -> original_intensities and residuals (columns)
				#   [1] total_fit -> each column is a fit based on peak number (which is based on center size) and the last one is the sum
				#   [2] heights, [3] widths, [4] areas -> size depends on number of peaks
				results = fit_results(w, average_spectrum, optimized, shape[i], len(center), scd)
				# Finally, appends results into the return variables
				nfevs[i, j] = optimized.nfev
				convegences[i, j] = optimized.success
				data[i][j] = results[0]
				total[i][j] = results[1]
				heights[i][j] = results[2]
				widths[i][j] = results[3]
				areas[i][j] = results[4]
			else:
				# If mean1st is False, area1st is select, and so we will need to iterates over each individual spectrum
				average_spectrum, shoots, npeaks = mean(ci, axis=1), ci.shape[1], len(center)
				k_data, k_total, k_heights, k_widths, k_areas = None, None, [], [], []
				for k in range(shoots):
					guess = fit_guess(x=w, y=ci[:, k],
					                  peaks=npeaks, center=center,
					                  shape_id=shape[i], asymmetry=asymmetry[i])
					k_optimized = least_squares(residuals, guess,
					                          args=(
					                          w, average_spectrum, shape[i]),
					                          kwargs=scd, ftol=tols[0], gtol=tols[1],
					                          xtol=tols[2], max_nfev=tols[3])
					# Gets the result based on optimized solution
					results = fit_results(w, average_spectrum, k_optimized, shape[i], len(center), scd)
					# Saves some values
					nfevs[i, j] += k_optimized.nfev
					convegences[i, j] += k_optimized.success
					k_heights.append(results[2])
					k_widths.append(results[3])
					k_areas.append(results[4])
					if k == 0:
						# 1st loop
						k_data = results[0]
						k_total = results[1]
					else:
						# other loops
						k_data += results[0]
						k_total += results[1]
				# Outside the k-loop, we need to reorganize data for saving
				nfevs[i, j] /= shoots
				convegences[i, j] /= shoots
				data[i][j] = k_data / shoots
				total[i][j] = k_total / shoots
				heights[i][j] = array(k_heights).mean()
				widths[i][j] = array(k_widths).mean()
				areas[i][j] = array(k_areas).mean()
				areas_std[i][j] = array(k_areas).std()
			progress.emit(j)
	return nfevs, convegences, tuple(data), tuple(total), tuple(heights), tuple(widths), tuple(areas), tuple(areas_std), shape

def equations_translator(center: list, asymmetry: float):
	"""
	Convenient function to return correct function to call (for fit).
	
	:param center: list values of center of peaks
	:param asymmetry: value for peak asymmetry
	:return: dict to be used in fitpeaks
	"""
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

def linear_model(mode: str, reference: Series, values: tuple, base: str, base_peak: int, selected: str, selected_peak: int, elements: ndarray, param: str):
	# Defines base variables
	idx_b = where(elements == base)[0][0]
	val_b = values[idx_b][:, base_peak]
	pred_name, pred_val, r2, rmse, slope, intercept = [], [], [], [], [], []
	# Does the calculations depending on the mode
	if mode == 'No Norm':
		title = '<b>{0}-P{1}</b> (No Normalization) [Ref: <u>{2}</u>] (Param: <i>{3}</i>)'
		parameter = val_b.reshape(-1, 1)
		model = LinearRegression().fit(parameter, reference)
		pred_name.append(title.format(base, base_peak+1, reference.name, param))
		pred_val.append(model.predict(parameter))
		r2.append(model.score(parameter, reference))
		rmse.append(mean_squared_error(reference, pred_val[-1]) ** 0.5)
		slope.append(model.coef_[0])
		intercept.append(model.intercept_)
	else:
		title_norm = '<b><sup>{0}-P{1}</sup>&frasl;<sub>{2}-P{3}</sub></b> [Ref: <u>{4}</u>] (Param: <i>{5}</i>)'
		if mode == 'Peak Norm':
			idx_s = where(elements == selected)[0][0]
			val_s = values[idx_s][:, selected_peak]
			parameter = (val_b / val_s).reshape(-1, 1)
			model = LinearRegression().fit(parameter, reference)
			pred_name.append(title_norm.format(base, base_peak + 1, selected, selected_peak+1, reference.name, param))
			pred_val.append(model.predict(parameter))
			r2.append(model.score(parameter, reference))
			rmse.append(mean_squared_error(reference, pred_val[-1]) ** 0.5)
			slope.append(model.coef_[0])
			intercept.append(model.intercept_)
		elif mode == 'All Norm':
			# Gets list for all but base
			n_elements = list(elements)
			for i, p in enumerate(n_elements):
				if p == base:
					n_elements.pop(i)
					break
			# Creates empty lists for saving results
			pred_name, pred_val, r2, slope, intercept = [], [], [], [], []
			for e in n_elements:
				idx_e = where(elements == e)[0][0]
				val_e = values[idx_e]
				for c in range(val_e.shape[1]):
					parameter = (val_b / val_e[:, c]).reshape(-1, 1)
					model = LinearRegression().fit(parameter, reference)
					pred_name.append(title_norm.format(base, base_peak + 1, e, c + 1, reference.name, param))
					pred_val.append(model.predict(parameter))
					r2.append(model.score(parameter, reference))
					rmse.append(mean_squared_error(reference, pred_val[-1]) ** 0.5)
					slope.append(model.coef_[0])
					intercept.append(model.intercept_)
	# Organizes variables to return
	ref = array((reference.name, reference.to_numpy(), param), dtype=object)
	predict = array((list(zip(pred_name, pred_val))), dtype=object)
	return ref, predict, array(r2), array(rmse), array(slope), array(intercept)