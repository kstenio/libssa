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
try:
	from time import time
	from os import listdir
	from pathlib import Path, PosixPath
	from env.worker import Worker
	from env.spectra import Spectra
	from env.gui import LIBSsaGUI, changestatus
	from env.imports import load, outliers, refcorrel, domulticorrel
	from PySide2.QtGui import QKeyEvent
	from PySide2.QtWidgets import QApplication, QMessageBox, QMainWindow
	from PySide2.QtCore import QThreadPool, QObject, QCoreApplication, Qt
except (ImportError, ImportWarning) as err:
	print('\nYou have missing libraries to install.\n\n'
	      '\tError message: {error}\n\n'
	      'Check the README.md for extra info.'.format(error=str(err)))
	sys.exit(1)


# LIBSsa main class
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
		self.gui.g_current_sb.valueChanged.connect(self.doplot)
		# menu
		self.gui.menu_import_ref.triggered.connect(self.loadrefcorrel)
		# page 1
		self.gui.p1_fdbtn.clicked.connect(self.spopen)
		self.gui.p1_ldspectra.clicked.connect(self.spload)
		# page 2
		self.gui.p2_apply_out.clicked.connect(self.outliers)
		self.gui.p2_apply_correl.clicked.connect(self.docorrel)
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
			self.gui.g.clear()
			self.gui.g.setTitle('Correlation spectrum for <b>%s</b>' % self.spec.pearson_ref.columns[idx])
			self.gui.splot(self.spec.wavelength, self.spec.pearson[0][:, idx], False)
			self.gui.splot(self.spec.wavelength, self.spec.pearson[1], False)
			self.gui.splot(self.spec.wavelength, self.spec.pearson[2], False)
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
			self.gui.g_current_sb.setRange(1, self.spec.pearson_ref.columns.__len__())
			self.gui.g_max.setText(str(self.spec.pearson_ref.columns.__len__()))
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
			# enable gui elements
			self.gui.graphenable(True)
			self.gui.p1_ldspectra.setEnabled(True)
			self.gui.p2_apply_out.setEnabled(True)
			# outputs timer
			print('Timestamp:', time(), 'MSG: Load spectra count timer: %.2f seconds. ' % (time() - self.timer))
			# updates gui elements
			self.ranged = False
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
			print('Timestamp:', time(), 'MSG: Outliers removal count timer: %.2f seconds. ' % (time() - self.timer))
			# updates gui elements
			self.ranged = False
			self.gui.g_selector.setCurrentIndex(1)
			self.doplot()
		
		# main method itself
		if self.spec.nsamples <= 0:
			self.gui.guimsg('Error', 'Please import data <b>before</b> using this feature.', 'w')
		else:
			# defines type of outliers removal (and selected criteria)
			out_type = 'SAM' if self.gui.p2_dot.isChecked() else 'MAD'
			criteria = self.gui.p2_dot_c.value() if self.gui.p2_dot.isChecked() else self.gui.p2_mad_c.value()
			# now, setup some configs and initialize worker
			changestatus(self.gui.sb, 'Please Wait. Removing outliers...', 'p', 1)
			self.gui.dynamicbox('Removing outliers', '<b>Please wait</b>. Using <b>%s</b> to remove outliers...' % out_type, self.spec.nsamples)
			self.gui.p2_apply_out.setEnabled(False)
			worker = Worker(outliers, out_type, criteria, self.spec.counts)
			worker.signals.progress.connect(self.gui.updatedynamicbox)
			worker.signals.finished.connect(lambda: self.gui.updatedynamicbox(val=0, update=False, msg='Outliers removed from set'))
			worker.signals.result.connect(result)
			self.configthread()
			self.timer = time()
			self.threadpool.start(worker)
	
	def loadrefcorrel(self):
		if self.spec.nsamples <= 0:
			self.gui.guimsg('Error', 'Please import data <b>before</b> using this feature.', 'w')
		else:
			# gets file from dialog
			ref_file = Path(self.gui.guifd(self.parent, 'gof', 'Select reference spreadsheet file', 'Excel Spreadsheet Files (*.xls *.xlsx)')[0])
			if ref_file.as_posix() == '.':
				self.gui.guimsg('Error', 'Cancelled by the user.', 'w')
			else:
				ref_spreadsheet = refcorrel(ref_file)
				if ref_spreadsheet.index.__len__() != self.spec.nsamples:
					self.gui.guimsg('Error',
					                'Total of rows in spreadsheet: <b>{rows}</b><br>'
					                'Total of samples in sample set: <b>{samples}</b><br><br>'
					                'Number of rows <b>must</b> be the same as total of samples!'.format(
						                rows=ref_spreadsheet.index.__len__(),
						                samples=self.spec.nsamples), 'c')
				else:
					# enables gui element and saves val
					self.spec.pearson_ref = ref_spreadsheet
					self.gui.p2_apply_correl.setEnabled(True)
	
	def docorrel(self):
		# module for receiving result from worker
		def result(returned):
			# saves result
			self.spec.pearson = returned
			# enable apply button
			self.gui.p2_apply_correl.setEnabled(True)
			# outputs timer
			print('Timestamp:', time(),
			      'MSG: Correlation spectrum count timer: %.2f seconds. ' % (
						      time() - self.timer))
			# updates gui elements
			self.ranged = False
			self.gui.g_selector.setCurrentIndex(2)
			self.doplot()
		
		# setup some configs and initialize worker
		changestatus(self.gui.sb, 'Please Wait. Creating correlation spectrum...', 'p', 1)
		self.gui.dynamicbox('Creating correlation spectrum',
		                    '<b>Please wait</b>. This may take a while...',
		                    self.spec.pearson_ref.columns.__len__())
		self.gui.p2_apply_correl.setEnabled(False)
		worker = Worker(domulticorrel, self.spec.wavelength.__len__(), self.spec.counts, self.spec.pearson_ref)
		worker.signals.progress.connect(self.gui.updatedynamicbox)
		worker.signals.finished.connect(
			lambda: self.gui.updatedynamicbox(val=0, update=False,
			                                  msg='Correlation spectrum for all parameters finished'))
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
