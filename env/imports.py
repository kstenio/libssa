#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  imports.py
#
#  Copyright 2020 Kleydson Stenio <kleydson.stenio@gmail.com>
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

# imports
from os import listdir
from pandas import read_csv
from pathlib import PosixPath
from typing import List, Tuple
from PySide2.QtCore import Signal
from numpy import array, equal, ndarray, column_stack

def load(folder: List[PosixPath], mode: str, delim: str, header: int, wcol: int, ccol: int, progress: Signal) -> Tuple[ndarray, ndarray]:
	"""
	This method loads spectra and returns global variables wavelength and counts
	:param folder: PosixPath list of input folder/files (sorted)
	:param mode: File reading mode. 'Single' for one file per sample, or 'Multiple' for one folder per sample, multiple files per shoot
	:param delim: Delimiter (space, tab, comma and semicolon)
	:param header: Rows to skip in the spectra files
	:param wcol: Which column is wavelength
	:param ccol: Which column is counts
	:param progress: Qt signal for multithreading
	:return: Wavelength and Counts arrays
	"""
	# organizes delimiter
	if delim == 'TAB':
		delim = '\t'
	elif delim == 'SPACE':
		delim = '\s+'
	# creates wavelength and counts vectors
	wavelength, counts, count, sort = array(([None])), array(([None]*len(folder)), dtype=object), None, False
	if mode == "Single":
		# reads all files
		for i, file in enumerate(folder):
			if i == 0:
				matrix = read_csv(file, delimiter=delim, skiprows=header, dtype=float).to_numpy()
				wavelength, counts[i] = matrix[:, 0], matrix[:, 1:]
				if not all(equal(wavelength, wavelength[wavelength.argsort()])):
					sort = True
					counts[i] = counts[i][wavelength.argsort()]
			else:
				# after reading wavelength and defining if sort is needed, reads counts
				counts[i] = read_csv(file, delimiter=delim, skiprows=header, dtype=float).to_numpy()[:, 1:]
				if sort:
					counts[i] = counts[i][wavelength.argsort()]
			# emits signal for GUI
			progress.emit(i+1)
		# by the end - if needed - sorts wavelength
		if sort:
			wavelength.sort()
		# return values
		return wavelength, counts
	elif mode == "Multiple":
		# reads all files in each folder
		for j, folders in enumerate(folder):
			files = listdir(folders)
			files.sort()
			files = [folders.joinpath(x) for x in files]
			for k, spectrum in enumerate(files):
				# reads wavelength
				if (j == 0) and (k == 0):
					wavelength = read_csv(spectrum, usecols=[wcol-1], delimiter=delim, skiprows=header, dtype=float).to_numpy().T[0]
					if not all(equal(wavelength, wavelength[wavelength.argsort()])):
						sort = True
				# reads counts
				if k == 0:
					count = read_csv(spectrum, usecols=[ccol-1], delimiter=delim, skiprows=header, dtype=float).to_numpy()
				else:
					count = column_stack((count, read_csv(spectrum, usecols=[ccol-1], delimiter=delim, skiprows=header, dtype=float).to_numpy()))
			# back in j loop, save count in counts vector and sort if needed
			counts[j] = count
			if sort:
				counts[j] = counts[j][wavelength.argsort()]
			# emits signal for GUI
			progress.emit(j + 1)
		# by the end - if needed - sorts wavelength
		if sort:
			wavelength.sort()
		# return values
		return wavelength, counts
	else:
		raise ValueError('Wrong reading mode.')
	