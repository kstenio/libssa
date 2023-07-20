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
from numpy import array
from pathlib import Path
from pandas import DataFrame
from traceback import print_exc
from PySide6.QtCore import QObject, QRunnable, Signal, Slot


# Signals for Qt worker
class WorkerSignals(QObject):
	def __init__(self):
		super(WorkerSignals, self).__init__()
	# Types of signals for LIBSsa
	progress = Signal(int)
	error = Signal(tuple)
	result = Signal(object)
	finished = Signal()


# Main QThreadPool worker
class Worker(QRunnable):
	def __init__(self, fn, *args, **kwargs):
		super(Worker, self).__init__()
		# Base args
		self.fn = fn
		self.args = args
		self.kwargs = kwargs
		self.signals = WorkerSignals()
		# Adds callback (progress) to kwargs
		self.kwargs['progress'] = self.signals.progress
	
	@Slot(name='run')
	def run(self):
		try:
			# Normal run of function
			result = self.fn(*self.args, **self.kwargs)
		except Exception as ex:
			# Return error message as signal
			print(f'An error of type {type(ex).__name__} occurred.\nMSG: {ex}\n')
			print_exc()
			self.signals.error.emit((type(ex).__name__, str(ex)))
		else:
			# Returns result of functions
			self.signals.result.emit(result)
		finally:
			# Sends finished signal
			self.signals.finished.emit()


# LIBSsa main spectra class
class Spectra(object):
	"""
	LIBSsa: Spectra
	
	Class for storing and organizing entire LIBSsa environment.
	
	It is divided in:
		* properties = size, sample names and file
		* base data = wavelengths and counts/intensities
		* references = values for correlation and models
		* models = values that store models properties and predictions
		* plasma information = for temperature and plasma density
	"""
	# Base element
	base = array([None], dtype=object)
	
	def __init__(self):
		# Sample set and properties
		self.samples = {'Count': 0, 'Name': tuple([None]), 'Path': tuple([Path()])}
		# Base spectra elements: Wavelengths and Counts
		self.wavelength = {'Raw': self.base, 'Isolated': self.base}
		self.intensities = {'Count': 0, 'Raw': self.base, 'Outliers': self.base, 'Removed': self.base, 'Isolated': self.base}
		# References and correlation
		self.ref = DataFrame({'Empty': [0]})
		self.pearson = {'Data': self.base, 'Full-Mean': self.base, 'Zeros': self.base}
		# Results from isolation and peak fitting
		self.isolated = {'Count': 0, 'NSamples': 0, 'Element': self.base,
		                 'Center': self.base, 'Upper': self.base, 'Lower': self.base,
						 'Noise': self.base, 'Table': DataFrame()}
		self.fit = {'Area': self.base, 'AreaSTD': self.base, 'Width': self.base, 'Height': self.base,
		            'Shape': self.base, 'NFev': self.base, 'Convergence': self.base,
		            'Data': self.base, 'Total': self.base}
		# Models
		self.linear = {'Reference': self.base, 'Predict': self.base,
					   'R2': self.base, 'RMSE': self.base,
					   'Slope': self.base, 'Intercept': self.base,
					   'LoD': self.base, 'LoQ': self.base, 'Element': ''}
		self.pca = {'Mode': None, 'OptComp': 0, 'ExpVar': self.base,
		            'Attributes': self.base, 'Transformed': self.base, 'Loadings': self.base}
		self.pls = {'Element': self.base, 'Model': self.base, 'NComps': 0, 'Samples': self.base,
		            'Reference': self.base, 'Predict': self.base, 'Residual': self.base, 'Att': '',
		            'PredictR2': self.base, 'PredictRMSE': self.base, 'CrossValPredict': self.base,
		            'CrossValR2': self.base, 'CrossValRMSE': self.base, 'BlindPredict': self.base}
		# Plasma properties
		self.plasma = {'Ln': self.base, 'En': self.base, 'Fit': self.base, 'Report': self.base,
		               'Tables': self.base, 'Element': '', 'Parameter': ''}
	
	def clear(self):
		"""
		clear method. Totally clear an object, except pls if previous calculated
		(for blind predictions)
		
		:return: None
		"""
		pls = self.pls.copy()
		self.__init__()
		if pls['Model'] != self.base:
			self.pls = pls
