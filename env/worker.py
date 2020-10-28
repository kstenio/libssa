#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  worker.py
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
from sys import exc_info
from traceback import print_exc, format_exc
from PySide2.QtCore import QObject, QRunnable, Signal, Slot

# signals for Qt worker
class WorkerSignals(QObject):
	# types of signals for LIBSsa
	finished = Signal()
	error = Signal(tuple)
	result = Signal(object)
	progress = Signal(int)


class Worker(QRunnable):
	def __init__(self, fn, *args, **kwargs):
		super(Worker, self).__init__()
		# args
		self.fn = fn
		self.args = args
		self.kwargs = kwargs
		self.signals = WorkerSignals()
		# adds callback (progress) to kwargs
		self.kwargs['progress'] = self.signals.progress
	
	@Slot(name='run')
	def run(self):
		try:
			result = self.fn(*self.args, **self.kwargs)
		except:
			# return error message as signal
			print_exc()
			exctype, value = exc_info()[:2]
			self.signals.error.emit((exctype, value, format_exc()))
		else:
			# returns result of functions
			self.signals.finished.emit()
			self.signals.result.emit(result)
		"""
		finally:
			# sends finished signal
			self.signals.finished.emit()
		"""