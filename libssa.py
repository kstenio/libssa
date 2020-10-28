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
from PySide2.QtWidgets import QApplication, QMessageBox, QMainWindow, QFileDialog, QProgressBar
from PySide2.QtCore import QThreadPool, QObject, QCoreApplication, Qt
from env.functions import changestatus
from env.gui import LIBSsaGUI
from env.spectra import Spectra
from env.worker import Worker
from env.imports import load
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
			self.parent = PosixPath()
			self.mbox = QMessageBox()
			self.mode = self.delimiter = ''
			self.timer = 0
			# connects
			self.connects()
			# extra variables
			self.variables()
			self.configthread()
	
	def variables(self):
		self.parent = Path.cwd()
	
	def connects(self):
		# page 1
		self.gui.p1_fdbtn.clicked.connect(self.spopen)
		self.gui.p1_ldspectra.clicked.connect(self.spload)
	
	def configthread(self):
		self.threadpool = QThreadPool()
		self.cores = self.threadpool.maxThreadCount()
		self.threadpool.setMaxThreadCount(self.cores - 1)
	
	#
	# GUI/helper functions
	#
	def guimsg(self, top: str, main: str, tp: str):
		if tp.lower() in ('w','warning'):
			return QMessageBox.warning(self.gui.mw, top, main)
		elif tp.lower() in ('i','information'):
			return QMessageBox.information(self.gui.mw, top, main)
		elif tp.lower() in ('q','question'):
			return QMessageBox.question(self.gui.mw, top, main)
		elif tp.lower() in ('c','critical'):
			return QMessageBox.critical(self.gui.mw, top, main)
		else:
			QMessageBox.critical(self.gui.mw, 'Erro', 'Wrong MSG ID!')
			raise ValueError('Wrong MSG ID!')
	
	def guifd(self, parent: PosixPath, tp: str, st1: str, st2: str = ''):
		if tp in ('ged', 'getExistingDirectory'):
			return QFileDialog.getExistingDirectory(self.gui.mw, st1, dir=parent.as_posix())
		else:
			QMessageBox.critical(self.gui.mw, 'Erro', 'Wrong FD ID!')
			raise ValueError('Wrong FD ID!')
	
	def dynamicbox(self, top: str, msg: str, maxi: int):
		self.mbox = QMessageBox(QMessageBox.Information, top, msg, QMessageBox.NoButton)
		mbox_layout = self.mbox.layout()
		mbox_layout.itemAtPosition(mbox_layout.rowCount() - 1, 0).widget().hide()
		self.mbox_pbar = QProgressBar()
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
			changestatus(self.gui.sb, msg, 'g', False)
			
		
	#
	# Methods for page 1 == Load Spectra
	#
	def spopen(self):
		# sets mode
		self.mode = 'Multiple' if self.gui.p1_smm.isChecked() else 'Single'
		# gets folder from file dialog
		folder = Path(self.guifd(self.parent, 'ged', 'Select spectra folder for %s mode' % self.mode))
		if folder.as_posix() == '.':
			self.guimsg('Error', 'Cancelled by the user.', 'w')
		else:
			# lists all in folder
			samples = listdir(folder.as_posix())
			samples.sort()
			samples_pathlib = [folder.joinpath(x) for x in samples]
			for s in samples_pathlib:
				if (self.mode == 'Multiple' and s.is_file()) or (self.mode == 'Single' and s.is_dir()):
					self.guimsg('Error', 'Wrong file structure for <b>%s</b> mode.' % self.mode, 'c')
					self.gui.p1_fdtext.setText('')
					self.spec.samples = [None]
					break
			else:
				self.parent = folder
				self.gui.p1_fdtext.setText(folder.as_posix())
				self.spec.nsamples = len(samples)
				self.spec.samples = samples
				self.spec.samples_path = samples_pathlib
	
	def spload(self):
		# module for receiving result from worker
		def result(returned):
			# enable load button
			self.gui.p1_ldspectra.setEnabled(True)
			# outputs timer
			print('Load spectra count timer: %.2f seconds. ' % (time() - self.timer))
			# saves result
			self.spec.wavelength = returned[0]
			self.spec.counts = returned[1]
		
		# the method itself
		if not self.spec.samples[0]:
			self.guimsg('Error', 'Please select <b>spectra folder</b> in order to load spectra.', 'w')
		else:
			# disable load button
			self.gui.p1_ldspectra.setEnabled(False)
			# configures worker
			changestatus(self.gui.sb, 'Please Wait. Loading spectra...', 'p', 1)
			self.dynamicbox('Loading data', '<b>Please wait</b>. Loading spectra into LIBSsa...', self.spec.nsamples)
			worker = Worker(load, self.spec.samples_path, self.mode, self.gui.p1_delim.currentText(), self.gui.p1_header.value(), self.gui.p1_wcol.value(), self.gui.p1_ccol.value())
			worker.signals.progress.connect(self.updatedynamicbox)
			worker.signals.finished.connect(lambda: self.updatedynamicbox(val=0, update=False, msg='Spectra loaded into LIBSsa'))
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
