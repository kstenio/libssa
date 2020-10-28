#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  gui.py
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
from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


# gui class
class LIBSsaGUI(object):
	"""
	LIBSsa: GUI

	This is the main GUI class for LIBSsa.
	
	Every element here is loaded from libssa.ui file, and bound as class variables.
	With an object of this class, the main is able to control the entire gui.
	"""
	def __init__(self, uifile: str, logofile: str):
		# loads main window
		try:
			self.mw = QtWidgets.QMainWindow()
			self.loadui(uifile)
		except Exception as err:
			raise ValueError('Could not initialize UI file. Error message:\n\t%s' % str(err))
		# if no error was fount, loads all remaining widgets
		else:
			# main tab element and logo
			self.sb = self.mw.findChild(QtWidgets.QStatusBar, 'statusbar')
			self.toolbox = self.mw.findChild(QtWidgets.QToolBox, 'operationsMainToolBox')
			self.logo = self.mw.findChild(QtWidgets.QLabel, 'mainLogo')
			self.loadstyle(logofile)
			# elements from graph
			self.g_plot = self.mw.findChild(QtWidgets.QLineEdit, 'graphWindow')
			self.g_selector = self.mw.findChild(QtWidgets.QComboBox, 'graphTypeCB')
			self.g_minus = self.mw.findChild(QtWidgets.QToolButton, 'graphMinus')
			self.g_plus = self.mw.findChild(QtWidgets.QToolButton, 'graphPlus')
			self.g_displayed = self.mw.findChild(QtWidgets.QSpinBox, 'graphIndex')
			self.g_max = self.mw.findChild(QtWidgets.QLabel, 'graphLabel3')
			self.g_run = self.mw.findChild(QtWidgets.QLabel, 'graphPlot')
			# page 1 == Load Spectra
			self.p1_smm = self.p1_sms = QtWidgets.QRadioButton()
			self.p1_fdtext = QtWidgets.QLineEdit()
			self.p1_fdbtn = QtWidgets.QToolButton()
			self.p1_delim = QtWidgets.QComboBox()
			self.p1_header = self.p1_wcol = self.p1_ccol = QtWidgets.QSpinBox()
			self.p1_ldspectra = QtWidgets.QPushButton()
			# page 2 == Operations
			pass
			# loads all elements
			self.loadp1()
			self.loadp2()
			self.loadp3()
			self.loadp4()
			self.loadp5()
			self.loadp6()
			
			
	def loadui(self, uifile: str):
		uifile = QFile(uifile)
		if uifile.open(QFile.ReadOnly):
			loader = QUiLoader()
			window = loader.load(uifile)
			uifile.close()
			self.mw = window
		else:
			raise FileNotFoundError('Could not load UI file.')

	def loadstyle(self, logofile):
		try:
			logo = QtGui.QPixmap(logofile)
			self.logo.setPixmap(logo)
		except Exception as err:
			print(err)
		style = """
		QToolBox::tab {
			background: qlineargradient(x1: 0, x2: 1, stop: 0 #cc99ff, stop: 1.0 transparent);
			border-radius: 2px;
			color: #000000;
		}
		
		QToolBox::tab:selected {
			font: bold italic;
			background: #6600cc;
			color: #ffffff;
		}"""
		self.toolbox.setStyleSheet(style)
		
	def loadp1(self):
		self.p1_smm = self.mw.findChild(QtWidgets.QRadioButton, 'p1rB1')
		self.p1_sms = self.mw.findChild(QtWidgets.QRadioButton, 'p1rB2')
		self.p1_fdtext = self.mw.findChild(QtWidgets.QLineEdit, 'p1lE1')
		self.p1_fdbtn = self.mw.findChild(QtWidgets.QToolButton, 'p1tB1')
		self.p1_delim = self.mw.findChild(QtWidgets.QComboBox, 'p1cB1')
		self.p1_header = self.mw.findChild(QtWidgets.QSpinBox, 'p1sB1')
		self.p1_wcol = self.mw.findChild(QtWidgets.QSpinBox, 'p1sB2')
		self.p1_ccol = self.mw.findChild(QtWidgets.QSpinBox, 'p1sB3')
		self.p1_ldspectra = self.mw.findChild(QtWidgets.QPushButton, 'p1pB1')
	
	def loadp2(self):
		pass
	
	def loadp3(self):
		pass
	
	def loadp4(self):
		pass
	
	def loadp5(self):
		pass
	
	def loadp6(self):
		pass
