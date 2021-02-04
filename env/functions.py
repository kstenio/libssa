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

from numpy import ndarray, array, where, min as mini, hstack, vstack, polyfit, trapz
from PySide2.QtCore import Signal
from typing import List, Tuple
from env.equations import lorentz

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
		new_wavelength[i] = e, array([lower[i], upper[i], center[i].split(';')]), x
		progress.emit(i)
	return new_wavelength, new_counts

def fitpeaks(iso_wavelengths, iso_counts):
	for i, w in enumerate(iso_wavelengths):
		print(w[:2], iso_counts[i])
		pass