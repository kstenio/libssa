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
import sys
from PySide2.QtGui import QKeyEvent
from PySide2.QtWidgets import QApplication, QMessageBox, QMainWindow
from PySide2.QtCore import QThreadPool, QObject, QCoreApplication, Qt
from env.gui import LIBSsaGUI, changestatus
from env.spectra import Spectra
from env.worker import Worker
from env.imports import load, outliers
from pathlib import Path, PosixPath
from os import listdir
from time import time

class LIBSSA2(QObject):
	"""
	This is LIBSsa main APP.

	In it we have all needed functions, actions and connects for the app to work properly.
	"""
	def __init__(self, ui_file: str, logo_file: str, parent=None):
		# checks if ui file exists and warn users if not
		try:
			super(LIBSSA2, self).__init__(parent)
			self.gui = LIBSsaGUI(ui_file, logo_file)
			self.gui.mw.show()
		except ValueError:
			QMessageBox.critical(QMainWindow(None), 'Critical error!', 'Could not find <b>libssa.ui (or libssa.svg)</b> files in pic folder!')
			sys.exit(1)
		else:
			# if all is fine with ui, then starts to read other modules
			self.spec = Spectra()
			# defines global variables
			self.threadpool = QThreadPool()
			self.parent = PosixPath()
			self.mbox = QMessageBox()
			self.mode = self.delimiter = ''
			self.cores = self.ranged = self.timer = 0
			# connects
			self.connects()
			# extra variables
			self.variables()
	
	def variables(self):
		self.parent = Path.cwd()
	
	def connects(self):
		# main
		self.gui.g_run.clicked.connect(self.doplot)
		self.gui.g_selector.activated.connect(self.setgrange)
		self.gui.g_current_sb.editingFinished.connect(self.doplot)
		# page 1
		self.gui.p1_fdbtn.clicked.connect(self.spopen)
		self.gui.p1_ldspectra.clicked.connect(self.spload)
		# page 2
		self.gui.p2_apply_out.clicked.connect(self.outliers)
		self.gui.p2_dot_c.valueChanged.connect(self.outliers)
		self.gui.p2_mad_c.valueChanged.connect(self.outliers)
		
	def configthread(self):
		self.threadpool = QThreadPool()
		self.cores = self.threadpool.maxThreadCount()
		self.threadpool.setMaxThreadCount(self.cores - 1)
	
	#
	# Methods for Graphics
	#
	def doplot(self):
		# Rechecks current ranges
		if not self.ranged: self.setgrange()
		# Sets current index
		idx = self.gui.g_current_sb.value() - 1
		# Perform plot based on actual settings
		if self.gui.g_current == 'Raw':
			self.gui.g.setTitle('Raw LIBS spectra from sample <b>%s</b>' % self.spec.samples_path[idx].stem)
			self.gui.mplot(self.spec.wavelength, self.spec.counts[idx])
		elif self.gui.g_current == 'Outliers':
			self.gui.g.setTitle('Outliers removed LIBS spectra from sample <b>%s</b>' % self.spec.samples_path[idx].stem)
			self.gui.mplot(self.spec.wavelength, self.spec.counts_out[idx])
		elif self.gui.g_current == 'Correlation':
			self.gui.g.setTitle('Correlation spectrum os sample set (for ELEMENT)')
			self.gui.mplot(self.spec.wavelength, self.spec.counts[idx])
		elif self.gui.g_current == 'Isolated':
			self.gui.g.setTitle('Isolated peak of <b>%s</b> for sample <b>%s</b>' %('ELEMENT', self.spec.samples_path[idx].stem))
			self.gui.mplot(self.spec.wavelength, self.spec.counts[idx])
		elif self.gui.g_current == 'Fit':
			self.gui.g.setTitle('Fitted peak of <b>%s</b> for sample <b>%s</b>' % ('ELEMENT', self.spec.samples_path[idx].stem))
			self.gui.mplot(self.spec.wavelength, self.spec.counts[idx])
		elif self.gui.g_current == 'PCA':
			if idx == 0:
				self.gui.g.setTitle('Cumulative explained variance as function of number of components')
				self.gui.mplot(self.spec.wavelength, self.spec.counts[idx])
			if idx == 1:
				self.gui.g.setTitle('Principal component <b>2</b> as function of component <b>1</b>')
				self.gui.mplot(self.spec.wavelength, self.spec.counts[idx])
			if idx == 2:
				self.gui.g.setTitle('Principal component <b>3</b> as function of component <b>1</b>')
				self.gui.mplot(self.spec.wavelength, self.spec.counts[idx])
			if idx == 3:
				self.gui.g.setTitle('Principal component <b>3</b> as function of component <b>2</b>')
				self.gui.mplot(self.spec.wavelength, self.spec.counts[idx])
		elif self.gui.g_current == 'PLS':
			if idx == 0:
				self.gui.g.setTitle('PLSR prediction model for <b>%s</b>' %('Element') )
				self.gui.mplot(self.spec.wavelength, self.spec.counts[idx])
			if idx == 1:
				self.gui.g.setTitle('PLSR blind predictions for <b>%s</b>' % ('Element'))
				self.gui.mplot(self.spec.wavelength, self.spec.counts[idx])
		elif self.gui.g_current == 'Linear':
			if idx == 0:
				self.gui.g.setTitle('Calibration curve for <b>%s</b> using <u>Height</u> as <i>Intensity</i>' % ('Element'))
				self.gui.mplot(self.spec.wavelength, self.spec.counts[idx])
			if idx == 1:
				self.gui.g.setTitle('Calibration curve for <b>%s</b> using <u>Area</u> as <i>Intensity</i>' % ('Element'))
				self.gui.mplot(self.spec.wavelength, self.spec.counts[idx])
		elif self.gui.g_current == 'Temperature':
			self.gui.g.setTitle('Saha-Boltzmann plot for sample <b>%s</b>' % self.spec.samples_path[idx].stem)
			self.gui.mplot(self.spec.wavelength, self.spec.counts[idx])
	
	def setgrange(self):
		# Enable ranged global variable
		self.ranged = True
		# Helper idx variable
		idx = self.gui.g_selector.currentIndex()
		# Sets correct range based on current graph
		if idx == 0:
			# Raw spectra
			self.gui.g_current_sb.setRange(1, self.spec.nsamples)
			self.gui.g_max.setText(str(self.spec.nsamples))
		elif idx == 1:
			# Spectra after having outliers removed
			self.gui.g_current_sb.setRange(1, self.spec.nsamples)
			self.gui.g_max.setText(str(self.spec.nsamples))
		elif idx == 2:
			# Correlation spectrum
			self.gui.g_current_sb.setRange(1, 1)
			self.gui.g_max.setText('1')
		elif idx == 3:
			# Isolated peaks
			self.gui.g_current_sb.setRange(1, len(self.spec.counts_iso))
			self.gui.g_max.setText(str(len(self.spec.counts_iso)))
		elif idx == 4:
			# Fitted peaks
			self.gui.g_current_sb.setRange(1, len(self.spec.counts_iso))
			self.gui.g_max.setText(str(len(self.spec.counts_iso)))
		elif idx == 5:
			# PCA
			self.gui.g_current_sb.setRange(1, 5)
			self.gui.g_max.setText('5')
		elif idx == 6:
			# PLS
			self.gui.g_current_sb.setRange(1, 2)
			self.gui.g_max.setText('2')
		elif idx == 7:
			# Linear curve
			self.gui.g_current_sb.setRange(1, 2)
			self.gui.g_max.setText('2')
		elif idx == 8:
			# Saha-Boltzmann plot
			self.gui.g_current_sb.setRange(1, self.spec.nsamples)
			self.gui.g_max.setText(str(self.spec.nsamples))
			
	#
	# Methods for page 1 == Load Spectra
	#
	def spopen(self):
		# sets mode
		self.mode = 'Multiple' if self.gui.p1_smm.isChecked() else 'Single'
		# gets folder from file dialog
		folder = Path(self.gui.guifd(self.parent, 'ged', 'Select spectra folder for %s mode' % self.mode))
		if folder.as_posix() == '.':
			self.gui.guimsg('Error', 'Cancelled by the user.', 'w')
		else:
			# lists all in folder
			samples = listdir(folder.as_posix())
			samples.sort()
			samples_pathlib = [folder.joinpath(x) for x in samples]
			for s in samples_pathlib:
				if (self.mode == 'Multiple' and s.is_file()) or (self.mode == 'Single' and s.is_dir()):
					self.gui.guimsg('Error', 'Wrong file structure for <b>%s</b> mode.' % self.mode, 'c')
					self.gui.p1_fdtext.setText('')
					self.gui.p1_fdtext.setEnabled(False)
					self.spec.samples = [None]
					break
			else:
				self.parent = folder
				self.gui.p1_fdtext.setText(folder.as_posix())
				self.gui.p1_fdtext.setEnabled(True)
				# self.spec.nsamples = len(samples)
				self.spec.samples = samples
				self.spec.samples_path = samples_pathlib
	
	def spload(self):
		# module for receiving result from worker
		def result(returned):
			# saves result
			self.spec.wavelength, self.spec.counts = returned
			self.spec.nsamples = len(self.spec.samples)
			# enable load button
			self.gui.p1_ldspectra.setEnabled(True)
			# outputs timer
			print('Load spectra count timer: %.2f seconds. ' % (time() - self.timer))
			# updates gui elements
			self.gui.g_selector.setCurrentIndex(0)
			self.doplot()
		
		# the method itself
		if not self.spec.samples[0]:
			self.gui.guimsg('Error', 'Please select <b>spectra folder</b> in order to load spectra.', 'w')
		else:
			# disable load button
			self.gui.p1_ldspectra.setEnabled(False)
			# configures worker
			changestatus(self.gui.sb, 'Please Wait. Loading spectra...', 'p', 1)
			self.gui.dynamicbox('Loading data', '<b>Please wait</b>. Loading spectra into LIBSsa...', self.spec.samples.__len__())
			worker = Worker(load, self.spec.samples_path, self.mode, self.gui.p1_delim.currentText(), self.gui.p1_header.value(), self.gui.p1_wcol.value(), self.gui.p1_ccol.value(), self.gui.p1_dec.value())
			worker.signals.progress.connect(self.gui.updatedynamicbox)
			worker.signals.finished.connect(lambda: self.gui.updatedynamicbox(val=0, update=False, msg='Spectra loaded into LIBSsa'))
			worker.signals.result.connect(result)
			self.configthread()
			self.timer = time()
			self.threadpool.start(worker)
			
	#
	# Methods for page 2 == Operations
	#
	def outliers(self):
		# module for receiving result from worker
		def result(returned):
			# saves result
			self.spec.counts_out = returned
			# enable apply button
			self.gui.p2_apply_out.setEnabled(True)
			# outputs timer
			print('Outliers removal count timer: %.2f seconds. ' % (time() - self.timer))
			# updates gui elements
			self.gui.g_selector.setCurrentIndex(1)
			self.doplot()
		
		# main method itself
		if self.spec.nsamples <= 0:
			self.gui.guimsg('Error', 'Please import data <b>before</b> using this feature.', 'w')
		else:
			# defines type of outliers removal (and selected criteria)
			out_type = 'SAM' if self.gui.p2_dot.isChecked() else 'MAD'
			criteria = self.gui.p2_dot_c.value() if self.gui.p2_dot.isChecked() else self.gui.p2_mad_c.value()
			if out_type == 'SAM':
				out_size = self.spec.nsamples
			elif out_type == 'MAD':
				out_size = self.spec.wavelength.__len__()
			else:
				raise ValueError('Outliers removal algorithm not selected.') # this should not happen. Else here just in case it does...
			# now, setup tome configs and initialize worker
			changestatus(self.gui.sb, 'Please Wait. Removing outliers...', 'p', 1)
			self.gui.dynamicbox('Removing outliers', '<b>Please wait</b>. Using <b>%s</b> to remove outliers...' % out_type, out_size)
			self.gui.p2_apply_out.setEnabled(False)
			worker = Worker(outliers, out_type, criteria, self.spec.counts)
			worker.signals.progress.connect(self.gui.updatedynamicbox)
			worker.signals.finished.connect(lambda: self.gui.updatedynamicbox(val=0, update=False, msg='Outliers removed from set'))
			worker.signals.result.connect(result)
			self.configthread()
			self.timer = time()
			self.threadpool.start(worker)
	
	
if __name__ == '__main__':
	# checks the ui file and run LIBSsa main app
	uif = Path.cwd().joinpath('pic').joinpath('libssa.ui')
	lof = Path.cwd().joinpath('pic').joinpath('libssa.svg')
	QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
	app = QApplication(sys.argv)
	if uif.is_file() and lof.is_file():
		form = LIBSSA2(str(uif), str(lof))
		sys.exit(app.exec_())
	else:
		form = LIBSSA2('','')
		sys.exit(app.exec_())
