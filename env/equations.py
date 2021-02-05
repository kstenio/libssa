#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  equations.py
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

from numpy import ndarray, array, empty, sum, std

# Lorentzian functions
def lorentz(x: ndarray, *args: float, **kwargs) -> ndarray:
	"""
	:param x: Input vector (wavelength for isolated region)
	:param args: Parameters of function. These values can be optimized for fit.
	:param kwargs: Extra fixed parameters (number of peaks, center, asymmetry)
	:return: y values for function (intensities)
	"""
	peaks = kwargs['Peaks']
	lo = empty((x.size, peaks))
	for i in range(peaks):
		h, w, c = args[3 * i], args[(3 * i) + 1], args[(3 * i) + 2]
		lo[:, i] = abs(h) / (1 + ((x - c) / (0.5 * w)) ** 2)
	return sum(lo, 1)

def lorentz_fixed_center(x: ndarray, *args: float, **kwargs) -> ndarray:
	"""
	:param x: Input vector (wavelength for isolated region)
	:param args: Parameters of function. These values can be optimized for fit.
	:param kwargs: Extra fixed parameters (number of peaks, center, asymmetry)
	:return: y values for function (intensities)
	"""
	peaks, c = kwargs['Peaks'], kwargs['Center']
	lofc = empty((x.size, peaks))
	for i in range(peaks):
		h, w = args[2 * i], args[(2 * i) + 1]
		lofc[:, i] = abs(h) / (1 + ((x - c[i]) / (0.5 * w)) ** 2)
	return sum(lofc, 1)

def lorentz_asymmetric(x: ndarray, *args: float, **kwargs) -> ndarray:
	"""
	:param x: Input vector (wavelength for isolated region)
	:param args: Parameters of function. These values can be optimized for fit.
	:param kwargs: Extra fixed parameters (number of peaks, center, asymmetry)
	:return: y values for function (intensities)
	"""
	peaks = kwargs['Peaks']
	loa = empty((x.size, peaks))
	for i in range(peaks):
		h, w, c, m = args[4 * i], args[(4 * i) + 1], args[(4 * i) + 2], args[(4 * i) + 3]
		loa[x <= c, i] = abs(h) / (1 + ((x[x <= c] - c) / (0.5 * w * m)) ** 2)
		loa[x > c, i] = abs(h) / (1 + ((x[x > c] - c) / (0.5 * w * m)) ** 2)
	return sum(loa, 1)

def lorentz_asymmetric_fixed_center(x: ndarray, *args: float, **kwargs) -> ndarray:
	"""
	:param x: Input vector (wavelength for isolated region)
	:param args: Parameters of function. These values can be optimized for fit.
	:param kwargs: Extra fixed parameters (number of peaks, center, asymmetry)
	:return: y values for function (intensities)
	"""
	peaks, c = kwargs['Peaks'], kwargs['Center']
	loafc = empty((x.size, peaks))
	for i in range(peaks):
		h, w, m = args[3 * i], args[(3 * i) + 1], args[(3 * i) + 2]
		loafc[x <= c[i], i] = abs(h) / (1 + ((x[x <= c[i]] - c) / (0.5 * w * m)) ** 2)
		loafc[x > c[i], i] = abs(h) / (1 + ((x[x > c[i]] - c[i]) / (0.5 * w * m)) ** 2)
	return sum(loafc, 1)

def lorentz_asymmetric_fixed_center_asymmetry(x: ndarray, *args: float, **kwargs) -> ndarray:
	"""
	:param x: Input vector (wavelength for isolated region)
	:param args: Parameters of function. These values can be optimized for fit.
	:param kwargs: Extra fixed parameters (number of peaks, center, asymmetry)
	:return: y values for function (intensities)
	"""
	peaks, c, m = kwargs['Peaks'], kwargs['Center'], kwargs['Asymmetry']
	loafca = empty((x.size, peaks))
	for i in range(peaks):
		h, w = args[2 * i], args[(2 * i) + 1]
		loafca[x <= c[i], i] = abs(h) / (1 + ((x[x <= c[i]] - c) / (0.5 * w * m[i])) ** 2)
		loafca[x > c[i], i] = abs(h) / (1 + ((x[x > c[i]] - c[i]) / (0.5 * w * m[i])) ** 2)
	return sum(loafca, 1)

# Residuals function
def residuals(guess, x, y, shape_id, **kwargs):
	function_kwargs = {'Center': kwargs['Center'], 'Extra': kwargs['Extra']}
	return y - kwargs[shape_id](x, *guess, **function_kwargs)

