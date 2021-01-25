#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  imports.py
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

# imports
from os import listdir
from pandas import read_csv, read_excel, DataFrame, Series
from pathlib import Path
from typing import List, Tuple
from PySide2.QtCore import Signal
from numpy import array, array_equal, ndarray, column_stack, mean, dot, zeros, median, abs as nabs, subtract
from scipy.linalg import norm
from scipy.stats import pearsonr

def load(folder: List[Path], mode: str, delim: str, header: int, wcol: int, ccol: int, dec: int, progress: Signal) -> Tuple[ndarray, ndarray]:
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
				matrix = read_csv(file, delimiter=delim, skiprows=header).to_numpy(dtype=float).round(dec)
				wavelength, counts[i] = matrix[:, 0], matrix[:, 1:]
				if not array_equal(wavelength, wavelength[wavelength.argsort()]):
					sort = True
					counts[i] = counts[i][wavelength.argsort()]
			else:
				# after reading wavelength and defining if sort is needed, reads counts
				counts[i] = read_csv(file, delimiter=delim, skiprows=header).to_numpy(dtype=float).round(dec)[:, 1:]
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
					wavelength = read_csv(spectrum, usecols=[wcol-1], delimiter=delim, skiprows=header).to_numpy(dtype=float).round(dec).T[0]
					if not array_equal(wavelength, wavelength[wavelength.argsort()]):
						sort = True
				# reads counts
				if k == 0:
					count = read_csv(spectrum, usecols=[ccol-1], delimiter=delim, skiprows=header).to_numpy(dtype=float).round(dec)
				else:
					count = column_stack((count, read_csv(spectrum, usecols=[ccol-1], delimiter=delim, skiprows=header).to_numpy(dtype=float).round(dec)))
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

def outliers(mode: str, criteria: float, counts: ndarray, progress: Signal) -> ndarray:
	# creates counts new vector
	out_counts = array(([None] * counts.__len__()), dtype=object)
	if mode == 'SAM':
		for i in range(counts.__len__()):
			out_average = mean(counts[i], 1)
			out_counts[i] = out_average
			for j in range(counts[i].shape[1]):
				costheta = dot(out_average, counts[i][:, j]) / ( norm(out_average)*norm(counts[i][:, j]) )
				if costheta >= criteria:
					out_counts[i] = column_stack((out_counts[i], counts[i][:, j]))
			out_counts[i] = out_counts[i][:, 1:]
			progress.emit(i)
	elif mode == 'MAD':
		b = 1.4826
		for i in range(counts.__len__()):
			# calculates MAD for each wavelength
			ith_mad_vector = zeros(counts[i].shape[0])
			ith_median = median(counts[i], 1)
			ith_mad_vector = b * median(nabs(subtract(counts[i].T, ith_median).T), 1)
			# now, check if each shoot is or isn't an outlier
			zero_counts = zeros(counts[i].shape[0])
			bool_checker = array([criteria] * counts[i].shape[0])
			for k in range(counts[i].shape[1]):
				criteria_ = (counts[i][:, k] - ith_median) / ith_mad_vector
				criteria_bool = nabs(criteria_) < bool_checker
				if criteria_bool.sum() / counts[i].shape[0] >= 0.95:
					zero_counts = column_stack((zero_counts, counts[i][:, k]))
			# saves corrected values
			out_counts[i] = zero_counts[:, 1:]
			progress.emit(i)
	# return result
	return out_counts

def refcorrel(file: Path) -> DataFrame:
	return read_excel(file)

def domulticorrel(wsize: int, counts: ndarray, ref: DataFrame, progress: Signal) -> ndarray:
	# extra functions
	def meanmatrix(rows: int, full_matrix: ndarray):
		mean_ = zeros((rows, full_matrix.__len__()))
		for i, m in enumerate(full_matrix):
			mean_[:, i] = mean(m, 1)
		return mean_
	
	def onepearson(rows: int, m_matrix: ndarray, one_ref: Series):
		p  = zeros(rows)
		for i in range(rows):
			p[i], _ = pearsonr(m_matrix[i, :], one_ref)
		return p
	
	# main function
	pearson = zeros((wsize, ref.columns.__len__()))
	mean_matrix = meanmatrix(wsize, counts)
	# now, for each column in ref, we must calculate one pearson
	for i, r in enumerate(ref.columns):
		pearson[:, i] = onepearson(wsize, mean_matrix, ref[r])
		progress.emit(i)
	# calculates full_mean
	full_mean = mean(mean_matrix, 1)
	full_mean /= max(full_mean)
	# organizes return array
	return_array = array(([None]*3), dtype=object)
	return_array[0], return_array[1], return_array[2] = pearson, full_mean, zeros(wsize)
	return return_array