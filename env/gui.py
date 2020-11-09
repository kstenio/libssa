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

# Imports
from numpy import zeros
from numpy.random import random
from colorsys import hsv_to_rgb
from PySide2.QtCore import QFile, Qt
from PySide2 import QtWidgets, QtGui
from PySide2.QtUiTools import QUiLoader
from pyqtgraph import PlotWidget, setConfigOption
from pathlib import PosixPath

# Graph global configurations
setConfigOption('background', 'w')
setConfigOption('foreground', '#26004d')

# GUI class
class LIBSsaGUI(object):
	"""
	LIBSsa: GUI

	This is the main GUI class for LIBSsa.
	
	Every element here is loaded from libssa.ui file, and bound as class variables.
	With an object of this class, the main is able to control the entire gui.
	"""
	def __init__(self, uifile: str, logofile: str):
		# Loads main window
		try:
			self.mw = QtWidgets.QMainWindow()
			self.loadui(uifile)
		except Exception as err:
			raise ValueError('Could not initialize UI file. Error message:\n\t%s' % str(err))
		# If no error was found, loads all remaining widgets
		else:
			# Main tab element and logo
			self.sb = QtWidgets.QStatusBar()
			self.toolbox = QtWidgets.QToolBox()
			self.logo = QtWidgets.QLabel()
			self.mbox = QtWidgets.QMessageBox()
			self.mbox_pbar = QtWidgets.QProgressBar()
			# Graph elements
			self.g = PlotWidget()
			self.g_selector = QtWidgets.QComboBox()
			self.g_minus = self.g_plus = QtWidgets.QToolButton()
			self.g_displayed = QtWidgets.QSpinBox()
			self.g_max = self.g_run = QtWidgets.QLabel()
			# Page 1 == Load Spectra
			self.p1_smm = self.p1_sms = QtWidgets.QRadioButton()
			self.p1_fdtext = QtWidgets.QLineEdit()
			self.p1_fdbtn = QtWidgets.QToolButton()
			self.p1_delim = QtWidgets.QComboBox()
			self.p1_header = self.p1_wcol = self.p1_ccol = self.p1_dec = QtWidgets.QSpinBox()
			self.p1_ldspectra = QtWidgets.QPushButton()
			# Page 2 == Operations
			pass
			# loads all elements
			self.loadmain()
			self.loadp1()
			self.loadp2()
			self.loadp3()
			self.loadp4()
			self.loadp5()
			self.loadp6()
			# extra configs
			self.loadmain()
			self.loadstyle(logofile)
			self.configgraphic()
			# gui connects
			self.p1_sms.toggled.connect(self.modechanger)
			
	def loadui(self, uifile: str):
		uifile = QFile(uifile)
		if uifile.open(QFile.ReadOnly):
			loader = QUiLoader()
			# register PlotWidget (promoted in QtDesigner)
			loader.registerCustomWidget(PlotWidget)
			# loads QMainWindow
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
			color: #000000;}
		
		QToolBox::tab:selected {
			font: bold italic;
			background: #6600cc;
			color: #ffffff;}"""
		self.toolbox.setStyleSheet(style)
	
	# Load methods
	def loadmain(self):
		# main tab element and logo
		self.sb = self.mw.findChild(QtWidgets.QStatusBar, 'statusbar')
		self.toolbox = self.mw.findChild(QtWidgets.QToolBox, 'operationsMainToolBox')
		self.logo = self.mw.findChild(QtWidgets.QLabel, 'mainLogo')
		# elements from graph
		self.g = self.mw.findChild(PlotWidget, 'graph')
		self.g_selector = self.mw.findChild(QtWidgets.QComboBox, 'graphTypeCB')
		self.g_minus = self.mw.findChild(QtWidgets.QToolButton, 'graphMinus')
		self.g_plus = self.mw.findChild(QtWidgets.QToolButton, 'graphPlus')
		self.g_displayed = self.mw.findChild(QtWidgets.QSpinBox, 'graphIndex')
		self.g_max = self.mw.findChild(QtWidgets.QLabel, 'graphLabel3')
		self.g_run = self.mw.findChild(QtWidgets.QLabel, 'graphPlot')
	
	def loadp1(self):
		self.p1_smm = self.mw.findChild(QtWidgets.QRadioButton, 'p1rB1')
		self.p1_sms = self.mw.findChild(QtWidgets.QRadioButton, 'p1rB2')
		self.p1_fdtext = self.mw.findChild(QtWidgets.QLineEdit, 'p1lE1')
		self.p1_fdbtn = self.mw.findChild(QtWidgets.QToolButton, 'p1tB1')
		self.p1_delim = self.mw.findChild(QtWidgets.QComboBox, 'p1cB1')
		self.p1_header = self.mw.findChild(QtWidgets.QSpinBox, 'p1sB1')
		self.p1_wcol = self.mw.findChild(QtWidgets.QSpinBox, 'p1sB2')
		self.p1_ccol = self.mw.findChild(QtWidgets.QSpinBox, 'p1sB3')
		self.p1_dec = self.mw.findChild(QtWidgets.QSpinBox, 'p1sB4')
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
	
	# Connects helper
	def modechanger(self):
		is_single = self.p1_sms.isChecked()
		if is_single:
			self.p1_wcol.setEnabled(not is_single)
			self.p1_ccol.setEnabled(not is_single)
		else:
			self.p1_wcol.setEnabled(not is_single)
			self.p1_ccol.setEnabled(not is_single)
	
	# Graph methods
	def configgraphic(self):
		self.g.setTitle('LIBS Spectum')
		self.g.setLabel('left', 'Counts', units='a.u.')
		self.g.setLabel('bottom', 'Wavelength', units='nm')
		
	def splot(self, x, y):
		self.g.clear()
		self.g.plot(x, y)
		self.g.autoRange()
	
	def mplot(self, x, matrix):
		self.g.clear()
		smp = matrix.shape[1]
		colors = pretty_colours(smp)
		for i in range(smp):
			self.g.plot(x, matrix[:, i], pen=colors[i, :])
		self.g.autoRange()
		
	#
	# GUI/helper functions
	#
	def guimsg(self, top: str, main: str, tp: str):
		if tp.lower() in ('w', 'warning'):
			return QtWidgets.QMessageBox.warning(self.mw, top, main)
		elif tp.lower() in ('i', 'information'):
			return QtWidgets.QMessageBox.information(self.mw, top, main)
		elif tp.lower() in ('q', 'question'):
			return QtWidgets.QMessageBox.question(self.mw, top, main)
		elif tp.lower() in ('c', 'critical'):
			return QtWidgets.QMessageBox.critical(self.mw, top, main)
		else:
			QtWidgets.QMessageBox.critical(self.mw, 'Erro', 'Wrong MSG ID!')
			raise ValueError('Wrong MSG ID!')
	
	def guifd(self, parent: PosixPath, tp: str, st1: str, st2: str = ''):
		if tp in ('ged', 'getExistingDirectory'):
			return QtWidgets.QFileDialog.getExistingDirectory(self.mw, st1,
			                                        dir=parent.as_posix())
		else:
			QtWidgets.QMessageBox.critical(self.mw, 'Erro', 'Wrong FD ID!')
			raise ValueError('Wrong FD ID!')
	
	def dynamicbox(self, top: str, msg: str, maxi: int):
		self.mbox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, top, msg,
		                        QtWidgets.QMessageBox.NoButton)
		mbox_layout = self.mbox.layout()
		mbox_layout.itemAtPosition(mbox_layout.rowCount() - 1,
		                           0).widget().hide()
		self.mbox_pbar = QtWidgets.QProgressBar()
		self.mbox_pbar.setValue(0)
		self.mbox_pbar.setRange(0, maxi)
		mbox_layout.addWidget(self.mbox_pbar, mbox_layout.rowCount(), 0, 1, mbox_layout.columnCount(), Qt.AlignCenter)
		self.mbox.show()
	
	def updatedynamicbox(self, val, update=True, msg='Operation Finished'):
		if update:
			self.mbox_pbar.setValue(val)
		else:
			self.mbox_pbar.setValue(self.mbox_pbar.maximum())
			self.mbox.close()
			self.mbox = None
			changestatus(self.sb, msg, 'g', False)
			

# Extra functions
def pretty_colours(colors):
	"""uses golden ratio to create pleasant/pretty colours
	returns in rgb form"""
	output = zeros((colors, 3))
	golden_ratio_conjugate = (1 + (7**0.5)) / 2
	hue = random()
	for tmp in range(colors):
		hue += golden_ratio_conjugate * (tmp / (5 * random()))
		hue %= 1
		output[tmp, :] = [int(x * 256) for x in hsv_to_rgb(hue, 0.95, 0.75)]
	return output

def changestatus(bar, message='', color='', bold=False):
	if (message == '') and (color == ''):
		bar.clearMessage()
	else:
		if len(color) == 1:
			r, g, b, p, color = ['ff2266', '008000', '003cb3', 'cc00ff', color.lower()]
			if color == 'r':
				color = r
			elif color == 'g':
				color = g
			elif color == 'b':
				color = b
			elif color == 'p':
				color = p
			else:
				raise ValueError('Wrong color identifier. Use "r","g","b","p" or 6 hexadecimal values.')
		if len(color) == 6:
			bar.showMessage(message)
			if bold:
				bar.setStyleSheet('color:#%s;font-weight:bold' % color)
			else:
				bar.setStyleSheet('color:#%s' % color)
		else:
			raise ValueError('Wrong color length style. Please use 6 hexadecimal values.')