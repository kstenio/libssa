#!/usr/bin/env python3
#
# Copyright (c) 2024 Kleydson Stenio (9257942+kstenio@users.noreply.github.com).
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
from tempfile import mkdtemp

import numpy as np
import pandas as pd

from libssa.env.imports import load

# Global test variables
ROWS = 50
COLUMNS = 5
HEADER = 0
WAVE_COL = 1
COUNTS_COL = 2
SEP = ('\t', 'TAB')
DECIMAL = 3
WAVE_MIN = 100
WAVE_MAX = 1000


# Qt Signal mock class
class Signal: ...


class SignalMock(Signal):
	def __init__(self):
		super().__init__()
		self.signal = 0

	def emit(self, value: int):
		self.signal += value


# Basic mock functions
def counts_mock(load_mode: str):
	if load_mode == 'Single':
		return np.arange(ROWS).reshape(-1, 1) * np.ones((ROWS, COLUMNS))
	elif load_mode == 'Multiple':
		return np.arange(ROWS).reshape(-1, 1) * np.ones((ROWS, 1))
	else:
		raise AssertionError('Illegal value')


def spectrum_mock(load_mode: str):
	counts = counts_mock(load_mode)
	wavelength = np.linspace(WAVE_MIN, WAVE_MAX, ROWS)
	return np.column_stack((wavelength, counts))


def load_mock(load_mode: str):
	tempfolder, paths = Path(mkdtemp(prefix='libssa_', suffix='_test')), []
	if load_mode == 'Single':
		# Single folder containing the spectra
		# For the tests, this folder will have 3 files, each one with 6 columns:
		#   - 1st: wavelength
		#   - remaining: counts
		for file in ('A', 'B', 'C'):
			paths.append(tempfolder.joinpath(f'{file}.txt'))
			df = pd.DataFrame(spectrum_mock(load_mode), columns=['W'] + [f'Count_{x}' for x in range(COLUMNS)])
			df.to_csv(paths[-1], sep=SEP[0], index=False)
	elif load_mode == 'Multiple':
		# Multiple folders containing the spectra
		# For the tests, this folder will have 3 subfolders, each one with 5 files with two columns:
		#   - 1st: wavelength
		#   - 2nd: counts
		for folder in ('A', 'B', 'C'):
			tempfolder.joinpath(folder).mkdir()
			paths.append(tempfolder.joinpath(folder))
			for file in range(5):
				df = pd.DataFrame(spectrum_mock(load_mode), columns=['W', 'Count'])
				df.to_csv(paths[-1].joinpath(f'{file}.txt'), sep=SEP[0], index=False)
	return tuple(paths)


# Main test
def test_load():
	for mode in ('Single', 'Multiple'):
		# Creates files for mock
		folder = load_mock(mode)
		# Call load function
		wavelength, counts = load(
			folder=folder,
			mode=mode,
			delim=SEP[1],
			header=HEADER,
			wcol=WAVE_COL,
			ccol=COUNTS_COL,
			dec=DECIMAL,
			fsn=['Average', None, None],
			progress=SignalMock(),
		)
		# Clear folder/files used for mocking (the breakpoint below is useful to check folders before being deleted)
		# breakpoint()
		for f in folder:
			if f.is_file():
				f.unlink()
			else:
				files = listdir(f)
				for fi in [f.joinpath(x) for x in files]:
					if fi.is_file():
						fi.unlink()
				f.rmdir()
		else:
			f.parent.rmdir()
		# Check values
		counts_array = counts_mock('Single').round(DECIMAL)
		assert np.array_equal(wavelength, np.linspace(WAVE_MIN, WAVE_MAX, ROWS).round(DECIMAL))
		assert np.array_equal(counts[0], counts_array)
		assert np.array_equal(counts[1], counts_array)
		assert np.array_equal(counts[2], counts_array)
