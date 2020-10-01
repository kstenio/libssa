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
from pathlib import Path


class LIBSSA2(QObject):
	def __init__(self, ui_file: str, parent=None):
		if ui_file != '0':
			super(LIBSSA2, self).__init__(parent)
			self.gui = LIBSsaGUI(ui_file)
			self.gui.mw.show()
			self.start = True
		else:
			QMessageBox.critical(QMainWindow(), 'Critical error!', 'Could not find <b>libssa.ui</b> file in pic folder!')
			sys.exit(1)

			
if __name__ == '__main__':
	# checks the ui file and run LIBSsa main app
	uif = Path.cwd().joinpath('pic').joinpath('1libssa.ui')
	QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
	app = QApplication(sys.argv)
	if uif.is_file():
		form = LIBSSA2(str(uif))
		sys.exit(app.exec_())
	else:
		form = LIBSSA2('0')
		sys.exit(app.exec_())
