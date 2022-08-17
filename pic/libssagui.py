#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  ./pic/libssagui.py
#
#  Copyright 2021 Kleydson Stenio <kleydson.stenio@gmail.com>
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
from numpy import zeros, int16, ones, ndarray, std, linspace, arange, hstack
from pandas import DataFrame
from numpy.random import randint, uniform, random, rand
from colorsys import hsv_to_rgb, hls_to_rgb
from PySide6.QtCore import QFile, Qt
from PySide6 import QtWidgets, QtGui
from PySide6.QtUiTools import QUiLoader
from pyqtgraph import PlotWidget, setConfigOption, mkBrush, mkPen, TextItem, BarGraphItem
from pathlib import Path
from string import punctuation

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
			self.logofile = logofile
			self.peaknormitems = []
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
			# Menubar
			self.menu_import_ref = QtGui.QAction()
			self.menu_export_fullspectra_raw = self.menu_export_fullspectra_out = QtGui.QAction()
			self.menu_export_peaks_table = self.menu_export_peaks_isolated = self.menu_export_peaks_fitted = self.menu_export_peaks_areas = QtGui.QAction()
			self.menu_export_predictions_linear = self.menu_export_predictions_pls = QtGui.QAction()
			self.menu_export_other_pca = self.menu_export_other_tne = self.menu_export_other_correl = QtGui.QAction()
			# Graph elements
			self.g = PlotWidget()
			self.g_selector = QtWidgets.QComboBox()
			self.g_minus = self.g_plus = self.g_run = QtWidgets.QToolButton()
			self.g_current_sb = self.g_displayed = QtWidgets.QSpinBox()
			self.g_max = QtWidgets.QLabel()
			self.g_current = ''
			self.g_op = ['Wavelenght', 'nm', 'Counts', 'a.u.']
			self.g_legend = None
			# Page 1 == Load Spectra
			self.p1_smm = self.p1_sms = QtWidgets.QRadioButton()
			self.p1_fdtext = QtWidgets.QLineEdit()
			self.p1_fdbtn = QtWidgets.QToolButton()
			self.p1_delim = self.p1_fsn_type = QtWidgets.QComboBox()
			self.p1_header = self.p1_wcol = self.p1_ccol = self.p1_dec = QtWidgets.QSpinBox()
			self.p1_ldspectra = QtWidgets.QPushButton()
			self.p1_fsn_check = QtWidgets.QCheckBox()
			self.p1_fsn_labelminus = self.p1_fsn_labelplus = QtWidgets.QLabel()
			self.p1_fsn_lminus = self.p1_fsn_lplus = QtWidgets.QDoubleSpinBox()
			
			# Page 2 == Operations
			self.p2_dot = self.p2_mad = QtWidgets.QRadioButton()
			self.p2_dot_c = self.p2_mad_c = QtWidgets.QDoubleSpinBox()
			self.p2_apply_out = self.p2_apply_correl = QtWidgets.QToolButton()
			self.p2_correl_lb = QtWidgets.QLabel()
			# Page 3 == Peaks
			self.p3_isotb = self.p3_fittb = QtWidgets.QTableWidget()
			self.p3_isoadd = self.p3_isorem = self.p3_isoapply = self.p3_fitapply = QtWidgets.QToolButton()
			self.p3_linear = self.p3_norm = QtWidgets.QCheckBox()
			self.p3_mean1st = QtWidgets.QRadioButton()
			# Page 4 == Calibration curve
			self.p4_peak = self.p4_ref = self.p4_pnorm_combo = QtWidgets.QComboBox()
			self.p4_areas = self.p4_heights = self.p4_wnorm = self.p4_pnorm = self.p4_anorm = self.p4_epeak = QtWidgets.QRadioButton()
			self.p4_apply = QtWidgets.QPushButton()
			self.p4_npeak = self.p4_npeak_norm = QtWidgets.QSpinBox()
			# Page 5 == PCA and PLSR
			self.p5_pca_raw = self.p5_pca_iso = self.p5_pca_areas = self.p5_pca_heights = QtWidgets.QRadioButton()
			self.p5_pca_fs = QtWidgets.QCheckBox()
			self.p5_pca_ncomps = QtWidgets.QSpinBox()
			self.p5_pca_cscan = self.p5_pca_do = self.p5_pls_cal_start = self.p5_pls_pred_start = QtWidgets.QPushButton()
			self.p5_pls_cal_att = self.p5_pls_pred_model = self.p5_pls_pred_att = QtWidgets.QLabel()
			self.p5_pls_cal_ref = QtWidgets.QComboBox()
			# loads all elements
			self.loadmain()
			self.loadp1()
			self.loadp2()
			self.loadp3()
			self.loadp4()
			self.loadp5()
			self.loadp6()
			# extra configs and connects
			self.loadconfigs()
			self.connects()
			
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
	def loadconfigs(self):
		self.g.setTitle('LIBS Spectum')
		self.g_legend = self.g.addLegend()
		self.loadstyle(self.logofile)
		self.setgoptions()
		self.modechanger()
		
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
		self.g_current_sb = self.mw.findChild(QtWidgets.QSpinBox, 'graphIndex')
		self.g_max = self.mw.findChild(QtWidgets.QLabel, 'graphLabel3')
		self.g_run = self.mw.findChild(QtWidgets.QToolButton, 'graphPlot')
		# menu
		self.menu_import_ref = self.mw.findChild(QtGui.QAction, 'actionI01')
		self.menu_export_fullspectra_raw = self.mw.findChild(QtGui.QAction, 'actionE01')
		self.menu_export_fullspectra_out = self.mw.findChild(QtGui.QAction, 'actionE02')
		self.menu_export_peaks_table = self.mw.findChild(QtGui.QAction, 'actionE03')
		self.menu_export_peaks_isolated = self.mw.findChild(QtGui.QAction, 'actionE04')
		self.menu_export_peaks_fitted = self.mw.findChild(QtGui.QAction, 'actionE05')
		self.menu_export_peaks_areas = self.mw.findChild(QtGui.QAction, 'actionE06')
		self.menu_export_predictions_linear = self.mw.findChild(QtGui.QAction, 'actionE07')
		self.menu_export_predictions_pls = self.mw.findChild(QtGui.QAction, 'actionE08')
		self.menu_export_other_pca = self.mw.findChild(QtGui.QAction, 'actionE09')
		self.menu_export_other_tne = self.mw.findChild(QtGui.QAction, 'actionE10')
		self.menu_export_other_correl = self.mw.findChild(QtGui.QAction, 'actionE11')
		# self.menu_export_
		
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
		self.p1_fsn_check = self.mw.findChild(QtWidgets.QCheckBox, 'p1cBox1')
		self.p1_fsn_type = self.mw.findChild(QtWidgets.QComboBox, 'p1cB2')
		self.p1_fsn_labelminus = self.mw.findChild(QtWidgets.QLabel, 'p1lB8')
		self.p1_fsn_labelplus = self.mw.findChild(QtWidgets.QLabel, 'p1lB9')
		self.p1_fsn_lminus = self.mw.findChild(QtWidgets.QDoubleSpinBox, 'p1dsB1')
		self.p1_fsn_lplus = self.mw.findChild(QtWidgets.QDoubleSpinBox, 'p1dsB2')
		
	def loadp2(self):
		self.p2_dot = self.mw.findChild(QtWidgets.QRadioButton, 'p2rB1')
		self.p2_mad = self.mw.findChild(QtWidgets.QRadioButton, 'p2rB1')
		self.p2_dot_c = self.mw.findChild(QtWidgets.QDoubleSpinBox, 'p2dSb1')
		self.p2_mad_c = self.mw.findChild(QtWidgets.QDoubleSpinBox, 'p2dSb2')
		self.p2_apply_out = self.mw.findChild(QtWidgets.QToolButton, 'p2tB1')
		self.p2_apply_correl =  self.mw.findChild(QtWidgets.QToolButton, 'p2tB2')
		self.p2_correl_lb = self.mw.findChild(QtWidgets.QLabel, 'p2lB4')
		
	def loadp3(self):
		self.p3_isotb = self.mw.findChild(QtWidgets.QTableWidget, 'p3tW1')
		self.p3_isoadd = self.mw.findChild(QtWidgets.QToolButton, 'p3tB1')
		self.p3_isorem = self.mw.findChild(QtWidgets.QToolButton, 'p3tB2')
		self.p3_isoapply = self.mw.findChild(QtWidgets.QToolButton, 'p3tB3')
		self.p3_fittb = self.mw.findChild(QtWidgets.QTableWidget, 'p3tW2')
		self.p3_fitapply = self.mw.findChild(QtWidgets.QToolButton, 'p3tB4')
		self.p3_linear = self.mw.findChild(QtWidgets.QCheckBox, 'p3cBox1')
		self.p3_norm = self.mw.findChild(QtWidgets.QCheckBox, 'p3cBox2')
		self.p3_mean1st = self.mw.findChild(QtWidgets.QRadioButton, 'p3rB1')
		
	def loadp4(self):
		self.p4_peak = self.mw.findChild(QtWidgets.QComboBox, 'p4cB1')
		self.p4_npeak = self.mw.findChild(QtWidgets.QSpinBox, 'p4sB1')
		self.p4_npeak_norm = self.mw.findChild(QtWidgets.QSpinBox, 'p4sB2')
		self.p4_ref = self.mw.findChild(QtWidgets.QComboBox, 'p4cB2')
		self.p4_areas = self.mw.findChild(QtWidgets.QRadioButton, 'p4rB1')
		self.p4_heights = self.mw.findChild(QtWidgets.QRadioButton, 'p4rB2')
		self.p4_wnorm = self.mw.findChild(QtWidgets.QRadioButton, 'p4rB3')
		self.p4_pnorm = self.mw.findChild(QtWidgets.QRadioButton, 'p4rB4')
		self.p4_pnorm_combo = self.mw.findChild(QtWidgets.QComboBox, 'p4cB3')
		self.p4_anorm = self.mw.findChild(QtWidgets.QRadioButton, 'p4rB5')
		self.p4_epeak = self.mw.findChild(QtWidgets.QRadioButton, 'p4rB6')
		self.p4_apply = self.mw.findChild(QtWidgets.QPushButton, 'p4pB1')
	
	def loadp5(self):
		self.p5_pca_raw = self.mw.findChild(QtWidgets.QRadioButton, 'p5rB1')
		self.p5_pca_iso = self.mw.findChild(QtWidgets.QRadioButton, 'p5rB2')
		self.p5_pca_areas = self.mw.findChild(QtWidgets.QRadioButton, 'p5rB3')
		self.p5_pca_heights = self.mw.findChild(QtWidgets.QRadioButton, 'p5rB4')
		self.p5_pca_fs = self.mw.findChild(QtWidgets.QCheckBox, 'p5cBox1')
		self.p5_pca_cscan = self.mw.findChild(QtWidgets.QPushButton, 'p5pB1')
		self.p5_pca_ncomps = self.mw.findChild(QtWidgets.QSpinBox, 'p5sB1')
		self.p5_pca_do = self.mw.findChild(QtWidgets.QPushButton, 'p5pB2')
		self.p5_pls_cal_att = self.mw.findChild(QtWidgets.QLabel, 'p5lB7')
		self.p5_pls_cal_ref = self.mw.findChild(QtWidgets.QComboBox, 'p5cB1')
		self.p5_pls_cal_start = self.mw.findChild(QtWidgets.QPushButton, 'p5pB3')
		self.p5_pls_pred_model = self.mw.findChild(QtWidgets.QLabel, 'p5lB11')
		self.p5_pls_pred_att = self.mw.findChild(QtWidgets.QLabel, 'p5lB13')
		self.p5_pls_pred_start = self.mw.findChild(QtWidgets.QPushButton, 'p5pB4')
		
	def loadp6(self):
		pass
	
	# Connects helper
	def connects(self):
		# connects
		self.g_selector.currentIndexChanged.connect(self.setgoptions)
		# p1
		self.p1_sms.toggled.connect(self.modechanger)
		self.p1_fsn_check.stateChanged.connect(lambda: self.config_fsn(0))
		self.p1_fsn_type.currentIndexChanged.connect(lambda: self.config_fsn(1))
		self.p1_fsn_lminus.valueChanged.connect(lambda: self.config_fsn(2))
		self.p1_fsn_lplus.valueChanged.connect(lambda: self.config_fsn(3))
		# p2
		self.p2_dot.toggled.connect(self.setoutliers)
		# p3
		self.p3_isoadd.clicked.connect(lambda: self.changetable(True))
		self.p3_isorem.clicked.connect(lambda: self.changetable(False))
		self.p3_isotb.cellChanged.connect(self.checktable)
		self.p3_linear.stateChanged.connect(self.normenable)
		# p4
		self.p4_peak.currentIndexChanged.connect(self.setpeaknorm)
		self.p4_pnorm_combo.currentIndexChanged.connect(self.setnpeaksnorm)
		self.p4_pnorm.toggled.connect(self.curvechanger)
		# settings
		self.graphenable(False)
		self.g_current_sb.setKeyboardTracking(False)
		self.g_plus.clicked.connect(lambda: self.graphchangeval(1))
		self.g_minus.clicked.connect(lambda: self.graphchangeval(-1))
		self.p2_dot_c.setKeyboardTracking(False)
		self.p2_mad_c.setKeyboardTracking(False)
		self.p3_isotb.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		self.p3_fittb.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
	
	def modechanger(self):
		is_multi = True if self.p1_smm.isChecked() else False
		self.p1_wcol.setEnabled(is_multi)
		self.p1_ccol.setEnabled(is_multi)
	
	def curvechanger(self):
		status = True if self.p4_pnorm.isChecked() else False
		self.p4_pnorm_combo.setEnabled(status)
		self.p4_npeak_norm.setEnabled(status)
	
	def setoutliers(self):
		self.p2_apply_out.setEnabled(True)
		dot = True if self.p2_dot.isChecked() else False
		self.p2_dot_c.setEnabled(dot)
		self.p2_mad_c.setEnabled(not dot)
			
	def setgoptions(self):
		# Current Index selected
		ci = self.g_selector.currentIndex()
		# Raw spectra
		if ci == 0:
			self.g_current = 'Raw'
			self.g_op = ['Wavelenght', 'nm', 'Counts', 'a.u.']
		# Spectra after having outliers removed
		elif ci == 1:
			self.g_current = 'Outliers'
			self.g_op = ['Wavelenght', 'nm', 'Counts', 'a.u.']
		# Correlation spectrum
		elif ci == 2:
			self.g_current = 'Correlation'
			self.g_op = ['Wavelenght', 'nm', 'Pearson correlation coefficient', '&rho;']
		# Isolated peaks
		elif ci == 3:
			self.g_current = 'Isolated'
			self.g_op = ['Wavelenght', 'nm', 'Intensity', 'a.u.']
		# Fitted peaks
		elif ci == 4:
			self.g_current = 'Fit'
			self.g_op = ['Wavelenght', 'nm', 'Intensity', 'a.u.']
		# Linear model regression
		elif ci == 5:
			self.g_current = 'Linear'
			self.g_op = ['True value', 'ref.u.', 'Predicted value', 'ref.u.']
		# PCA plot
		elif ci == 6:
			self.g_current = 'PCA'
			pca = self.g_current_sb.value()
			if pca == 1:
				self.g_op = ['Number of components', '#', 'Cumulative explained variance', '%']
			elif pca == 2:
				self.g_op = ['Principal Component <b>1</b>', 'a.u.', 'Principal Component <b>2</b>', 'a.u.']
			elif pca == 3:
				self.g_op = ['Principal Component <b>1</b>', 'a.u.', 'Principal Component <b>3</b>', 'a.u.']
			elif pca == 4:
				self.g_op = ['Principal Component <b>2</b>', 'a.u.', 'Principal Component <b>3</b>', 'a.u.']
			elif pca == 5:
				self.g_op = ['Attributes', 'a.u', 'PCA Loadings', 'a.u.']
		# PLS regression
		elif ci == 7:
			self.g_current = 'PLS'
			pls = self.g_current_sb.value()
			if pls == 1:
				self.g_op = ['True value', 'ref.u.', 'Predicted values', 'ref.u.']
			elif pls == 2:
				self.g_op = ['Sample', '#', 'Predicted values', 'ref.u.']
		# Saha-Boltzmann energy plot
		elif ci == 8:
			self.g_current = 'Temperature'
			self.g_op = ['Energy', 'eV', 'Ln', 'a.u.']
		# Change Graph labels
		self.g.setLabel('bottom', self.g_op[0], units=self.g_op[1])
		self.g.setLabel('left', self.g_op[2], units=self.g_op[3])
		
	# Graph methods
	def splot(self, x, y, clear=True, symbol=None, name=None, width=1):
		if clear: self.g.clear()
		if symbol is None:
			self.g.plot(x.reshape(-1), y.reshape(-1), pen=mkPen(randint(50, 200, (1, 3))[0], width=width), name=name)
		else:
			self.g.plot(x.reshape(-1), y.reshape(-1), pen=None, symbol=symbol, symbolBrush=mkBrush(randint(50, 200, (1, 3))[0]), name=name)
		self.g.autoRange()
		
	def mplot(self, x, matrix, hsl=True):
		smp = matrix.shape[1]
		colors = hsl_colors(smp) if hsl else randint(0, 255, (smp, 3))
		for i in range(smp):
			self.g.plot(x, matrix[:, i], pen=colors[i, :])
		self.g.autoRange()
	
	def fitplot(self, wavelength_iso: ndarray, area: ndarray, area_std: ndarray, width: ndarray, height: ndarray, shape: str, nfev: int, conv: bool, data: ndarray, total: ndarray):
		"""
		:param fitresults: A parameter containing all values and information for proper fit plotting
		:return: Nothing. Just do the plotting with additional information for user
		
		fitresults is an array with the following fields:
		
		[0] = Original (x,y) and residuals
		[1] = x-axis with more points (linspace)
		[2] = Total y-axis of fit, where each column is for a fit, and the last one is the SUM
		[3] = Shape of the fit
		[4] = Optimized results for Height, Width and Area. Size depends on peak numbers
		[5] = Number of functions evaluations for convergence
		[6] = Convergence (boolean)
		"""
		# important variables
		rmsd = std(data[:, 1])
		x = linspace(wavelength_iso[0], wavelength_iso[-1], 1000) if shape != 'Trapezoidal rule' else wavelength_iso
		height_str = ', '.join([f'{h:.0E}' for h in height])
		width_str = ', '.join([f'{w:.0E}' for w in width])
		area_str = ', '.join([f'{a:.0E}' for a in area])
		areastd_str = ', '.join([f'{s:.0E}' for s in area_std])
		# 1st plot is for original data and residuals
		self.g.plot(wavelength_iso, data[:, 0], symbol='o', pen=None, symbolBrush=mkBrush(randint(50, 220, (1, 3))[0]), name='Original data')
		self.g.plot(wavelength_iso, data[:, 1], symbol='+', pen=None, symbolBrush=mkBrush(list(randint(50, 220, (1, 3))[0])+[0.8]), name='Residuals')
		# The remaining plots are for each peak
		for i in range(len(area)):
			self.g.plot(x, total[:, i], pen=mkPen(randint(50, 220, (1, 3))[0], width=1), name='Peak %i' % (i + 1))
		# Last one is for total (sum of peaks)
		self.g.plot(x, total[:, -1], pen=mkPen(randint(50, 220, (1, 3))[0], width=2.5), name='Total')
		# Organizes string for fit box
		fitbox_str = f'Shape: <b>{shape}</b><br>' \
		             f'Evaluations: <b>{nfev}</b><br>' \
		             f'Convergence: <b>{conv}</b><br>' \
		             f'Height: <b>{height_str}</b><br>' \
		             f'Width: <b>{width_str}</b><br>'
		if area_std.mean() > 0:
			fitbox_str += f'Area: <b>{area_str}</b><br>' \
			              f'AreaSTD: <b>{areastd_str}</b><br>' \
			              f'RMSD: <b>{rmsd:.0E}</b>'
		else:
			fitbox_str += f'Area: <b>{area_str}</b><br>' \
			              f'RMSD: <b>{rmsd:.0E}</b>'
		fitbox = TextItem(html=fitbox_str, anchor=(1, 0), angle=0, border='#6600cc', fill='#f2e6ff')
		# Adds fit box to graphic and sets its position
		self.g.addItem(fitbox)
		my = (data, 0) if max(data[:, 0]) > max(total[:, -1]) else (total, -1)
		xpos = x[-1] + (x[-1] - x[0])/20
		ypos = max(my[0][:, my[1]]) + (max(my[0][:, my[1]]) - min(my[0][:, my[1]]))/20
		fitbox.setPos(xpos, ypos)
		# Finally, performs auto-range
		self.g.autoRange()
	
	def linplot(self, linear: dict, index: int):
		x, y = linear['Reference'][1], linear['Predict'][index, 1]
		self.splot(x, x, clear=True, symbol=None, name='Ideal', width=2)
		self.splot(x, y, clear=False, symbol='o', name='Model')
		linbox_str = f"Slope: <b>{linear['Slope'][index]:.3f}</b><br>" \
		             f"Intercept: <b>{linear['Intercept'][index]:.3f}</b><br>" \
		             f"R2: <b>{linear['R2'][index]:.3f}</b><br>" \
		             f"RMSE: <b>{linear['RMSE'][index]:.3f}</b><br>" \
					 f"LoD: <b>{linear['LoD'][index]:.3f}</b><br>"\
					 f"LoQ: <b>{linear['LoQ'][index]:.3f}</b><br>" \
					 f"Correlation: <b>{linear['R2'][index] ** 0.5:.0%}</b>"
		linbox = TextItem(html=linbox_str, anchor=(0, 1), angle=0, border='#004de6', fill='#ccddff')
		self.g.addItem(linbox)
		may = y if max(y) > max(x) else x
		miy = y if min(y) < min(x) else x
		xpos = x[-1] + (x[-1] - x[0]) / 20
		ypos = max(may) + (max(may) - min(miy))/20
		linbox.setPos(xpos, ypos)
		# Finally, performs auto-range
		self.g.autoRange()
	
	def pcaplot(self, idx: int, mode: str, param: tuple):
		if idx == 0:
			# Plot is for cumulative variance
			expvar = 100*param[0]
			ncomps = arange(1, expvar.size + 1)
			self.g.plot(ncomps, expvar, symbol='o', symbolBrush=pretty_colors(1), pen=mkPen(pretty_colors(1), style=Qt.DashLine))
		elif idx in (1, 2, 3):
			pass
		else:
			ld = param[0]
			if mode == 'Raw':
				x = param[1]['Raw']
			elif mode == 'Isolated':
				x = param[1]['Isolated'][0]
				for i in param[1]['Isolated'][1:]:
					x = hstack((x, i))
			else:
				x = arange(1, ld.shape[0]+1)
			sort = x.argsort()
			self.g.plot(x[sort], ld[sort][:, 0], pen=mkPen(pretty_colors(1), width=2), name='Loadings PC1')
			self.g.plot(x[sort], ld[sort][:, 1], pen=mkPen(pretty_colors(1), width=1.5), name='Loadings PC2')
			self.g.plot(x[sort], ld[sort][:, 2], pen=mkPen(pretty_colors(1), width=1), name='Loadings PC3')
		self.g.autoRange()
	
	def plsplot(self, param: dict, mode: str = 'CV'):
		# self.spec.pls['Element'] = self.gui.p5_pls_cal_ref.currentText()
		# self.spec.pls['Model'] = returned[0]
		# self.spec.pls['Reference'] = returned[1]
		# self.spec.pls['Predict'] = returned[2]
		# self.spec.pls['Residual'] = returned[3]
		# self.spec.pls['PredictR2'] = returned[4]
		# self.spec.pls['PredictRMSE'] = returned[5]
		# self.spec.pls['CrossValPredict'] = returned[6]
		# self.spec.pls['CrossValR2'] = returned[7]
		# self.spec.pls['CrossValRMSE'] = returned[8]
		if mode == 'CV':
			x = param['Reference']
			y1 = param['Predict']
			y2 = param['CrossValPredict']
			self.splot(x, x, clear=True, symbol=None, name='Ideal', width=2)
			self.splot(x, y1, clear=False, symbol='o', name='Predict')
			self.splot(x, y2, clear=False, symbol='t', name='CV Predict')
			# Adds message box (with report)
			plsbox_str = f"R2: <b>{param['PredictR2']:.3f}</b><br>" \
			             f"R2_CV: <b>{param['CrossValR2']:.3f}</b><br>" \
			             f"RMSEC: <b>{param['PredictRMSE']:.3f}</b><br>" \
			             f"RMSEC_CV: <b>{param['CrossValRMSE']:.3f}</b><br>" \
			             f"Correlation: <b>{param['PredictR2'] ** 0.5:.0%}</b>"
			plsbox = TextItem(html=plsbox_str, anchor=(0, 1), angle=0,
			                  border='#004de6', fill='#ccddff')
			self.g.addItem(plsbox)
			may = y2 if max(y2) > max(x) else x
			miy = y2 if min(y2) < min(x) else x
			xpos = x[-1] + (x[-1] - x[0]) / 20
			ypos = max(may) + (max(may) - min(miy)) / 20
			plsbox.setPos(xpos, ypos)
		elif mode == 'Blind':
			prediction = param['BlindPredict']
			x_pred = range(1, prediction.shape[0] + 1)
			colors = randint(10, 220, size=(len(prediction), 3), dtype=int)
			self.g.addItem(BarGraphItem(x=x_pred, height=prediction, width=0.9, brushes=colors))
		else:
			raise AssertionError('Illegal operation mode for PLS plot!')
		# Finally, performs auto-range
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
		elif tp.lower() in ('r', 'reference'):
			df = DataFrame(columns=['Ref_1', '...', 'Ref_n'], index=['Sample_1', '...', 'Sample_n'], data=rand(3,3)*10).round(3).to_html()
			return QtWidgets.QMessageBox.information(self.mw, top, f'{main}<p style="text-align: center">{df}</p>')
		else:
			QtWidgets.QMessageBox.critical(self.mw, 'Erro', 'Wrong MSG ID!')
			raise ValueError('Wrong MSG ID!')
	
	def guifd(self, parent: Path, tp: str, st1: str, st2: str = ''):
		if tp in ('ged', 'getExistingDirectory'):
			return QtWidgets.QFileDialog.getExistingDirectory(parent=self.mw, caption=st1, dir=str(parent))
		elif tp in ('gof', 'getOpenFileName'):
			return QtWidgets.QFileDialog.getOpenFileName(parent=self.mw, caption=st1, filter=st2, dir=str(parent))
		elif tp in ('gsf', 'getSaveFileName'):
			return QtWidgets.QFileDialog.getSaveFileName(parent=self.mw, caption=st1, filter=st2, dir=str(parent))
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
	
	def config_fsn(self, mode: int):
		if mode == 0:
			self.p1_fsn_type.setEnabled(self.p1_fsn_check.isChecked())
		elif mode == 1:
			en_dis = True if self.p1_fsn_type.currentText() == 'Internal Standard' else False
			self.p1_fsn_lminus.setEnabled(en_dis)
			self.p1_fsn_lplus.setEnabled(en_dis)
			self.p1_fsn_labelminus.setEnabled(en_dis)
			self.p1_fsn_labelplus.setEnabled(en_dis)
		elif mode == 2:
			self.p1_fsn_lminus.blockSignals(True)
			if self.p1_fsn_lminus.value() >= self.p1_fsn_lplus.value():
				self.guimsg('Invalid value', 'Lower wavelenght must be <b style="color: red">lower</b> than upper!', 'w')
				self.p1_fsn_lminus.setValue(0.0)
			self.p1_fsn_lminus.blockSignals(False)
		elif mode == 3:
			self.p1_fsn_lplus.blockSignals(True)
			if self.p1_fsn_lplus.value() <= self.p1_fsn_lminus.value():
				self.guimsg('Invalid value', 'Upper wavelenght must be <b style="color: red">bigger</b> than lower!', 'w')
				self.p1_fsn_lplus.setValue(1000.0)
			self.p1_fsn_lplus.setKeyboardTracking(False)
	
	def graphchangeval(self, val: int):
		self.g_current_sb.setValue(self.g_current_sb.value()+val)
	
	def graphenable(self, status: bool):
		self.g_selector.setEnabled(status)
		self.g_minus.setEnabled(status)
		self.g_plus.setEnabled(status)
		self.g_current_sb.setEnabled(status)
		self.g_run.setEnabled(status)
	
	def changetable(self, option: bool):
		self.p3_isotb.blockSignals(True)
		# creates set list for to-be-removed rows
		selected = set([x.row() for x in self.p3_isotb.selectedIndexes()])
		if selected.__len__() > 0:
				for r in selected:
					if option:
						self.p3_isotb.insertRow(r + 1)
						self.p3_isotb.setItem(r + 1, 4, QtWidgets.QTableWidgetItem('1'))
					else:
						self.p3_isotb.removeRow(r)
		else:
			if option:
				self.p3_isotb.setRowCount(self.p3_isotb.rowCount() + 1)
				self.p3_isotb.setItem(self.p3_isotb.rowCount() - 1, 4, QtWidgets.QTableWidgetItem('1'))
			else:
				self.p3_isotb.setRowCount(self.p3_isotb.rowCount() - 1)
		self.p3_isotb.blockSignals(False)
		
	def checktable(self, row, col):
		# Block all signals from widget (to better check values)
		self.p3_isotb.blockSignals(True)
		error = [False, '']
		# Checks if there is an empty cell
		value = self.p3_isotb.item(row, col).text()
		if not len(value) or '---' in value:
			error[0], error[1] = True,  'Cell can not be <b>empty</b>! Please assign a value.'
		# Now, we know cell is not empty, but must check if value are OK
		else:
			# Element column
			if col == 0:
				# Checks repeated values in element column
				element_value = self.p3_isotb.item(row, col).text().title().replace(' ', '_')
				rows = self.p3_isotb.rowCount()
				element_values = []
				for i in range(rows):
					if i != row:
						try:
							element_values.append(self.p3_isotb.item(i, col).text())
						except AttributeError:
							pass
				if element_value in element_values:
					error[0] = True
					error[1] = 'The element <b>%s</b> is already in the table.' % element_value
				else:
					self.p3_isotb.item(row, col).setText(element_value)
			# Lower and upper wavelengths columns
			elif col in (1, 2):
				try:
					float(value)
				except ValueError:
					error[0], error[1] = True, 'This cell can only accept <b>numbers<b>.'
			# Center column
			elif col == 3:
				for char in value:
					if (char not in ('.', ';')) and (char in punctuation):
						error[0] = True
						error[1] = 'This cell can only accept <b>numbers</b> <i>or</i> <b>numbers separated by semicolon</b>.'
						break
				else:
					# Runs if no break was raised
					center_value = value.split(';')
					for number in center_value:
						try:
							float(number)
						except ValueError:
							error[0] = True
							error[1] = 'This cell can only accept <b>numbers</b> <i>or</i> <b>numbers separated by semicolon</b>.'
			# Peak number column
			elif col == 4:
				try:
					peak_value = int(float(value))
					self.p3_isotb.item(row, col).setText(str(peak_value))
				except ValueError:
					error[0], error[1] = True, 'This cell can only accept <b>integers<b>.'
		# Shows error message and clear cell (if error was found)
		if error[0]:
			self.guimsg('Wrong value assigned', error[1], 'w')
			self.p3_isotb.item(row, col).setText('---')
		# Re-enables signals
		self.p3_isotb.blockSignals(False)
		
	def checktablevalues(self, w_lower: float, w_upper: float):
		rows = self.p3_isotb.rowCount()
		# Columns:
		# 0 = Element
		# 1 = Lower
		# 2 = Upper
		# 3 = Center
		# 4 = Peaks
		for r in range(rows):
			try:
				element = self.p3_isotb.item(r, 0).text()
				if not len(element):
					raise AttributeError('Invalid value for element.')
			except AttributeError:
				self.guimsg('Critical error', 'Empty value in <b>element</b> name!', 'c')
				return False
			else:
				try:
					[lower, upper] = list(map(float, [self.p3_isotb.item(r, 1).text(), self.p3_isotb.item(r, 2).text()]))
				except AttributeError:
					self.guimsg('Critical error', '<b>Upper</b> or <b>lower</b> cells have empty values!', 'c')
					return False
				else:
					try:
						l, u = lower < w_lower, upper > w_upper
					except TypeError:
						self.guimsg('Critical error', 'Please import data <b>before</b> using this feature!', 'c')
						return False
					if lower < w_lower or upper > w_upper:
							self.guimsg('Critical error', '<b>Upper</b> or <b>lower</b> wavelengths are not inside spectra range!'
							                              f'<p>Element: <b>{element}</b>'
							                              f'<br>Spectra range: <b>{w_lower}</b> to <b>{w_upper}</b>'
							                              f'<br><i>Table entered range</i>: <b>{lower}</b> to <b>{upper}</b></p>', 'c')
							return False
					if lower < upper:
						# checks center only if passed 1st verification
						try:
							center = self.p3_isotb.item(r, 3).text().split(';')
							peaks = int(self.p3_isotb.item(r, 4).text())
						except (AttributeError, ValueError):
							self.guimsg('Critical error', '<b>Center</b> or <b>#Peaks</b> cells have empty values!', 'c')
							return False
						else:
							if len(center) == peaks:
								# if number of peaks is according to center size, continues
								center_err = False
								for c in center:
									if lower < float(c) < upper:
										# all fine!
										pass
									else:
										error_str = 'Peak center <b>must</b> be between lower and upper values!<p>' \
										            'Element: <b>{e}</b><br><br>' \
										            'Lower: <b>{l}</b><br>' \
										            'Center: <b>{c}</b><br>' \
										            'Upper: <b>{u}</b>' \
										            '</p>'.format(e=element, u=upper, l=lower, c=float(c))
										self.guimsg('Invalid value', error_str, 'w')
										center_err = True
										break
								if center_err:
									return False
							else:
								error_str = 'Number of peaks does not have the same size as center list!<p>' \
								            'Element: <b>{e}</b><br><br>' \
								            '#Peaks: <b>{p}</b><br>' \
								            'Center: <b>{c}</b>' \
								            '</p>'.format(e=element, c=center, p=peaks)
								self.guimsg('Invalid value', error_str, 'w')
								return False
					else:
						error_str = 'Invalid values for upper and lower wavelengths!<p>' \
						            'Element: <b>{e}</b><br><br>' \
						            'Lower: <b>{l}</b><br>' \
						            'Upper: <b>{u}</b>' \
						            '</p>'.format(e=element, u=upper, l=lower)
						self.guimsg('Invalid range', error_str, 'w')
						return False
		else:
			return True
	
	def normenable(self):
		enable = True if self.p3_linear.isChecked() else False
		self.p3_norm.setEnabled(enable)
		if not enable:
			self.p3_norm.setChecked(enable)
	
	def create_fit_table(self):
		# Iso table columns:
		# 0 = Element
		# 1 = Lower
		# 2 = Upper
		# 3 = Center
		# 4 = Peaks
		# ------------------ #
		# Fit table columns:
		# 0 = Element
		# 1 = Shape
		# 2 = Asymmetry
		
		# Clear values in table
		self.p3_fittb.setRowCount(0)
		# Defines values for shape
		drop_down_list = ['1) Lorentzian',
		                  '2) Asymmetric Lorentzian',
		                  '3) Lorentzian [center fixed]',
		                  '4) Asym. Lorentzian [center fixed]',
		                  '5) Asym. Lorentzian [center/as. fixed]',
		                  '6) Gaussian',
		                  '7) Gaussian [center fixed]',
		                  '8) Voigt Profile',
		                  '9) Voigt Profile [center fixed]',
		                  '10) Trapezoidal rule']
		# Iterates over iso table
		rows = self.p3_isotb.rowCount()
		for r in range(rows):
			self.p3_fittb.insertRow(r)
			self.p3_fittb.setItem(r, 0, QtWidgets.QTableWidgetItem(self.p3_isotb.item(r, 0).text()))
			self.p3_fittb.setItem(r, 2, QtWidgets.QTableWidgetItem('0.5'))
			# for ComboBox
			shapes = QtWidgets.QComboBox()
			shapes.addItems(drop_down_list)
			self.p3_fittb.setCellWidget(r, 1, shapes)
			# Locks editing name
			self.p3_fittb.item(r, 0).setFlags(Qt.ItemIsEditable)
		self.p3_fittb.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
	
	def setpeaknorm(self):
		# Constructs list for normalization combo box
		self.peaknormitems = [self.p4_peak.itemText(i) for i in range(self.p4_peak.count()) if self.p4_peak.itemText(i) != self.p4_peak.currentText()]
		self.p4_pnorm_combo.clear()
		self.p4_pnorm_combo.addItems(self.peaknormitems)
		# Sets correct values for number of peaks
		for np in range(self.p3_isotb.rowCount()):
			if self.p4_peak.currentText() == self.p3_isotb.item(np, 0).text():
				val = int(self.p3_isotb.item(np, 4).text())
				self.p4_npeak.setValue(1)
				self.p4_npeak.setRange(1, val)
				break
	
	def setnpeaksnorm(self):
		for ap in range(self.p3_isotb.rowCount()):
			if self.p3_isotb.item(ap, 0).text() == self.p4_pnorm_combo.currentText():
				val = int(self.p3_isotb.item(ap, 4).text())
				self.p4_npeak_norm.setValue(1)
				self.p4_npeak_norm.setRange(1, val)
				break
		
#
# Extra functions
#
def pretty_colors(colors):
	"""uses golden ratio to create pleasant/pretty colours
	returns in rgb form"""
	output = zeros((colors, 3))
	golden_ratio_conjugate = (1 + (7**0.5)) / 2
	hue = random()
	for tmp in range(colors):
		hue += golden_ratio_conjugate * (tmp / (5 * random()))
		hue %= 1
		output[tmp, :] = [int(x * 256) for x in hsv_to_rgb(hue, 0.95, 0.75)]
	if colors == 1:
		return tuple(output[0])
	else:
		return output

def hsl_colors(colors):
	output = ones((colors, 3))*255
	for c in range(colors):
		h, l, s = randint(190, 360)/360, uniform(0.30, 0.70), uniform(0.5, 1)
		output[c, :] *= hls_to_rgb(h, l, s)
	return int16(output)

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