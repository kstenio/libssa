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
from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd
from PySide6.QtWidgets import QTableWidgetItem
from pytestqt.qt_compat import qt_api

import libssa.libssa2 as libssa
from libssa.env.export import export_fit_areas

# Global variables
PREVIOUSLY_OBTAINED_AREA_SUM = 99.91516644755093


# Helper functions
def check_array(array):
	try:
		assert array.size > 1
	except AttributeError:
		assert array[0].size > 1


# Main test
def test_export_areas(qtbot):
	# Run app/loads main window into qbot
	root = Path(__file__).parents[1]
	uif = root.joinpath('libssa', 'env', 'gui', 'libssagui.ui')
	lof = root.joinpath('libssa', 'pic', 'libssa.svg')
	app = libssa.LIBSSA2(uif, lof)
	gui = app.gui
	qtbot.addWidget(app)
	# 1. Import basic sample data
	gui.menu_file_sample.trigger()  # OR app.loadsample_spectra()
	qtbot.waitUntil(lambda: check_array(app.spec.wavelength['Raw']))
	# 2. Move to tab 2 (Outliers), choose MAD (default == 3) and apply Outliers removal
	gui.toolbox.setCurrentIndex(1)
	gui.p2_mad.toggle()
	gui.p2_apply_out.click()
	qtbot.waitUntil(lambda: check_array(app.spec.intensities['Outliers']))
	# 3. Move to tab 3 (Regions and Peak Fitting) and fill isolation table
	gui.toolbox.setCurrentIndex(2)
	gui.p3_isoadd.click()
	for i, val in enumerate(('C247', '246.2', '248.2', '247.2')):
		gui.p3_isotb.setItem(0, i, QTableWidgetItem(val))
	# 4. Performs iso peak
	gui.p3_isoapply.click()  # OR app.peakiso()
	qtbot.waitUntil(lambda: check_array(app.spec.intensities['Isolated']))
	# 5. Performs peakfit
	gui.p3_default_shape.setValue(10)
	gui.p3_fitapply.click()  # OR app.peakfit()
	qtbot.waitUntil(lambda: check_array(app.spec.fit['Data']))
	# 6. Saves area report and check if Area SUM is as previously calculated
	with NamedTemporaryFile(suffix='.xlsx') as temp:
		# Export
		export_fit_areas(Path(temp.name), app.spec)
		# Read
		df = pd.read_excel(Path(temp.name))
	assert df['Area_Peak_1'].sum() == PREVIOUSLY_OBTAINED_AREA_SUM
