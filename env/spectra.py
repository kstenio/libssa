#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  spectra.py
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
from numpy import array

class Spectra(object):
	"""
	LIBSsa: Spectra
	
	Class for store and organize entire LIBSsa environment.
	"""
	def __init__(self):
		self.wavelength = array(([None]), dtype=object)
		self.wavelength_iso  = array(([None]), dtype=object)
		self.counts = array(([None]), dtype=object)
		self.counts_iso = array(([None]), dtype=object)
		self.counts_out = array(([None]), dtype=object)
		self.pearson_ref = array(([None]), dtype=object)
		self.pearson = array(([None]), dtype=object)
		self.pca = array(([None]), dtype=object)
		self.pls = array(([None]), dtype=object)
		self.linear = array(([None]), dtype=object)
		self.temperature = array(([None]), dtype=object)
		self.nsamples = 0
		self.samples = [None]
		self.samples_path = [None]