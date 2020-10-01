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
from PySide2 import QtWidgets
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


# gui class
class LIBSsaGUI(object):
	"""
	This is the main GUI class for LIBSsa.
	
	Every element here is loaded from libssa.ui file, and bound as class variables.
	With an object of this class, the main is able to control the entire gui.
	"""
	def __init__(self, uifile: str):
		# loads main window
		try:
			self.mw = self.loadui(uifile)
		except Exception as err:
			raise ValueError('Could not initialize UI file. Error message:\n\t%s' % str(err))
		# if no error was fount, loads all remaining widgets
		else:
			# elements from graph
			self.g_plot = self.mw.findChild(QtWidgets.QLineEdit, 'graphWindow')
			self.g_selector = self.mw.findChild(QtWidgets.QComboBox, 'graphTypeCB')
			self.g_minus = self.mw.findChild(QtWidgets.QToolButton, 'graphMinus')
			self.g_plus = self.mw.findChild(QtWidgets.QToolButton, 'graphPlus')
			self.g_displayed = self.mw.findChild(QtWidgets.QSpinBox, 'graphIndex')
			self.g_max = self.mw.findChild(QtWidgets.QLabel, 'graphLabel3')
			self.g_run = self.mw.findChild(QtWidgets.QLabel, 'graphPlot')
	
	def loadui(self, uifile: str):
		uifile = QFile(uifile)
		if uifile.open(QFile.ReadOnly):
			loader = QUiLoader()
			window = loader.load(uifile)
			uifile.close()
			return window
