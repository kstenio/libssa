#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Kleydson Stenio (kleydson.stenio@gmail.com).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along
# with this program.  If not, see <https://www.gnu.org/licenses/agpl-3.0.html>.


# Imports
from libssa.env.equations import *
from pandas import Series, DataFrame
from PySide6.QtCore import Signal
from scipy.stats import linregress
from scipy.optimize import least_squares, OptimizeResult
from numpy import exp, array, where, min as mini, hstack, vstack, polyfit, trapz, mean, zeros_like, linspace, column_stack, zeros, cumsum, ones, std, log
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


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
	:return: tuple of results: new_wavelength, new_counts, elements, lower, upper, center, noise
	"""
	# Allocate data
	new_wavelength = array([None] * len(elements))
	noise = zeros((len(elements), len(counts), 2))
	new_counts = array([array([None for X in range(len(counts))]) for Y in range(len(elements))], dtype=object)
	subtract_by_region_minimum = False
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
				if subtract_by_region_minimum:
					y_min = mini(y[:, k])
					if y_min > 0:
						y[:, k] -= y_min
					elif y_min < 0:
						y[:, k] += -1 * y_min
					else:
						pass
			# Saves new count
			new_counts[i][j] = y
			# Gets the noise (Standard deviation of beginning and end of the peak)
			ym = y.mean(1)
			get = int(0.2*y.shape[0]) if 0.2*y.shape[0] >= 2 else 2
			nz = ym[:get].std(), ym[-get:].std()
			noise[i][j, :] = nz[0], nz[1]
		# Saves new wavelength
		new_wavelength[i] = x
		progress.emit(i)
	return new_wavelength, new_counts, array(elements), array(lower), array(upper), array(center, dtype=object), array(noise)


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
		guess.append(r * max(y))  # Intensity is the highest value
		guess.append(r * d / 4)  # Width approximation by 1/4 of interval
		if 'voigt' in shape_id.lower():
			guess[-2] = r * max(y) * d / 2  # Area approximation by triangle
			guess.append(r * d / 4)  # Width approximation by 1/4 of interval
		if 'fixed' not in shape_id.lower():
			guess.append(center[i])  # Center (user entered value)
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
					                            args=(w, average_spectrum, shape[i]),
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


def equations_translator(center: list, asymmetry: float) -> dict:
	"""
	Convenient function to return correct function to call (for fit).
	
	:param center: list values of center of peaks
	:param asymmetry: value for peak asymmetry
	:return: dict to be used in fitpeaks
	"""
	shapes_and_curves_dict = {'Lorentzian': lorentz,
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


def linear_model(mode: str, reference: Series, values: tuple, base: str, base_peak: int, selected: str, selected_peak: int, elements: ndarray, noise: ndarray, param: str) -> tuple:
	"""
	Performs linear model of two dependant variables: reference (true value) and the values (dependant).
	Values can be areas or heights. The function fits a curve of type: Predict = INTERCEPT + SLOPE * Reference

	:param mode: mode of operation. Will defines if normalization is or isn't needed
	:param reference: vaules of reference
	:param values: values to be used for predicitons
	:param base: string of the base peak
	:param base_peak: which peak is being used for base (if the peak is resulted as a multi-fitting)
	:param selected: string of the selected peak (for single normalization)
	:param selected_peak: which peak is being used for select (if the peak is resulted as a multi-fitting)
	:param elements: full elements isolated (for all normalization)
	:param noise: array containing values of the standard deviation of noise for each sample (for LoD and LoQ)
	:param param: which parameter is being used (area or height)
	:return: tuple of results to be stored in Spectra.linear (ref, predict, r2, rmse, slope, intercept, lod, loq)
	"""
	# Defines base variables
	idx_b = where(elements == base)[0][0]
	val_b = values[idx_b][:, base_peak]
	sigma = noise[idx_b][reference == min(reference)].min()
	pred_name, pred_val, r2, rmse, slope, intercept, lod, loq = [], [], [], [], [], [], [], []
	# Does the calculations depending on the mode
	if mode == 'No Norm':
		title = '<b>{0}<sub>{1}</sub></b> (No Normalization) [Ref: <u>{2}</u>] (Param: <i>{3}</i>)'
		parameter = val_b.reshape(-1, 1)
		model = LinearRegression().fit(parameter, reference)
		pred_name.append(title.format(base, base_peak+1, reference.name, param))
		pred_val.append(model.predict(parameter))
		r2.append(model.score(parameter, reference))
		rmse.append(mean_squared_error(reference, pred_val[-1]) ** 0.5)
		slope.append(model.coef_[0])
		intercept.append(model.intercept_)
		# Calculates Limit of detection (LoD) and Limit of quantification (LoQ)
		s = polyfit(reference, parameter, 1)[0][0]
		lod.append(3.3*sigma/s)
		loq.append(10*sigma/s)
	else:
		title_norm = '<b>{0}<sub>{1}</sub></b> / <b>{2}<sub>{3}</sub></b> [Ref: <u>{4}</u>] (Param: <i>{5}</i>)'
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
			# Calculates Limit of detection (LoD) and Limit of quantification (LoQ)
			sigma_n = noise[idx_s][reference == min(reference)].min()
			s = polyfit(reference, parameter, 1)[0][0]
			lod.append((3.3 * (sigma/sigma_n))/s)
			loq.append((10 * (sigma/sigma_n))/s)
		else:
			# Gets list for all but base
			n_elements = list(elements)
			for i, p in enumerate(n_elements):
				if p == base:
					n_elements.pop(i)
					break
			# Perform normalized/equivalent model for each peak
			for e in n_elements:
				idx_e = where(elements == e)[0][0]
				val_e = values[idx_e]
				sigma_n = noise[idx_e][reference == min(reference)].min()
				sigma_e = sigma/sigma_n
				for c in range(val_e.shape[1]):
					if mode == 'All Norm':
						parameter = (val_b / val_e[:, c]).reshape(-1, 1)
					else:
						title_norm = '<b>{0}<sub>{1}</sub>*{2}<sub>{3}</sub></b> / <b>{0}<sub>{1}</sub>+{2}<sub>{3}</sub></b> [Ref: <u>{4}</u>] (Param: <i>{5}</i>)'
						parameter = ((val_b * val_e[:, c]) / (val_b + val_e[:, c])).reshape(-1, 1)
						sigma_e = (sigma * sigma_n) / (sigma + sigma_n)
					model = LinearRegression().fit(parameter, reference)
					pred_name.append(title_norm.format(base, base_peak + 1, e, c + 1, reference.name, param))
					pred_val.append(model.predict(parameter))
					r2.append(model.score(parameter, reference))
					rmse.append(mean_squared_error(reference, pred_val[-1]) ** 0.5)
					slope.append(model.coef_[0])
					intercept.append(model.intercept_)
					# Calculates Limit of detection (LoD) and Limit of quantification (LoQ)
					s = polyfit(reference, parameter, 1)[0][0]
					lod.append(3.3 * sigma_e / s)
					loq.append(10 * sigma_e / s)
	# Organizes variables to return
	ref = array((reference.name, reference.to_numpy(), param), dtype=object)
	predict = array((list(zip(pred_name, pred_val))), dtype=object)
	return ref, predict, array(r2), array(rmse), array(slope), array(intercept), array(lod), array(loq)


def pca_scan(attributes: ndarray, norm: bool = False) -> tuple:
	"""
	PCA_Scan function. Receives the attributes matrix and returns the cumulative
	explained variance and optimum number of components (where var > 0.95). If the
	user requested to normalise the matrix, returns the transformed one.
	
	:param attributes: attributes matrix. Each row is a sample, and column an attribute
	:param norm: boolean to choose if attribute matrix will be normalised or not
	:return: tuple of results
	"""
	# organize attributes matrix
	f_attributes = StandardScaler().fit_transform(attributes) if norm else attributes
	# perform full PCA
	pca = PCA().fit(f_attributes)
	# checks and corrects explained variance
	explained_variance = cumsum(pca.explained_variance_ratio_)
	difference = f_attributes.shape[0] - explained_variance.shape[0]
	if difference != 0:
		explained_variance = hstack((explained_variance, ones(difference)))
	# defines minimum components for +95% variance
	optimum_ncomp = len(explained_variance[explained_variance < 0.96])
	return f_attributes, explained_variance, optimum_ncomp


def pca_do(attributes: ndarray, n_comp: int) -> tuple:
	"""
	PCA_Do function. Uses the attributes to perform the PCA model, obtaining the
	loadings and transformed date (scores) for each PC.
	
	:param attributes: attribute matrix (might be normalized)
	:param n_comp: number of components to do the PCA
	:return: tuple of results (scores and loadings)
	"""
	pca = PCA(n_comp).fit(attributes)
	loadings = pca.components_.T
	transformed = pca.transform(attributes)
	return transformed, loadings


def pls_do(attributes: ndarray, reference: DataFrame, n_comp: int, scale: bool, cv_split: int = 5) -> tuple:
	"""
	Perform the PLS Regression in the attributes and returns the model and results of the regression.
	
	:param attributes: attribute matrix (samples in rows, attributes in columns)
	:param reference: reference/true value DF for a single element (for modelling)
	:param n_comp: number of components/latent variables of the model
	:param scale: boolean to turn on/off the normalization of the input data
	:param cv_split: determines how many groups will be used to perform cross validation (default: 5-fold)
	:return: tuple of results
	"""
	# Organizes variables before applying model
	pls = PLSRegression(n_comp, scale=scale)
	reference = array(reference).reshape(-1, 1)
	# Now, we get cross validation data
	cv_pred = cross_val_predict(pls, attributes, reference, cv=cv_split)
	cv_r2 = cross_val_score(pls, attributes, reference, scoring='r2', cv=cv_split).max()
	# For pure prediction
	pls.fit(attributes, reference)
	predicted = pls.predict(attributes)
	predict_r2 = pls.score(attributes, reference)
	# Residuals and others parameters
	residual = reference - predicted
	predict_rmse = std(residual)
	cv_rmse = std(reference - cv_pred)
	return pls, reference, predicted, residual, predict_r2, predict_rmse, cv_pred, cv_r2, cv_rmse


def tne_do(samples: tuple, param_array: ndarray, tne_df: DataFrame, ei_str: str) -> tuple:
	"""
	Does a Saha-Boltzmann plot to obtain plasma temperature and electrons density for
	many samples. As input this functions needs values of energies of higher level (Ek),
	Einstein probability of transition and degenerate energy levels (gAk) for the used
	emission lines. Also, atomic and ionic lines are needed.
	Those data can be obtained from NIST Atomic Spectra Database Lines Form:
		* https://physics.nist.gov/PhysRefData/ASD/lines_form.html (accessed on Aug/2022)
	Returns parameters of the plot, plus a report DF.
	
	:param samples: tuple containing the names of the samples
	:param param_array: array with all calculated areas (or heights) for all peaks and samples
	:param tne_df: DataFrame containing lines information (ionization, Ek and gAk)
	:param ei_str: string containing the ionization energy of the element
	:return: tuple of results (x, y, fit and parameters obtained from the plot)
	"""
	# Organizes useful variables
	ei = float(ei_str.split()[0])
	kb = 0.000086173303
	ke = 2.07e+16
	# Gets index for atomic and ionic species
	atm_idx = tne_df['Ionization'] == '1'
	ion_idx = tne_df['Ionization'] == '2'
	atm_tot = atm_idx.to_numpy().sum()
	ion_tot = ion_idx.to_numpy().sum()
	# Separates data into atomic
	ln_param_atomic = log(param_array[:, atm_idx])
	ln_gak_atomic = log(tne_df['gAk'][atm_idx].astype(float)).to_numpy()
	ek_atomic = tne_df['Ek'][atm_idx].astype(float).to_numpy()
	# And into ionic
	ln_param_ionic = log(param_array[:, ion_idx])
	ln_gak_ionic = log(tne_df['gAk'][ion_idx].astype(float)).to_numpy()
	ek_ionic = tne_df['Ek'][ion_idx].astype(float).to_numpy()
	# Now, we must walk into 3 levels: samples, atomic and ionic
	x_ = zeros((len(samples), atm_tot * ion_tot))
	y_ = zeros_like(x_)
	fit_ = zeros_like(x_)
	result_df = DataFrame(index=samples, columns=['T', 'ΔT', 'Ne', 'ΔNe', 'R2', 'R'], data=0.0)
	for i in range(len(samples)):
		x, y = [], []
		for at in range(atm_tot):
			for io in range(ion_tot):
				x.append(ek_atomic[at] - ek_ionic[io] - ei)
				y.append(ln_param_atomic[i, at] + ln_gak_ionic[io] - ln_param_ionic[i, io] - ln_gak_atomic[at])
		# Created main lists, we transform them into arrays
		x, y = array(x), array(y)
		# And then, we perform linear regression to obtain curve fitting
		reg = linregress(x, y)
		# Based on regression values, we can start calculating the parameters
		slope, intercept, r, r2, sslope, sintercept = reg.slope, reg.intercept, reg.rvalue, reg.rvalue ** 2, reg.stderr, reg.intercept_stderr
		fit = slope * x + intercept
		temp = -1 / (kb * slope)
		Ne = exp(intercept) * (temp ** 1.5) * ke
		# Get deviations
		stemp = -1 * temp * (sslope / slope)
		sNe = -1 * Ne * (sintercept / intercept)
		# Saves plot data
		x_[i] = x
		y_[i] = y
		fit_[i] = fit
		# And finally, saves report data
		result_df.loc[samples[i]] = (temp, stemp, Ne, sNe, r2, r)
	return x_, y_, fit_, result_df
