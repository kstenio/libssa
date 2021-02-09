#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  libssa.py
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

# imports
import sys
try:
	from time import time
	from os import listdir
	from pathlib import Path, PosixPath
	from env.worker import Worker
	from env.spectra import Spectra
	from pic.libssa_gui import LIBSsaGUI, changestatus
	from env.imports import load, outliers, refcorrel, domulticorrel
	from env.functions import isopeaks, fitpeaks
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
		# Main
		self.gui.g_run.clicked.connect(self.doplot)
		self.gui.g_selector.activated.connect(self.setgrange)
		self.gui.g_current_sb.valueChanged.connect(self.doplot)
		# Menu
		self.gui.menu_import_ref.triggered.connect(self.loadrefcorrel)
		# Page 1
		self.gui.p1_fdbtn.clicked.connect(self.spopen)
		self.gui.p1_ldspectra.clicked.connect(self.spload)
		# Page 2
		self.gui.p2_apply_out.clicked.connect(self.outliers)
		self.gui.p2_apply_correl.clicked.connect(self.docorrel)
		self.gui.p2_dot_c.valueChanged.connect(self.outliers)
		self.gui.p2_mad_c.valueChanged.connect(self.outliers)
		# Page 3
		self.gui.p3_isoapply.clicked.connect(self.peakiso)
		self.gui.p3_fitapply.clicked.connect(self.peakfit)
		
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
			i = idx // self.spec.nsamples
			j = idx - (i * self.spec.nsamples)
			self.gui.g.setTitle('Isolated peak of <b>%s</b> for sample <b>%s</b>' %(self.spec.wavelength_iso[i][0], self.spec.samples_path[j].stem))
			self.gui.mplot(self.spec.wavelength_iso[i][2], self.spec.counts_iso[i][j])
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
				self.gui.g.setTitle('PLSR prediction model for <b>%s</b>' % 'Element')
				self.gui.mplot(self.spec.wavelength, self.spec.counts[idx])
			if idx == 1:
				self.gui.g.setTitle('PLSR blind predictions for <b>%s</b>' % 'Element')
				self.gui.mplot(self.spec.wavelength, self.spec.counts[idx])
		elif self.gui.g_current == 'Linear':
			if idx == 0:
				self.gui.g.setTitle('Calibration curve for <b>%s</b> using <u>Height</u> as <i>Intensity</i>' % 'Element')
				self.gui.mplot(self.spec.wavelength, self.spec.counts[idx])
			if idx == 1:
				self.gui.g.setTitle('Calibration curve for <b>%s</b> using <u>Area</u> as <i>Intensity</i>' % 'Element')
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
			rvalue = self.spec.nsamples * self.spec.wavelength_iso.__len__()
			self.gui.g_current_sb.setRange(1, rvalue)
			self.gui.g_max.setText(str(rvalue))
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
	# Methods for page 1 == Load spectra
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
		# inner function to receive result from worker
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
		
		# inner function to receive errors from worker
		def error(runerror):
			# closes progress bar and updates statusbar
			self.gui.mbox.close()
			changestatus(self.gui.sb, 'Could not import Spectra. Check parameters and try again.', 'r', 0)
			# enable gui elements
			self.gui.graphenable(True)
			self.gui.p1_ldspectra.setEnabled(True)
			self.gui.p2_apply_out.setEnabled(True)
			# outputs timer
			print('Timestamp:', time(), 'ERROR: Could not import spectra. Timer: %.2f seconds.' % (time() - self.timer))
			# ousputs error message
			runerror_message = 'Could not import data properly! ' \
			                   'Try recheck a spectrum file and change import parameters (mostly <b>header</b> or <b>delimiter</b>).' \
			                   '<p>Error type: <b><i><u>%s</u></i></b></p>' \
			                   '<p>Error message:<br><b>%s</b></p>' % (runerror[0].__name__, str(runerror[1]))
			self.gui.guimsg('Error!', runerror_message, 'c')
			
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
			worker.signals.error.connect(error)
			self.configthread()
			self.timer = time()
			self.threadpool.start(worker)
			
	#
	# Methods for page 2 == Outliers and correlation spectrum
	#
	def outliers(self):
		# inner function to receive result from worker
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
					self.gui.p2_correl_lb.setText('Reference file <b><u>%s</u></b> properly imported to LIBSsa.' % ref_file.name )
					self.gui.p2_apply_correl.setEnabled(True)
	
	def docorrel(self):
		# inner function to receive result from worker
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
		
	#
	# Methods for page 3 == Regions and peak fitting
	#
	def peakiso(self):
		# inner function to receive result from worker
		def result(returned):
			# saves result
			self.spec.wavelength_iso, self.spec.counts_iso = returned
			# enable apply button
			self.gui.p3_isoapply.setEnabled(True)
			# outputs timer
			print('Timestamp:', time(), 'MSG: Peak isolation count timer: %.2f seconds. ' % (time() - self.timer))
			# updates gui elements
			self.ranged = False
			self.gui.g_selector.setCurrentIndex(3)
			self.doplot()
			self.gui.create_fit_table()
		
		# Checks if iso table is complete
		if self.gui.p3_isotb.rowCount() > 0:
			# Checks if values are OK
			if self.gui.checktablevalues(self.spec.wavelength[0], self.spec.wavelength[-1]):
				changestatus(self.gui.sb, 'Please Wait. Isolating peaks...', 'p', 1)
				self.gui.p3_isoapply.setEnabled(False)
				counts = self.spec.counts_out if len(self.spec.counts_out) > 1 else self.spec.counts
				elements, lower, upper, center = [], [], [], []
				for tb in range(self.gui.p3_isotb.rowCount()):
					elements.append(self.gui.p3_isotb.item(tb, 0).text())
					lower.append(float(self.gui.p3_isotb.item(tb, 1).text()))
					upper.append(float(self.gui.p3_isotb.item(tb, 2).text()))
					# for center
					center_cell = self.gui.p3_isotb.item(tb, 3).text()
					if ';' in center_cell:
						center.append(list(map(float, self.gui.p3_isotb.item(tb, 3).text().split(';'))))
					else:
						center.append([float(self.gui.p3_isotb.item(tb, 3).text())])
				self.gui.dynamicbox('Isolating peaks', '<b>Please wait</b>. This may take a while...', len(elements))
				worker = Worker(isopeaks, self.spec.wavelength, counts, elements, lower, upper, center, self.gui.p3_linear.isChecked(), self.gui.p3_norm.isChecked())
				worker.signals.progress.connect(self.gui.updatedynamicbox)
				worker.signals.finished.connect(lambda: self.gui.updatedynamicbox(val=0, update=False, msg='Peak isolation finished'))
				worker.signals.result.connect(result)
				self.configthread()
				self.timer = time()
				self.threadpool.start(worker)
			else:
				changestatus(self.gui.sb, 'Wrong value in isolation table', 'r', 1)
		else:
			self.gui.guimsg('Error', 'Please enter isolation parameters in the <b>table</b> before using this feature.', 'w')
			
	def peakfit(self):
		if self.spec.wavelength_iso.size:
			# Iterates over fit table rows to get selected values of shapes and asymmetry
			fittable_rows = self.gui.p3_fittb.rowCount()
			shapes = [x.split(')')[1][1:] for x in [self.gui.p3_fittb.cellWidget(y, 1).currentText() for y in range(fittable_rows)]]
			asymmetry = [float(z) for z in [self.gui.p3_fittb.item(w, 2).text() for w in range(fittable_rows)]]
			# Run the fit function
			fitpeaks(self.spec.wavelength_iso, self.spec.counts_iso, list(zip(shapes, asymmetry)))
		else:
			self.gui.guimsg('Error', 'Please perform peak isolation <b>before</b> using this feature.', 'w')
		
	
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
