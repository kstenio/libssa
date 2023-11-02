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
from scipy.special import wofz
from numpy import sum as nsum, abs as nabs
from numpy import ndarray, empty, sum, array_split, exp, real, log, pi


#
# Lorentzian functions
#
def lorentz(x: ndarray, *args: [float], **kwargs: dict) -> ndarray:
	"""
	Lorentz Function. All parameters are adjusted.
	
	:param x: Input vector (wavelength for isolated region)
	:param args: Parameters of function. These values can be optimized for fit
	:param kwargs: Extra fixed parameters (center, asymmetry)
	:return: y values for function (intensities)
	"""
	nparams = 3
	peaks = len(args) // nparams
	params = array_split(nabs(args), peaks)
	lo = empty((x.size, peaks))
	for i, p in enumerate(params):
		h, w, c = p
		lo[:, i] = h / (1 + 4 * ((x - c) / w) ** 2)
	return nsum(lo, 1)


def lorentz_fixed_center(x: ndarray, *args: [float], **kwargs: dict) -> ndarray:
	"""
	Lorentz Function. All parameters are adjusted but center.
	
	:param x: Input vector (wavelength for isolated region)
	:param args: Parameters of function. These values can be optimized for fit
	:param kwargs: Extra fixed parameters (number of peaks, center, asymmetry)
	:return: y values for function (intensities)
	"""
	nparams = 2
	peaks = len(args) // nparams
	params, c = array_split(nabs(args), peaks), kwargs['Center']
	lofc = empty((x.size, peaks))
	for i, p in enumerate(params):
		h, w = p
		lofc[:, i] = h / (1 + ((x - c[i]) / (0.5 * w)) ** 2)
	return sum(lofc, 1)


def lorentz_asymmetric(x: ndarray, *args: [float], **kwargs: dict) -> ndarray:
	"""
	Asymmetric Lorentz Function. All parameters are adjusted.
	
	:param x: Input vector (wavelength for isolated region)
	:param args: Parameters of function. These values can be optimized for fit
	:param kwargs: Extra fixed parameters (number of peaks, center, asymmetry)
	:return: y values for function (intensities)
	"""
	nparams = 4
	peaks = len(args) // nparams
	params, c = array_split(nabs(args), peaks), kwargs['Center']
	loa = empty((x.size, peaks))
	for i, p in enumerate(params):
		h, w, c, m = p
		m = m if 0.2 < m < 0.8 else 0.5
		loa[x <= c, i] = h / (1 + ((x[x <= c] - c) / (0.5 * w * m)) ** 2)
		loa[x > c, i] = h / (1 + ((x[x > c] - c) / (0.5 * w *(1-m))) ** 2)
	return sum(loa, 1)


def lorentz_asymmetric_fixed_center(x: ndarray, *args: [float], **kwargs: dict) -> ndarray:
	"""
	Asymmetric Lorentz Function. All parameters are adjusted but center.
	
	:param x: Input vector (wavelength for isolated region)
	:param args: Parameters of function. These values can be optimized for fit
	:param kwargs: Extra fixed parameters (number of peaks, center, asymmetry)
	:return: y values for function (intensities)
	"""
	nparams = 3
	peaks = len(args) // nparams
	params, c = array_split(nabs(args), peaks), kwargs['Center']
	loafc = empty((x.size, peaks))
	for i, p in enumerate(params):
		h, w, m = p
		m = m if 0.2 < m < 0.8 else 0.5
		loafc[x <= c[i], i] = h / (1 + ((x[x <= c[i]] - c[i]) / (0.5 * w * m)) ** 2)
		loafc[x > c[i], i] = h / (1 + ((x[x > c[i]] - c[i]) / (0.5 * w * (1 - m))) ** 2)
	return sum(loafc, 1)


def lorentz_asymmetric_fixed_center_asymmetry(x: ndarray, *args: [float], **kwargs: dict) -> ndarray:
	"""
	Asymmetric Lorentz Function. All parameters are adjusted but center and asymmetry.
	
	:param x: Input vector (wavelength for isolated region)
	:param args: Parameters of function. These values can be optimized for fit
	:param kwargs: Extra fixed parameters (number of peaks, center, asymmetry)
	:return: y values for function (intensities)
	"""
	nparams = 2
	peaks = len(args) // nparams
	params, c, mf = array_split(nabs(args), peaks), kwargs['Center'], kwargs['Asymmetry']
	loafca = empty((x.size, peaks))
	for i, p in enumerate(params):
		h, w = p
		loafca[x <= c[i], i] = h / (1 + ((x[x <= c[i]] - c[i]) / (0.5 * w * mf)) ** 2)
		loafca[x > c[i], i] = h / (1 + ((x[x > c[i]] - c[i]) / (0.5 * w * (1.0 - mf))) ** 2)
	return sum(loafca, 1)


#
# Gaussian functions
#
def gauss(x: ndarray, *args: [float], **kwargs: dict) -> ndarray:
	"""
	Gaussian Function. All parameters are adjusted.
	
	:param x: Input vector (wavelength for isolated region)
	:param args: Parameters of function. These values can be optimized for fit
	:param kwargs: Extra fixed parameters (center, asymmetry)
	:return: y values for function (intensities)
	"""
	nparams = 3
	peaks = len(args) // nparams
	params = array_split(nabs(args), peaks)
	ga = empty((x.size, peaks))
	for i, p in enumerate(params):
		h, w, c = p
		ga[:, i] = h * exp((-2) * ((x - c) / w) ** 2)
	return nsum(ga, 1)


def gauss_fixed_center(x: ndarray, *args: [float], **kwargs: dict) -> ndarray:
	"""
	Gaussian Function. All parameters are adjusted but center.
	
	:param x: Input vector (wavelength for isolated region)
	:param args: Parameters of function. These values can be optimized for fit
	:param kwargs: Extra fixed parameters (center, asymmetry)
	:return: y values for function (intensities)
	"""
	nparams = 2
	peaks = len(args) // nparams
	params, c = array_split(nabs(args), peaks), kwargs['Center']
	gafc = empty((x.size, peaks))
	for i, p in enumerate(params):
		h, w = p
		gafc[:, i] = h * exp((-2) * ((x - c[i]) / w) ** 2)
	return nsum(gafc, 1)


#
# Voigt functions
#
def voigt(x: ndarray, *args: [float], **kwargs: dict) -> ndarray:
	"""
	Voigt Profile function. All parameters are adjusted.
	
	:param x: Input vector (wavelength for isolated region)
	:param args: Parameters of function. These values can be optimized for fit
	:param kwargs: Extra fixed parameters (center, asymmetry)
	:return: y values for function (intensities)
	"""
	nparams = 4
	peaks = len(args) // nparams
	params = array_split(nabs(args), peaks)
	vo = empty((x.size, peaks))
	for i, p in enumerate(params):
		a, wl, wg, c = p
		sigma, gamma = wg / (2 * (2 * log(2))**0.5), wl / 2
		z = (x - c + 1j*gamma) / (sigma*(2**0.5))
		vo[:, i] = (a * real(wofz(z))) / (sigma*((2*pi)**0.5))
	return nsum(vo, 1)


def voigt_fixed_center(x: ndarray, *args: [float], **kwargs: dict) -> ndarray:
	"""
	Voigt Profile function. All parameters are adjusted but center.
	
	:param x: Input vector (wavelength for isolated region)
	:param args: Parameters of function. These values can be optimized for fit
	:param kwargs: Extra fixed parameters (center, asymmetry)
	:return: y values for function (intensities)
	"""
	nparams = 3
	peaks = len(args) // nparams
	params, c = array_split(nabs(args), peaks), kwargs['Center']
	vofc = empty((x.size, peaks))
	for i, p in enumerate(params):
		a, wl, wg = p
		sigma, gamma = wg / (2 * (2 * log(2))**0.5), wl / 2
		z = (x - c[i] + 1j*gamma) / (sigma*(2**0.5))
		vofc[:, i] = (a * real(wofz(z))) / (sigma*((2*pi)**0.5))
	return nsum(vofc, 1)
