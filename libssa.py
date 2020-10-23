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
from PySide2.QtWidgets import QApplication, QMessageBox, QMainWindow
from PySide2.QtCore import QObject, QCoreApplication, Qt
from env.gui import *
from env.spectra import Spectra
from pathlib import Path


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
			#
	
	def variables(self):
		pass
	
	def connects(self):
		pass
	
	


			
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
