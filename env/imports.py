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
from os import listdir
from pathlib import Path
from numpy.linalg import norm
from scipy.stats import pearsonr
from PySide6.QtCore import Signal
from pandas import read_csv, read_excel, DataFrame, Series
from numpy import array, array_equal, ndarray, column_stack, mean, dot, zeros, median, abs as nabs, subtract, trapz


def load(folder: tuple, mode: str, delim: str, header: int, wcol: int, ccol: int, dec: int, fsn: list, progress: Signal) -> tuple:
	"""
	This method loads spectra and returns global variables wavelength and counts.

	:param folder: tuple of Paths of input folder/files (sorted)
	:param mode: file reading mode. 'Single' for one file per sample, or 'Multiple' for one folder per sample, multiple files per shoot
	:param delim: delimiter (space, tab, comma and semicolon)
	:param header: rows to skip in the spectra files
	:param wcol: which column is wavelength
	:param ccol: which column is counts
	:param dec: decimals values for round
	:param fsn: values for Full Spectrum Normalization
	:param progress: PySide Signal object (for multithreading)
	:return: wavelength and counts arrays
	"""
	# Organizes delimiter
	if delim == 'TAB':
		delim = '\t'
	elif delim == 'SPACE':
		delim = '\s+'
	# Creates wavelength and counts vectors
	wavelength, counts, count, sort = array(([None])), array(([None]*len(folder)), dtype=object), None, False
	if mode == "Single":
		# Reads all files
		for i, file in enumerate(folder):
			if i == 0:
				matrix = read_csv(file, delimiter=delim, skiprows=header).to_numpy(dtype=float).round(dec)
				wavelength, counts[i] = matrix[:, 0], matrix[:, 1:]
				if not array_equal(wavelength, wavelength[wavelength.argsort()]):
					sort = True
					counts[i] = counts[i][wavelength.argsort()]
			else:
				# After reading wavelength and defining if sort is needed, reads counts
				counts[i] = read_csv(file, delimiter=delim, skiprows=header).to_numpy(dtype=float).round(dec)[:, 1:]
				if sort:
					counts[i] = counts[i][wavelength.argsort()]
			# Checks if FSN is needed
			if fsn[0] is None:
				pass
			else:
				if fsn[0] == 'Area':
					counts[i] /= trapz(counts[i], axis=0)
				elif fsn[0] == 'Norm':
					counts[i] /= norm(counts[i], axis=0)
				elif fsn[0] == 'Max. Value':
					counts[i] /= counts[i].max(axis=0)
				elif fsn[0] == 'IS':
					w = wavelength[wavelength.argsort()]
					is_idx = (w >= fsn[1]) & (w <= fsn[2])
					is_cut = counts[i][is_idx, :]
					counts[i] /= is_cut.max(axis=0)
			# Emits signal for GUI
			progress.emit(i+1)
		# By the end - if needed - sorts wavelength
		if sort:
			wavelength.sort()
		# Return values
		return wavelength, counts
	elif mode == "Multiple":
		# Reads all files in each folder
		for j, folders in enumerate(folder):
			files = listdir(folders)
			files.sort()
			files = [folders.joinpath(x) for x in files]
			for k, spectrum in enumerate(files):
				# Reads wavelength
				if (j == 0) and (k == 0):
					wavelength = read_csv(spectrum, usecols=[wcol-1], delimiter=delim, skiprows=header).to_numpy(dtype=float).round(dec).T[0]
					if not array_equal(wavelength, wavelength[wavelength.argsort()]):
						sort = True
				# Reads counts
				if k == 0:
					count = read_csv(spectrum, usecols=[ccol-1], delimiter=delim, skiprows=header).to_numpy(dtype=float).round(dec)
				else:
					count = column_stack((count, read_csv(spectrum, usecols=[ccol-1], delimiter=delim, skiprows=header).to_numpy(dtype=float).round(dec)))
			# Back in j loop, save count in counts vector and sort if needed
			counts[j] = count
			if sort:
				counts[j] = counts[j][wavelength.argsort()]
			# Checks if FSN is needed
			if fsn[0] is None:
				pass
			else:
				if fsn[0] == 'Area':
					counts[j] /= trapz(counts[j], axis=0)
				elif fsn[0] == 'Norm':
					counts[j] /= norm(counts[j], axis=0)
				elif fsn[0] == 'Max. Value':
					counts[j] /= counts[j].max(axis=0)
				elif fsn[0] == 'IS':
					w = wavelength[wavelength.argsort()]
					is_idx = (w >= fsn[1]) & (w <= fsn[2])
					is_cut = counts[j][is_idx, :]
					counts[j] /= is_cut.max(axis=0)
			# Emits signal for GUI
			progress.emit(j + 1)
		# By the end - if needed - sorts wavelength
		if sort:
			wavelength.sort()
		# Return values
		return wavelength, counts
	else:
		raise ValueError('Wrong reading mode.')


def outliers(mode: str, criteria: float, counts: dict, progress: Signal) -> tuple:
	"""
	Function to perform outliers removal for spectra.
	
	:param mode: operation mode, SAM (Spectral Angle Mapper) or MAD (median Absolute Deviation)
	:param criteria: criteria for exclusion (0:1 for SAM, 2:2.5:3 for MAD)
	:param counts: full Spectra object with intensities for sample set
	:param progress: PySide Signal object (for multithreading)
	:return: retults of exclusion (out_counts and removed_report)
	"""
	# Creates counts new vector
	out_counts = array(([None] * counts['Count']), dtype=object)
	removed_report = []
	if mode == 'SAM':
		for i in range(counts['Count']):
			out_average = mean(counts['Raw'][i], 1)
			out_counts[i] = out_average
			removed = [0, counts['Raw'][i].shape[1]]
			for j in range(counts['Raw'][i].shape[1]):
				costheta = dot(out_average, counts['Raw'][i][:, j]) / ( norm(out_average)*norm(counts['Raw'][i][:, j]) )
				if costheta >= criteria:
					out_counts[i] = column_stack((out_counts[i], counts['Raw'][i][:, j]))
				else:
					removed[0] += 1
			try:
				out_counts[i] = out_counts[i][:, 1:]
			except IndexError:
				raise AttributeError('Too little shoots for outliers removal')
			removed_report.append(removed)
			progress.emit(i)
	elif mode == 'MAD':
		b = 1.4826
		for i in range(counts['Count']):
			# Calculates MAD for each wavelength
			ith_median = median(counts['Raw'][i], 1)
			ith_mad_vector = b * median(nabs(subtract(counts['Raw'][i].T, ith_median).T), 1)
			# Now, check if each shoot is or isn't an outlier
			zero_counts = zeros(counts['Raw'][i].shape[0])
			bool_checker = array([criteria] * counts['Raw'][i].shape[0])
			removed = [0, counts['Raw'][i].shape[1]]
			for k in range(counts['Raw'][i].shape[1]):
				criteria_ = (counts['Raw'][i][:, k] - ith_median) / ith_mad_vector
				criteria_bool = nabs(criteria_) < bool_checker
				if criteria_bool.sum() / counts['Raw'][i].shape[0] >= 0.95:
					zero_counts = column_stack((zero_counts, counts['Raw'][i][:, k]))
				else:
					removed[0] += 1
			# Saves corrected values
			try:
				out_counts[i] = zero_counts[:, 1:]
			except IndexError:
				raise AttributeError('Too little shoots for outliers removal')
			removed_report.append(removed)
			progress.emit(i)
	# Return result
	return out_counts, array(removed_report)


def refcorrel(file: Path) -> DataFrame:
	"""
	Convenient function to read references. For now, does little, but I'll add some checkups later...
	
	:param file: path of file of reference (xls, xlsx)
	:return: dataframe after the loading
	"""
	return read_excel(file, index_col=0, engine='openpyxl')


def domulticorrel(wsize: int, counts: ndarray, ref: DataFrame, progress: Signal) -> ndarray:
	"""
	Function that calculates bitwise Pearson correlation
	
	:param wsize: size of wavelength
	:param counts: intensities for every sample
	:param ref: values of reference (each element in a column)
	:param progress: PySide Signal object (for multithreading)
	:return: object array containing Pearson, zeros and mean of sample set (I'll change this to a proper 3D array later...)
	"""
	# Extra functions
	def meanmatrix(rows: int, full_matrix: ndarray):
		mean_ = zeros((rows, full_matrix.__len__()))
		for i, m in enumerate(full_matrix):
			mean_[:, i] = mean(m, 1)
		return mean_
	
	def onepearson(rows: int, m_matrix: ndarray, one_ref: Series):
		p = zeros(rows)
		for ip in range(rows):
			p[ip], _ = pearsonr(m_matrix[ip, :], one_ref)
		return p
	
	# Main function
	pearson = zeros((wsize, ref.columns.__len__()))
	mean_matrix = meanmatrix(wsize, counts)
	# Now, for each column in ref, we must calculate one pearson
	for i, r in enumerate(ref.columns):
		pearson[:, i] = onepearson(wsize, mean_matrix, ref[r])
		progress.emit(i)
	# Calculates full_mean
	full_mean = mean(mean_matrix, 1)
	full_mean /= max(full_mean)
	# Organizes return array
	return_array = array(([None]*3), dtype=object)
	return_array[0], return_array[1], return_array[2] = pearson, full_mean, zeros(wsize)
	return return_array
