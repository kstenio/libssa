#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  libssa.py
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
import numpy as np

class Spectra(object):
    """
    LIBSsa: Spectra

    Class for store and organize entire LIBSsa environment.
    """
    def __init__(self):
        self.wavelength = np.array(([None]), dtype=object)
        self.wavelength_iso  = np.array(([None]), dtype=object)
        self.counts = np.array(([None]), dtype=object)
        self.counts_iso = np.array(([None]), dtype=object)
        self.counts_out = np.array(([None]), dtype=object)
        self.pearson = np.array(([None]), dtype=object)