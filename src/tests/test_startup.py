#!/usr/bin/env python3
#
# Copyright (c) 2023 Florian Dobener <florian.dobener@physik.hu-berlin.de> [@domna]
#               2024 Kleydson Stenio (9257942+kstenio@users.noreply.github.com) [@kstenio]
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
"""
A basic test to see if the gui starts up properly
"""

# Imports
from pathlib import Path

import libssa.libssa2 as libssa


def test_startup(qtbot):
	"""
	Test if the gui starts up
	"""
	root = Path(__file__).parents[1]
	uif = root.joinpath('libssa', 'env', 'gui', 'libssagui.ui')
	lof = root.joinpath('libssa', 'pic', 'libssa.svg')
	app = libssa.LIBSSA2(uif, lof)
	qtbot.addWidget(app)
