#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Kleydson Stenio (kleydson.stenio@gmail.com).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along
# with this program.  If not, see <https://www.gnu.org/licenses/agpl-3.0.html>.


# Imports
try:
	import sys
	import lzma
	import pickle
	import libssa.env.export as export
	from time import time
	from os import listdir
	from pathlib import Path
	from pandas import DataFrame
	from markdown import markdown
	from datetime import datetime
	from traceback import print_exc
	from psutil import virtual_memory
	from libssa.env.spectra import Spectra, Worker
	from libssa.env.gui.libssagui import LIBSsaGUI, changestatus
	from libssa.env.imports import load, outliers, refcorrel, domulticorrel
	from libssa.env.functions import (
		isopeaks,
		fitpeaks,
		linear_model,
		zeros,
		column_stack,
		pca_do,
		pca_scan,
		pls_do,
		tne_do,
		array,
	)
	from PySide6.QtWidgets import (
		QApplication,
		QMessageBox,
		QMainWindow,
		QTableWidgetItem,
	)
	from PySide6.QtCore import QThreadPool, QObject, QCoreApplication, Qt
except (ImportError, ImportWarning) as err:
	err_msg = str(err)
	print(
		f"\nYou have missing libraries to install.\n\n"
		f"\tError message: {err_msg}\n\n"
		f"Check the README.md for extra info.\n"
	)
	if "opengl" in err_msg.lower():
		print(
			'If you are under Linux Mint 20+ (or Ubuntu 20.04+), try running: "apt install libopengl0"'
		)
	elif "xcb" in err_msg.lower():
		print(
			'If you are under Linux Mint 20+ (or Ubuntu 20.04+), try running: "apt install libxcb-xinerama0 libxcb-cursor0"'
		)
	print_exc()
	sys.exit(1)


# LIBSsa main class
class LIBSSA2(QMainWindow):
	"""
	This is LIBSsa main APP.

	In it, we have all needed functions, actions and connects for the app to work properly.
	"""

	def __init__(self, ui_file: str, logo_file: str):
		# Checks if ui file exists and warn users if not
		try:
			super(LIBSSA2, self).__init__()
			self.gui = LIBSsaGUI(ui_file, logo_file)
		except Exception as ex:
			QMessageBox.critical(
				QMainWindow(None),
				"Critical error!",
				f"Can not initialize LIBSsa!"
				f'<p>Error message: <b style="color: red">{str(ex)}</b></p>',
			)
			sys.exit(1)
		else:
			# If all is fine with ui, then starts to read other modules
			self.spec = Spectra()
			# Defines global variables
			self.threadpool = QThreadPool()
			self.parent = Path()
			self.mbox = QMessageBox()
			self.mode, self.delimiter = "", ""
			self.cores, self.timer = 0, 0
			self.bytes_to_gb = 1073741824
			self.memory = virtual_memory()
			self.root = Path(__file__).parent
			# Connects
			self.connects()
			# Extra variables
			self.variables()

	def variables(self):
		self.parent = Path.cwd()
		self.create_about()

	def connects(self):
		# Main
		self.gui.g_run.clicked.connect(self.doplot)
		self.gui.g_selector.activated.connect(self.setgrange)
		self.gui.g_current_sb.valueChanged.connect(self.doplot)
		# Menu
		self.gui.menu_file_load.triggered.connect(lambda: self.environment("load"))
		self.gui.menu_file_save.triggered.connect(lambda: self.environment("save"))
		self.gui.menu_file_quit.triggered.connect(self.gui.mw.close)
		self.gui.menu_import_ref.triggered.connect(self.loadref)
		self.gui.menu_import_peaks.triggered.connect(
			lambda: self.spreadsheet_to_table("Peaks")
		)
		self.gui.menu_import_tne.triggered.connect(
			lambda: self.spreadsheet_to_table("TNe")
		)
		self.gui.menu_export_fullspectra_raw.triggered.connect(
			lambda: self.export_mechanism(1)
		)
		self.gui.menu_export_fullspectra_out.triggered.connect(
			lambda: self.export_mechanism(2)
		)
		self.gui.menu_export_peaks_table.triggered.connect(
			lambda: self.export_mechanism(3)
		)
		self.gui.menu_export_peaks_isolated.triggered.connect(
			lambda: self.export_mechanism(4)
		)
		self.gui.menu_export_peaks_fitted.triggered.connect(
			lambda: self.export_mechanism(5)
		)
		self.gui.menu_export_peaks_areas.triggered.connect(
			lambda: self.export_mechanism(6)
		)
		self.gui.menu_export_predictions_linear.triggered.connect(
			lambda: self.export_mechanism(7)
		)
		self.gui.menu_export_predictions_pls.triggered.connect(
			lambda: self.export_mechanism(8)
		)
		self.gui.menu_export_other_pca.triggered.connect(
			lambda: self.export_mechanism(9)
		)
		self.gui.menu_export_other_tne.triggered.connect(
			lambda: self.export_mechanism(10)
		)
		self.gui.menu_export_other_correl.triggered.connect(
			lambda: self.export_mechanism(11)
		)
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
		# Page 4
		self.gui.p4_apply.clicked.connect(self.docalibrationcurve)
		# Page 5
		self.gui.p5_pca_cscan.clicked.connect(self.pca_perform_scan)
		self.gui.p5_pca_do.clicked.connect(self.pca_do)
		self.gui.p5_pls_cal_start.clicked.connect(self.pls_do)
		self.gui.p5_pls_pred_start.clicked.connect(self.pls_predict)
		# Page 6
		self.gui.p6_start.clicked.connect(self.calc_t_ne)

	def configthread(self):
		self.threadpool = QThreadPool()
		self.cores = self.threadpool.maxThreadCount()
		self.threadpool.setMaxThreadCount(self.cores - 1)

	def create_about(self):
		readme = self.root.joinpath("README_GUI.md")
		save = False
		try:
			if readme.is_file():
				with readme.open("r") as r:
					html = markdown(r.read())
			else:
				raise FileNotFoundError("File <b>README.md</b> not found.")
		except FileNotFoundError:
			# self.gui.guimsg(
			#     "Error",
			#     "Could not find <b>README.md</b> file inside application root.",
			#     "w",
			# )
			print_exc()
		else:
			self.gui.version = html.split("\n")[1].split("<em>")[1].split("<")[0]
			self.gui.about_html = html
			self.gui.mw.setWindowTitle(
				f"Laser Induced Breakdown Spectroscopy spectra analyzer - LIBSsa - v{self.gui.version}"
			)
			if save:
				with self.root.joinpath("doc", "readme.html").open("w") as r:
					r.write(html)

	#
	# Menu input/output methods
	#
	def environment(self, mode: str = "save"):
		dt = datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")
		if mode == "save":
			# Fist, we bust check available RAM and warn user
			self.memory = virtual_memory()
			minimum_ram = 8
			recommended_ram = 16
			system_ram = self.memory.total
			percent_ram = (
				(self.memory.percent, "blue")
				if self.memory.percent <= 50
				else (self.memory.percent, "red")
			)
			if system_ram > recommended_ram * self.bytes_to_gb:
				color = "darkgreen"
			elif system_ram > minimum_ram * self.bytes_to_gb:
				color = "blue"
			else:
				color = "red"
			question = self.gui.guimsg(
				"Warning",
				f"Saving environment may take a <b>lot of time</b>, and is very demmading on CPU and RAM memmory, "
				f"depending on how much data was loaded and processed in the program.<br><p>"
				f"Minimum RAM: <b>{minimum_ram} Gb</b><br>"
				f"Recommended RAM: <b>{recommended_ram} Gb</b><br>"
				f'System RAM: <b style="color: {color}">{system_ram / self.bytes_to_gb:.2f} Gb</b><br>'
				f'Percent used RAM: <b style="color: {percent_ram[1]}">{percent_ram[0]} %</b></p>'
				f"Do you want to proceed?",
				"q",
			)
			if question == QMessageBox.Yes:
				# Now that user decided to export, continue...
				changestatus(self.gui.sb, "Please wait, saving environment...", "b", 1)
				save_file = Path(
					self.gui.guifd(
						Path.home().joinpath(f"LIBSsa_Environment_{dt}.lb2e"),
						"gsf",
						f"Choose filename to save environment",
						"LIBSsa 2.0 Environment (*.lb2e)",
					)[0]
				)
				if save_file.name in ("", "."):
					self.gui.guimsg("Error", "Cancelled by the user.", "w")
					self.gui.sb.clearMessage()
				else:
					# Actually starts
					save_file = save_file.with_suffix(".lb2e")
					with lzma.open(save_file, "wb", preset=3) as loc:
						pickle.dump(self.spec, loc)
					if save_file.is_file():
						self.gui.guimsg(
							"Done!",
							f"<b>Environment</b> data properly saved."
							f"<p>Save location: <a href={save_file.as_uri()}>{save_file.name}</a></p>",
							"i",
						)
						changestatus(self.gui.sb, "Environment saved", "g", 0)
					else:
						self.gui.guimsg(
							"Error!",
							f"Could not save <b>environment</b> data properly. Try free more RAM.",
							"c",
						)
						changestatus(
							self.gui.sb, "Error when saving environment", "r", 0
						)
		elif mode == "load":
			changestatus(self.gui.sb, "Please wait, loading environment...", "b", 1)
			load_file = Path(
				self.gui.guifd(
					self.parent,
					"gof",
					f"Choose filename to load environment",
					"LIBSsa 2.0 Environment (*.lb2e)",
				)[0]
			)
			if load_file.name in ("", "."):
				self.gui.guimsg("Error", "Cancelled by the user.", "w")
				self.gui.sb.clearMessage()
			else:
				with lzma.open(load_file, "rb") as loc:
					self.spec = pickle.load(loc)
				# Show message and updates gui elements
				self.gui.guimsg(
					"Done!",
					f"<b>Environment</b> data properly loaded into LIBSsa!"
					f"<p>File loaded: <a href={load_file.as_uri()}>{load_file.name}</a></p>",
					"i",
				)
				changestatus(self.gui.sb, "Environment loaded", "g", 0)
				self.gui.graphenable(True)
				self.gui.p2_apply_out.setEnabled(True)
				self.gui.g_selector.setCurrentIndex(0)
				self.setgrange()
				# If there is reference loaded
				if self.spec.ref.index.size > 1:
					self.gui.p2_correl_lb.setText(
						f"Reference data imported with <b><u>{load_file.stem}</u></b> environment."
					)
					self.gui.p2_apply_correl.setEnabled(True)
					self.gui.p4_ref.clear()
					self.gui.p5_pls_cal_ref.clear()
					self.gui.p4_ref.addItems(self.spec.ref.columns)
					self.gui.p5_pls_cal_ref.addItems(self.spec.ref.columns)
				# If iso table was created before
				if self.spec.isolated["Table"].index.size > 0:
					iso_df = self.spec.isolated["Table"]
					rows, cols = iso_df.index.size, iso_df.columns.size
					self.gui.p3_isotb.setRowCount(rows)
					self.gui.p3_isotb.setColumnCount(cols)
					for r in range(rows):
						for c in range(cols):
							self.gui.p3_isotb.setItem(
								r, c, QTableWidgetItem(iso_df.loc[r, c])
							)
					self.peakiso()
				# If TNe data was created before
				if self.spec.plasma["Element"]:
					element = self.spec.plasma["Element"]
					self.gui.p6_table_dfs = self.spec.plasma["Tables"]
					self.gui.p6_element.setCurrentIndex(0)
					self.gui.p6_element.setCurrentText(element)
		else:
			raise AssertionError(f"Illegal operation mode: {mode}")

	def loadref(self):
		if not self.spec.samples["Count"]:
			self.gui.guimsg(
				"Error", "Please import data <b>before</b> using this feature.", "w"
			)
		else:
			# Shows warning
			msg_str = (
				'Reference spreadsheet file (<i>XLS</i> or <i>XLSX</i>) <b style="color: red">must</b> be structured in the following manner:'
				"<ol>"
				"<li>First column containing the identifier of the sample;</li>"
				"<li>Samples has to be in the same order as the spectra files/folders;</li>"
				"<li>Remaining columns containing the values for each reference.</li>"
				"</ol>"
				"Check the example bellow:"
			)
			self.gui.guimsg("Instructions", msg_str, "r")
			# gets file from dialog
			ref_file = Path(
				self.gui.guifd(
					self.parent,
					"gof",
					"Select reference spreadsheet file",
					"Excel Spreadsheet Files (*.xls *.xlsx)",
				)[0]
			)
			if str(ref_file) == ".":
				self.gui.guimsg("Error", "Cancelled by the user.", "i")
			else:
				ref_spreadsheet = refcorrel(ref_file)
				if ref_spreadsheet.index.size != self.spec.samples["Count"]:
					self.gui.guimsg(
						"Error",
						"Total of rows in spreadsheet: <b>{rows}</b><br>"
						"Total of samples in sample set: <b>{samples}</b><br><br>"
						"Number of rows <b>must</b> be the same as total of samples!".format(
							rows=ref_spreadsheet.index.__len__(),
							samples=self.spec.samples["Count"],
						),
						"c",
					)
				else:
					# Removes illegal slash in column names (if exists)
					ref_spreadsheet.columns = [
						x.replace("/", "÷") for x in ref_spreadsheet.columns
					]
					# Enables gui element and saves val
					self.spec.ref = ref_spreadsheet
					self.gui.p2_correl_lb.setText(
						"Reference file <b><u>%s</u></b> properly imported to LIBSsa."
						% ref_file.name
					)
					self.gui.p2_apply_correl.setEnabled(True)
					# Puts values inside reference for calibration curve and PLS combo boxes
					self.gui.p4_ref.clear()
					self.gui.p5_pls_cal_ref.clear()
					self.gui.p4_ref.addItems(self.spec.ref.columns)
					self.gui.p5_pls_cal_ref.addItems(self.spec.ref.columns)

	def spreadsheet_to_table(self, mode: str):
		if mode == "TNe":
			self.gui.guimsg(
				"Warning!",
				"Make sure <b>peaks matrix</b> is created and <b>element for T/Ne</b> "
				'is set <b style="color: red">BEFORE</b> importing spreadsheet!',
				"w",
			)
		filepath = Path(
			self.gui.guifd(
				self.parent,
				"gof",
				f"Select spreadsheet to update {mode} table",
				"Excel 2007+ Spreadsheet (*.xlsx)",
			)[0]
		)
		if filepath.name in ("", "."):
			self.gui.guimsg("Error", "Cancelled by the user.", "w")
		else:
			self.gui.update_table_from_spreadsheet(mode, filepath.with_suffix(".xlsx"))

	def export_mechanism(self, mode: int):
		# Proper defines modes inside a dict
		modes_dict = {
			1: "RAW Spectra",
			2: "Outliers Removed Spectra",
			3: "Peaks Table",
			4: "Isolated Peaks",
			5: "Peak Fitting",
			6: "Peaks Report",
			7: "Predicions (Linear Regression)",
			8: "Predictions (PLS Regression)",
			9: "PCA Data",
			10: "Temperature and Ne Report",
			11: "Correlation Spectrum",
		}
		# Creates variables to be used in the method
		dt, suffix = datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss"), ""
		# Gets values based on mode
		if mode == 1:
			suffix = ""
			func = export.export_raw
			func_param = (self.spec, "Raw")
			fd_params = (
				Path.home(),
				"getExistingDirectory",
				f"Choose folder for exporting {modes_dict[mode]} data",
				"",
			)
			index = False
		elif mode == 2:
			suffix = ""
			func = export.export_raw
			func_param = (self.spec, "Outliers")
			fd_params = (
				Path.home(),
				"getExistingDirectory",
				f"Choose folder for exporting {modes_dict[mode]} data",
				"",
			)
			index = False
		elif mode == 3:
			suffix = ".xlsx"
			func = export.export_iso_table
			func_param = [self.gui.p3_isotb]
			fd_params = (
				Path.home().joinpath(f"Iso_Tables_Report_{dt}.xlsx"),
				"getSaveFileName",
				f"Choose filename to export {modes_dict[mode]} data",
				"Excel 2007+ Spreadsheet (*.xlsx)",
			)
			index = True
		elif mode == 4:
			suffix = ".xlsx"
			func = export.export_iso_peaks
			func_param = [self.spec]
			fd_params = (
				Path.home().joinpath(f"Iso_Peaks_Report_{dt}.xlsx"),
				"getSaveFileName",
				f"Choose filename to export {modes_dict[mode]} data",
				"Excel 2007+ Spreadsheet (*.xlsx)",
			)
			index = True
		elif mode == 5:
			suffix = ".xlsx"
			func = export.export_fit_peaks
			func_param = [self.spec]
			fd_params = (
				Path.home().joinpath(f"Fit_Peaks_Report_{dt}.xlsx"),
				"getSaveFileName",
				f"Choose filename to export {modes_dict[mode]} data",
				"Excel 2007+ Spreadsheet (*.xlsx)",
			)
			index = True
		elif mode == 6:
			func = export.export_fit_areas
			suffix = ".xlsx"
			func_param = [self.spec]
			fd_params = (
				Path.home().joinpath(f"Fit_Areas_Report_{dt}.xlsx"),
				"getSaveFileName",
				f"Choose filename to export {modes_dict[mode]} data",
				"Excel 2007+ Spreadsheet (*.xlsx)",
			)
			index = True
		elif mode == 7:
			suffix = ".xlsx"
			func = export.export_linear
			func_param = [self.spec]
			fd_params = (
				Path.home().joinpath(f"Linear_Model_Report_{dt}.xlsx"),
				"getSaveFileName",
				f"Choose filename to export {modes_dict[mode]} report",
				"Excel 2007+ Spreadsheet (*.xlsx)",
			)
			index = True
		elif mode == 8:
			suffix = ".xlsx"
			func = export.export_pls
			func_param = [self.spec]
			fd_params = (
				Path.home().joinpath(f"PLS_Model_Report_{dt}.xlsx"),
				"getSaveFileName",
				f"Choose filename to export {modes_dict[mode]} report",
				"Excel 2007+ Spreadsheet (*.xlsx)",
			)
			index = True
		elif mode == 9:
			suffix = ".xlsx"
			func = export.export_pca
			func_param = [self.spec]
			fd_params = (
				Path.home().joinpath(f"PCA_Report_{dt}.xlsx"),
				"getSaveFileName",
				f"Choose filename to export {modes_dict[mode]} report",
				"Excel 2007+ Spreadsheet (*.xlsx)",
			)
			index = True
		elif mode == 10:
			suffix = ".xlsx"
			func = export.export_tne
			func_param = [self.spec]
			fd_params = (
				Path.home().joinpath(f"T-Ne_Report_{dt}.xlsx"),
				"getSaveFileName",
				f"Choose filename to export {modes_dict[mode]} report",
				"Excel 2007+ Spreadsheet (*.xlsx)",
			)
			index = True
		elif mode == 11:
			suffix = ".xlsx"
			func = export.export_correl
			func_param = [self.spec]
			fd_params = (
				Path.home().joinpath(f"Correl_Report_{dt}.xlsx"),
				"getSaveFileName",
				f"Choose filename to export {modes_dict[mode]} report",
				"Excel 2007+ Spreadsheet (*.xlsx)",
			)
			index = True
		else:
			raise AssertionError("Illegal mode for export data!")
		# Call file dialog
		try:
			changestatus(
				self.gui.sb,
				f"Please wait, exporting {modes_dict[mode]} data...",
				"b",
				1,
			)
			path = (
				self.gui.guifd(*fd_params)[0] if index else self.gui.guifd(*fd_params)
			)
		except TypeError:
			self.gui.guimsg(
				"Error",
				f"Can not export data for <b>{modes_dict[mode]}</b>."
				f"<br>Not implemented yet.",
				"c",
			)
			self.gui.sb.clearMessage()
		else:
			path = Path(path)
			if path.name in ("", "."):
				self.gui.guimsg("Error", "Cancelled by the user.", "w")
				self.gui.sb.clearMessage()
			else:
				# Run func with parameters
				try:
					func(path.with_suffix(suffix) if suffix else path, *func_param)
				except Exception as ex:
					print_exc()
					self.gui.guimsg(
						"Could not export data!",
						f"Failed to save <u><b>{modes_dict[mode]}</b></u>."
						f'<p>Error message: <b style="color: red">{str(ex)}</b></p>',
						"c",
					)
					changestatus(
						self.gui.sb,
						f"{modes_dict[mode]} data could not be saved",
						"r",
						0,
					)
				else:
					self.gui.guimsg(
						"Done!",
						f"<b>{modes_dict[mode]}</b> data properly saved."
						f"<p>Save location: <a href={path.as_uri()}>{path.name}</a></p>",
						"i",
					)
					changestatus(self.gui.sb, f"{modes_dict[mode]} data saved", "g", 0)

	#
	# Methods for Graphics
	#
	def setgrange(self):
		# Helper idx variable
		idx = self.gui.g_selector.currentIndex()
		# Sets correct range based on current graph
		if idx == 0:
			# Raw spectra
			self.gui.g_current_sb.setRange(1, self.spec.samples["Count"])
			self.gui.g_max.setText(str(self.spec.samples["Count"]))
		elif idx == 1:
			# Spectra after having outliers removed
			self.gui.g_current_sb.setRange(1, self.spec.samples["Count"])
			self.gui.g_max.setText(str(self.spec.samples["Count"]))
		elif idx == 2:
			# Correlation spectrum
			self.gui.g_current_sb.setRange(1, self.spec.ref.columns.__len__())
			self.gui.g_max.setText(str(self.spec.ref.columns.__len__()))
		elif idx == 3:
			# Isolated peaks
			rvalue = self.spec.samples["Count"] * self.spec.isolated["Count"]
			self.gui.g_current_sb.setRange(1, rvalue)
			self.gui.g_max.setText(str(rvalue))
		elif idx == 4:
			# Fitted peaks
			rvalue = self.spec.samples["Count"] * self.spec.isolated["Count"]
			self.gui.g_current_sb.setRange(1, rvalue)
			self.gui.g_max.setText(str(rvalue))
		elif idx == 5:
			# Linear curve
			self.gui.g_current_sb.setRange(1, self.spec.linear["R2"].size)
			self.gui.g_max.setText(str(self.spec.linear["R2"].size))
		elif idx == 6:
			# PCA
			self.gui.g_current_sb.setRange(1, 5)
			self.gui.g_max.setText("5")
		elif idx == 7:
			# PLS
			self.gui.g_current_sb.setRange(1, 2)
			self.gui.g_max.setText("2")
		elif idx == 8:
			# Saha-Boltzmann plot
			self.gui.g_current_sb.setRange(1, self.spec.samples["Count"])
			self.gui.g_max.setText(str(self.spec.samples["Count"]))
		# Do plot after correcting the ranges
		self.doplot()

	def doplot(self):
		# Gets current index and clear legend
		idx = self.gui.g_current_sb.value() - 1
		self.gui.g_legend.setPen(None)
		self.gui.g.clear()
		# Perform plot based on actual settings
		if self.gui.g_current == "Raw":
			self.gui.g.setTitle(
				f"Raw LIBS spectra from sample <b>{self.spec.samples['Name'][idx]}</b>"
			)
			self.gui.mplot(
				self.spec.wavelength["Raw"], self.spec.intensities["Raw"][idx]
			)
		elif self.gui.g_current == "Outliers":
			self.gui.g.setTitle(
				f"Outliers removed LIBS spectra from sample <b>{self.spec.samples['Name'][idx]}</b>"
			)
			self.gui.mplot(
				self.spec.wavelength["Raw"], self.spec.intensities["Outliers"][idx]
			)
		elif self.gui.g_current == "Correlation":
			self.gui.g.setTitle(
				f"Correlation spectrum for <b>{self.spec.ref.columns[idx]}</b>"
			)
			self.gui.splot(
				self.spec.wavelength["Raw"],
				self.spec.pearson["Data"][:, idx],
				clear=True,
				name="Pearson",
			)
			self.gui.splot(
				self.spec.wavelength["Raw"],
				self.spec.pearson["Full-Mean"],
				clear=False,
				name="Sampling Average Spectrum",
			)
			self.gui.splot(
				self.spec.wavelength["Raw"], self.spec.pearson["Zeros"], clear=False
			)
		elif self.gui.g_current == "Isolated":
			# i == index for elements
			# j == index for samples
			i = idx // self.spec.samples["Count"]
			j = idx - (i * self.spec.samples["Count"])
			self.gui.g.setTitle(
				f"Isolated peak of <b>{self.spec.isolated['Element'][i]}</b> for sample <b>{self.spec.samples['Name'][j]}</b>"
			)
			self.gui.mplot(
				self.spec.wavelength["Isolated"][i],
				self.spec.intensities["Isolated"][i][j],
			)
		elif self.gui.g_current == "Fit":
			i = idx // self.spec.samples["Count"]
			j = idx - (i * self.spec.samples["Count"])
			k = self.spec.fit
			self.gui.g.setTitle(
				f"Fitted peak of <b>{self.spec.isolated['Element'][i]}</b> for sample <b>{self.spec.samples['Name'][j]}</b>"
			)
			self.gui.fitplot(
				self.spec.wavelength["Isolated"][i],
				k["Area"][i][j],
				k["AreaSTD"][i][j],
				k["Width"][i][j],
				k["Height"][i][j],
				k["Shape"][i],
				k["NFev"][i][j],
				k["Convergence"][i][j],
				k["Data"][i][j],
				k["Total"][i][j],
			)
			del k
		elif self.gui.g_current == "Linear":
			self.gui.g.setTitle(
				f"Linear model of {self.spec.linear['Predict'][idx, 0]}"
			)
			self.gui.linplot(self.spec.linear, idx)
		elif self.gui.g_current == "PCA":
			self.gui.setgoptions()
			if idx == 0:
				self.gui.g.setTitle(
					"Cumulative explained variance as function of number of components"
				)
				self.gui.pcaplot(
					idx, self.spec.pca["Mode"], tuple([self.spec.pca["ExpVar"]])
				)
			else:
				self.gui.g_legend.setPen("#52527a")
				if idx == 1:
					self.gui.g.setTitle(
						"Principal component <b>2</b> as function of component <b>1</b>"
					)
					self.gui.splot(
						self.spec.pca["Transformed"][:, 0],
						self.spec.pca["Transformed"][:, 1],
						symbol="o",
						name="PC2(PC1)",
					)
				if idx == 2:
					self.gui.g.setTitle(
						"Principal component <b>3</b> as function of component <b>1</b>"
					)
					self.gui.splot(
						self.spec.pca["Transformed"][:, 0],
						self.spec.pca["Transformed"][:, 2],
						symbol="o",
						name="PC3(PC1)",
					)
				if idx == 3:
					self.gui.g.setTitle(
						"Principal component <b>3</b> as function of component <b>2</b>"
					)
					self.gui.splot(
						self.spec.pca["Transformed"][:, 1],
						self.spec.pca["Transformed"][:, 2],
						symbol="o",
						name="PC2(PC3)",
					)
				if idx == 4:
					self.gui.g.setTitle(
						"Plot of <b>Loadings</b> (P1/P2/P3) as function of <b>attributes</b>"
					)
					self.gui.pcaplot(
						idx,
						self.spec.pca["Mode"],
						tuple([self.spec.pca["Loadings"], self.spec.wavelength]),
					)
		elif self.gui.g_current == "PLS":
			self.gui.setgoptions()
			if idx == 0:
				self.gui.g.setTitle(
					f'PLSR prediction model for <b>{self.spec.pls["Element"]}</b>'
					f' (<i style="color: #1a75ff">{self.spec.pls["Att"]}</i>)'
				)
				self.gui.plsplot(self.spec.pls, mode="CV")
			if idx == 1:
				self.gui.g.setTitle(
					f'PLSR blind predictions for <b>{self.spec.pls["Element"]}</b>'
					f' (<i style="color: #1a75ff">{self.spec.pls["Att"]}</i>)'
				)
				self.gui.plsplot(self.spec.pls, mode="Blind")
		elif self.gui.g_current == "Temperature":
			self.gui.g.setTitle(
				f'Saha-Boltzmann plot for sample <b>{self.spec.samples["Name"][idx]}</b>'
				f' (<i style="color: #1a75ff">{self.spec.plasma["Parameter"]}s</i>)'
			)
			self.gui.saha_b_plot(self.spec.plasma, idx)

	#
	# Methods for page 1 == Load spectra
	#
	def spopen(self):
		# Sets mode
		self.mode = "Multiple" if self.gui.p1_smm.isChecked() else "Single"
		# Gets folder from file dialog
		folder = Path(
			self.gui.guifd(
				self.parent, "ged", "Select spectra folder for %s mode" % self.mode
			)
		)
		if str(folder) == ".":
			self.gui.guimsg("Error", "Cancelled by the user.", "w")
		else:
			# Lists all in folder
			samples = listdir(folder)
			samples.sort()
			samples_pathlib = [folder.joinpath(x) for x in samples]
			for s in samples_pathlib:
				if (self.mode == "Multiple" and s.is_file()) or (
					self.mode == "Single" and s.is_dir()
				):
					self.gui.guimsg(
						"Error",
						"Wrong file structure for <b>%s</b> mode." % self.mode,
						"c",
					)
					self.gui.p1_fdtext.setText("")
					self.gui.p1_fdtext.setEnabled(False)
					self.spec.samples = self.spec.base
					break
			else:
				# Saves variables for further steps
				self.parent = folder
				self.spec.clear()
				self.spec.samples["Count"] = len(samples)
				self.spec.samples["Name"] = tuple([x.stem for x in samples_pathlib])
				self.spec.samples["Path"] = tuple(samples_pathlib)
				# Updates gui elements
				self.gui.p1_fdtext.setText(str(folder))
				self.gui.p1_fdtext.setEnabled(True)

	def spload(self):
		# Inner function to receive result from worker
		def result(returned):
			# Saves result
			self.spec.wavelength["Raw"] = returned[0]
			self.spec.intensities["Raw"] = returned[1]
			self.spec.intensities["Count"] = self.spec.samples["Count"]
			# Enable gui elements
			self.gui.graphenable(True)
			self.gui.p1_ldspectra.setEnabled(True)
			self.gui.p2_apply_out.setEnabled(True)
			# Outputs timer
			print(
				"Timestamp:",
				time(),
				"MSG: Load spectra count timer: %.2f seconds. " % (time() - self.timer),
			)
			# Updates gui elements
			self.gui.g_selector.setCurrentIndex(0)
			self.setgrange()

		# Inner function to receive errors from worker
		def ld_error(runerror):
			# Closes progress bar and updates statusbar
			self.gui.mbox.close()
			changestatus(
				self.gui.sb,
				"Could not import Spectra. Check parameters and try again.",
				"r",
				0,
			)
			# Enable gui elements
			self.gui.graphenable(True)
			self.gui.p1_ldspectra.setEnabled(True)
			self.gui.p2_apply_out.setEnabled(True)
			# Outputs timer
			print(
				"Timestamp:",
				time(),
				"ERROR: Could not import spectra. Timer: %.2f seconds."
				% (time() - self.timer),
			)
			# Outputs error message
			runerror_message = (
				"Could not import data properly! "
				"Try recheck a spectrum file and change import parameters (mostly <b>header</b> or <b>delimiter</b>)."
				"<p>Error type: <b><i><u>%s</u></i></b></p>"
				"<p>Error message:<br><b>%s</b></p>" % (runerror[0], runerror[1])
			)
			self.gui.guimsg("Error!", runerror_message, "c")

		# the method itself
		error = False
		fsn = [None, None, None]
		# Check if folder was selected
		if not self.spec.samples["Count"]:
			self.gui.guimsg(
				"Error",
				"Please select <b>spectra folder</b> in order to load spectra.",
				"w",
			)
			error = True
		# Check if fsn is enabled
		if self.gui.p1_fsn_check.isChecked():
			fsn_mode = (
				"IS"
				if self.gui.p1_fsn_type.currentText() == "Internal Standard"
				else self.gui.p1_fsn_type.currentText()
			)
			fsn[0] = fsn_mode
			if fsn_mode == "IS":
				lm = self.gui.p1_fsn_lminus.value()
				lp = self.gui.p1_fsn_lplus.value()
				if lp <= lm:
					self.gui.guimsg(
						"Error",
						"Use appropriate values for FSN Internal Standard mode.",
						"w",
					)
					error = True
				else:
					fsn[1] = lm
					fsn[2] = lp
		if not error:
			# Disable load button
			self.gui.p1_ldspectra.setEnabled(False)
			# Configures worker
			changestatus(self.gui.sb, "Please Wait. Loading spectra...", "p", 1)
			self.gui.dynamicbox(
				"Loading data",
				"<b>Please wait</b>. Loading spectra into LIBSsa...",
				self.spec.samples["Count"],
			)
			worker = Worker(
				load,
				self.spec.samples["Path"],
				self.mode,
				self.gui.p1_delim.currentText(),
				self.gui.p1_header.value(),
				self.gui.p1_wcol.value(),
				self.gui.p1_ccol.value(),
				self.gui.p1_dec.value(),
				fsn,
			)
			worker.signals.progress.connect(self.gui.updatedynamicbox)
			worker.signals.finished.connect(
				lambda: self.gui.updatedynamicbox(
					val=0, update=False, msg="Spectra loaded into LIBSsa"
				)
			)
			worker.signals.result.connect(result)
			worker.signals.error.connect(ld_error)
			self.configthread()
			self.timer = time()
			self.threadpool.start(worker)

	#
	# Methods for page 2 == Outliers and correlation spectrum
	#
	def outliers(self):
		# Inner function to receive result from worker
		def result(returned):
			# Saves result
			(
				self.spec.intensities["Outliers"],
				self.spec.intensities["Removed"],
			) = returned
			# Enable apply button
			self.gui.p2_apply_out.setEnabled(True)
			# Outputs timer
			print(
				"Timestamp:",
				time(),
				"MSG: Outliers removal count timer: %.2f seconds. "
				% (time() - self.timer),
			)
			# updates gui elements
			self.gui.g_selector.setCurrentIndex(1)
			self.setgrange()

		# Inner function to handle errors

		def errors(runerror):
			# Closes progress bar and updates statusbar
			self.gui.mbox.close()
			changestatus(
				self.gui.sb,
				"Could not perform outliers removal. Check spectra and try again.",
				"r",
				0,
			)
			# enable gui elements
			self.gui.p2_apply_out.setEnabled(True)
			# Outputs timer (error)
			print(
				"Timestamp:",
				time(),
				"ERROR: Could not remove outliers. Timer: %.2f seconds. "
				% (time() - self.timer),
			)
			# Outputs error message
			runerror_message = (
				"Could not remove outliers properly! "
				"Try recheck spectra and try again."
				"<p>Error type: <b><i><u>%s</u></i></b></p>"
				"<p>Error message:<br><b>%s</b></p>" % (runerror[0], runerror[1])
			)
			self.gui.guimsg("Error!", runerror_message, "c")

		# Main method itself
		if not self.spec.intensities["Count"]:
			self.gui.guimsg(
				"Error", "Please import data <b>before</b> using this feature.", "w"
			)
		else:
			# Defines type of outliers removal (and selected criteria)
			out_type = "SAM" if self.gui.p2_dot.isChecked() else "MAD"
			criteria = (
				self.gui.p2_dot_c.value()
				if self.gui.p2_dot.isChecked()
				else self.gui.p2_mad_c.value()
			)
			# Now, setup some configs and initialize worker
			changestatus(self.gui.sb, "Please Wait. Removing outliers...", "p", 1)
			self.gui.dynamicbox(
				"Removing outliers",
				"<b>Please wait</b>. Using <b>%s</b> to remove outliers..." % out_type,
				self.spec.intensities["Count"],
			)
			self.gui.p2_apply_out.setEnabled(False)
			worker = Worker(outliers, out_type, criteria, self.spec.intensities)
			worker.signals.progress.connect(self.gui.updatedynamicbox)
			worker.signals.finished.connect(
				lambda: self.gui.updatedynamicbox(
					val=0, update=False, msg="Outliers removed from set"
				)
			)
			worker.signals.result.connect(result)
			worker.signals.error.connect(errors)
			self.configthread()
			self.timer = time()
			self.threadpool.start(worker)

	def docorrel(self):
		# Inner function to receive result from worker
		def result(returned):
			# Saves result
			self.spec.pearson["Data"] = returned[0]
			self.spec.pearson["Full-Mean"] = returned[1]
			self.spec.pearson["Zeros"] = returned[2]
			# Enable apply button
			self.gui.p2_apply_correl.setEnabled(True)
			# Outputs timer
			print(
				"Timestamp:",
				time(),
				"MSG: Correlation spectrum count timer: %.2f seconds. "
				% (time() - self.timer),
			)
			# Updates gui elements
			self.gui.g_selector.setCurrentIndex(2)
			self.setgrange()

		# Setup some configs and initialize worker
		changestatus(
			self.gui.sb, "Please Wait. Creating correlation spectrum...", "p", 1
		)
		self.gui.dynamicbox(
			"Creating correlation spectrum",
			"<b>Please wait</b>. This may take a while...",
			self.spec.ref.columns.__len__(),
		)
		self.gui.p2_apply_correl.setEnabled(False)
		worker = Worker(
			domulticorrel,
			self.spec.wavelength["Raw"].size,
			self.spec.intensities["Raw"],
			self.spec.ref,
		)
		worker.signals.progress.connect(self.gui.updatedynamicbox)
		worker.signals.finished.connect(
			lambda: self.gui.updatedynamicbox(
				val=0,
				update=False,
				msg="Correlation spectrum for all parameters finished",
			)
		)
		worker.signals.result.connect(result)
		self.configthread()
		self.timer = time()
		self.threadpool.start(worker)

	#
	# Methods for page 3 == Regions and peak fitting
	#
	def peakiso(self):
		# Inner function to receive result from worker
		def result(returned):
			# Saves returned values into Spectra object
			self.spec.wavelength["Isolated"] = returned[0]
			self.spec.intensities["Isolated"] = returned[1]
			self.spec.isolated["Element"] = returned[2]
			self.spec.isolated["Lower"] = returned[3]
			self.spec.isolated["Upper"] = returned[4]
			self.spec.isolated["Center"] = returned[5]
			self.spec.isolated["Noise"] = returned[6]
			self.spec.isolated["Count"] = returned[2].size
			self.spec.isolated["NSamples"] = self.spec.samples["Count"]
			# Enable apply button
			self.gui.p3_isoapply.setEnabled(True)
			# Outputs timer
			print(
				"Timestamp:",
				time(),
				"MSG: Peak isolation count timer: %.2f seconds. "
				% (time() - self.timer),
			)
			# Updates gui elements
			self.gui.g_selector.setCurrentIndex(3)
			self.setgrange()
			self.gui.create_fit_table()
			# Saves iso Table (for environment)
			rows, cols = self.gui.p3_isotb.rowCount(), self.gui.p3_isotb.columnCount()
			self.spec.isolated["Table"] = DataFrame(
				index=range(rows), columns=range(cols), dtype=str
			)
			for r in range(rows):
				for c in range(cols):
					self.spec.isolated["Table"].loc[r, c] = self.gui.p3_isotb.item(
						r, c
					).text()

		# Checks if iso table is complete
		if self.gui.p3_isotb.rowCount() > 0:
			# Checks if values are OK
			if self.gui.checktablevalues(
				self.spec.wavelength["Raw"][0], self.spec.wavelength["Raw"][-1]
			):
				# Update some gui elements
				changestatus(self.gui.sb, "Please Wait. Isolating peaks...", "p", 1)
				self.gui.p3_isoapply.setEnabled(False)
				# Defines if it will use raw or outliers for isolation
				if (
					self.spec.intensities["Outliers"] is None
					or self.spec.intensities["Outliers"] is self.spec.base
				):
					counts = self.spec.intensities["Raw"]
				else:
					if self.spec.intensities["Outliers"][0] is None:
						counts = self.spec.intensities["Raw"]
					else:
						counts = self.spec.intensities["Outliers"]
				elements, lower, upper, center = [], [], [], []
				for tb in range(self.gui.p3_isotb.rowCount()):
					elements.append(self.gui.p3_isotb.item(tb, 0).text())
					lower.append(float(self.gui.p3_isotb.item(tb, 1).text()))
					upper.append(float(self.gui.p3_isotb.item(tb, 2).text()))
					# For center
					center_cell = self.gui.p3_isotb.item(tb, 3).text()
					if ";" in center_cell:
						center.append(
							list(
								map(
									float,
									self.gui.p3_isotb.item(tb, 3).text().split(";"),
								)
							)
						)
					else:
						center.append([float(self.gui.p3_isotb.item(tb, 3).text())])
				self.gui.dynamicbox(
					"Isolating peaks",
					"<b>Please wait</b>. This may take a while...",
					len(elements),
				)
				worker = Worker(
					isopeaks,
					self.spec.wavelength["Raw"],
					counts,
					elements,
					lower,
					upper,
					center,
					self.gui.p3_linear.isChecked(),
					self.gui.p3_norm.isChecked(),
				)
				worker.signals.progress.connect(self.gui.updatedynamicbox)
				worker.signals.finished.connect(
					lambda: self.gui.updatedynamicbox(
						val=0, update=False, msg="Peak isolation finished"
					)
				)
				worker.signals.result.connect(result)
				self.configthread()
				self.timer = time()
				self.threadpool.start(worker)
			else:
				changestatus(self.gui.sb, "Wrong value in isolation table", "r", 1)
		else:
			self.gui.guimsg(
				"Error",
				"Please enter isolation parameters in the <b>table</b> before using this feature.",
				"w",
			)

	def peakfit(self):
		# Inner function to receive result from worker
		def result(returned):
			# Saves result into each corresponding value inside Spectra
			self.spec.fit["NFev"] = returned[0]
			self.spec.fit["Convergence"] = returned[1]
			self.spec.fit["Data"] = returned[2]
			self.spec.fit["Total"] = returned[3]
			self.spec.fit["Height"] = returned[4]
			self.spec.fit["Width"] = returned[5]
			self.spec.fit["Area"] = returned[6]
			self.spec.fit["AreaSTD"] = returned[7]
			self.spec.fit["Shape"] = returned[8]
			# Enable apply button
			self.gui.p3_fitapply.setEnabled(True)
			# Outputs timer
			print(
				"Timestamp:",
				time(),
				"MSG: Peak fitting count timer: %.2f seconds. " % (time() - self.timer),
			)
			# Updates gui elements
			self.gui.g_selector.setCurrentIndex(4)
			self.setgrange()
			# Prepares elements for page 4
			self.gui.p4_peak.clear()
			self.gui.p4_peak.addItems(self.spec.isolated["Element"])
			self.gui.p4_npeak.setEnabled(True)
			# Updates table in page 6
			self.gui.update_tne_values()

		if not self.spec.isolated["Count"]:
			self.gui.guimsg(
				"Error",
				"Please perform peak isolation <b>before</b> using this feature.",
				"w",
			)
		else:
			# Updates gui elements
			changestatus(self.gui.sb, "Please Wait. Performing peak fitting...", "p", 1)
			self.gui.p3_fitapply.setEnabled(False)
			# Iterates over fit table rows to get selected values of shapes and asymmetry
			fittable_rows = self.gui.p3_fittb.rowCount()
			shapes = [
				x.split(")")[1][1:]
				for x in [
					self.gui.p3_fittb.cellWidget(y, 1).currentText()
					for y in range(fittable_rows)
				]
			]
			asymmetry = [
				float(z)
				for z in [
					self.gui.p3_fittb.item(w, 2).text() for w in range(fittable_rows)
				]
			]
			# Run fit function inside pool
			self.gui.dynamicbox(
				"Fitting peaks",
				"<b>Please wait</b>. This may take a while...",
				self.spec.samples["Count"],
			)
			worker = Worker(
				fitpeaks,
				self.spec.wavelength["Isolated"],
				self.spec.intensities["Isolated"],
				shapes,
				asymmetry,
				self.spec.isolated,
				self.gui.p3_mean1st.isChecked(),
			)
			worker.signals.progress.connect(self.gui.updatedynamicbox)
			worker.signals.finished.connect(
				lambda: self.gui.updatedynamicbox(
					val=0, update=False, msg="Peak fitting finished"
				)
			)
			worker.signals.result.connect(result)
			self.configthread()
			self.timer = time()
			self.threadpool.start(worker)

	#
	# Methods for page 4 == Calibration curve
	#
	def docalibrationcurve(self):
		if (
			not self.spec.isolated["Count"]
			and (self.spec.fit["Area"] is self.spec.base)
		) or (self.spec.ref.columns[0] == "Empty"):
			self.gui.guimsg(
				"Warning",
				'You must <i>load references</i> <b>and</b> <i>perform peak fitting</i> <b style="color:red">before</b> using this feature.',
				"w",
			)
		else:
			# Sets parameter to be used: areas or intensities
			param = "Area" if self.gui.p4_areas.isChecked() else "Height"
			values = self.spec.fit[param]
			# Checks the mode of analysis
			if self.gui.p4_wnorm.isChecked():
				mode = "No Norm"
			elif self.gui.p4_pnorm.isChecked():
				mode = "Peak Norm"
			elif self.gui.p4_anorm.isChecked():
				mode = "All Norm"
			else:
				mode = "Equivalent Peak"
			# Defines variables to be passed to linear model function
			noise = self.spec.isolated["Noise"]
			base, base_peak = (
				self.gui.p4_peak.currentText(),
				self.gui.p4_npeak.value() - 1,
			)
			selected, selected_peak = (
				self.gui.p4_pnorm_combo.currentText(),
				self.gui.p4_npeak_norm.value() - 1,
			)
			elements, reference = (
				self.spec.isolated["Element"],
				self.spec.ref[self.gui.p4_ref.currentText()],
			)
			linear = linear_model(
				mode,
				reference,
				values,
				base,
				base_peak,
				selected,
				selected_peak,
				elements,
				noise,
				param,
			)
			self.spec.linear["Reference"] = linear[0]
			self.spec.linear["Predict"] = linear[1]
			self.spec.linear["R2"] = linear[2]
			self.spec.linear["RMSE"] = linear[3]
			self.spec.linear["Slope"] = linear[4]
			self.spec.linear["Intercept"] = linear[5]
			self.spec.linear["LoD"] = linear[6]
			self.spec.linear["LoQ"] = linear[7]
			self.spec.linear["Element"] = linear[0][0]
			# Updates gui elements
			self.gui.g_selector.setCurrentIndex(5)
			self.setgrange()

	#
	# Methods for page 5 == PCA/PLS
	#
	def pca_perform_scan(self):
		# Checks current operation mode
		ok, mode, attribute_matrix = True, "", zeros(0)
		for rb in [
			self.gui.p5_pca_raw,
			self.gui.p5_pca_iso,
			self.gui.p5_pca_areas,
			self.gui.p5_pca_heights,
		]:
			if rb.isChecked():
				mode = rb.text()
				break
		# Gets correct value for attributes, depending on mode
		if mode == "Raw":
			# Checks if samples are imported
			if not self.spec.samples["Count"]:
				self.gui.guimsg(
					"Error",
					'You have to import samples <b style="color: red">before</b> performing components scan!',
					"w",
				)
				ok = False
			else:
				# Raw mode: the attribute matrix is the full spectra
				counts = (
					self.spec.intensities["Outliers"]
					if self.spec.intensities["Outliers"].size > 1
					else self.spec.intensities["Raw"]
				)
				# Now, we need the mean matrix
				meanmatrix = zeros(
					(self.spec.wavelength["Raw"].size, self.spec.samples["Count"])
				)
				for i, c in enumerate(counts):
					meanmatrix[:, i] = c.mean(1)
				# Finally, the attribute matrix is transposed
				attribute_matrix = meanmatrix.T
		elif mode == "Isolated":
			# Checks if isolation were made
			if not self.spec.isolated["Count"]:
				self.gui.guimsg(
					"Error",
					'Please perform peak isolation <b style="color: red">before</b> using this feature.',
					"w",
				)
				ok = False
			else:
				# Isolated mode: the attribute matrix is the concatenation of all isolated peaks
				isolations = [iw.size for iw in self.spec.wavelength["Isolated"]]
				# In isolated mode (different as in raw), the attribute matrix is created in the needed format,
				# with rows = samples, and columns =  attributes (counts for each isolated and averaged peak)
				iso_mean, iso_start = (
					zeros((self.spec.samples["Count"], sum(isolations))),
					0,
				)
				# With iso_mean created, we need now to add values to it
				for iso in self.spec.intensities["Isolated"]:
					for j, sample in enumerate(iso):
						sample_mean = sample.mean(1)
						iso_mean[
							j, iso_start : iso_start + sample_mean.size
						] = sample_mean
					iso_start = sample_mean.shape[0]
				# Defines matrix as input for next part
				attribute_matrix = iso_mean
		elif mode == "Areas":
			# Checks if peak fitting was made
			if self.spec.fit["Shape"] is self.spec.base:
				self.gui.guimsg(
					"Error",
					'Please perform peak fitting <b style="color: red">before</b> using this feature.',
					"w",
				)
				ok = False
			else:
				# Area mode: the attribute matrix is the column concatenation of all areas
				area_matrix = zeros((self.spec.samples["Count"], 1))
				for a in self.spec.fit["Area"]:
					# self.spec.fit['Height']
					area_matrix = column_stack((area_matrix, a))
				# Finally, the attribute matrix is the area_matrix except for column 0
				attribute_matrix = area_matrix[:, 1:]
		else:
			# Checks if peak fitting was made (same for areas)
			if self.spec.fit["Shape"] is self.spec.base:
				self.gui.guimsg(
					"Error",
					'Please perform peak fitting <b style="color: red">before</b> using this feature.',
					"w",
				)
				ok = False
			else:
				# Height mode: the attribute matrix is the column concatenation of all heights
				height_matrix = zeros((self.spec.samples["Count"], 1))
				for h in self.spec.fit["Height"]:
					height_matrix = column_stack((height_matrix, h))
				# Finally, the attribute matrix is the height_matrix except for column 0
				attribute_matrix = height_matrix[:, 1:]
		# With the attribute matrix ready, we are ready for the components scan
		if ok:
			f_attributes, explained_variance, optimum_ncomp = pca_scan(
				attribute_matrix, self.gui.p5_pca_fs.isChecked()
			)
			self.spec.pca["Attributes"] = f_attributes
			self.spec.pca["ExpVar"] = explained_variance
			self.spec.pca["OptComp"] = optimum_ncomp
			self.spec.pca["Mode"] = mode
			# With the results, updates elements in the gui and do the plot
			self.gui.p5_pca_ncomps.setMaximum(len(explained_variance) - 1)
			self.gui.p5_pca_ncomps.setValue(optimum_ncomp)
			self.gui.p5_pca_ncomps.setEnabled(True)
			self.gui.p5_pca_do.setEnabled(True)
			self.gui.g_selector.setCurrentIndex(6)
			self.gui.g_current_sb.setValue(1)
			self.setgrange()

	def pca_do(self):
		if self.spec.pca["Mode"] is None:
			self.gui.guimsg(
				"Error",
				'Please perform PCA scan <b style="color: red">before</b> using this feature.',
				"w",
			)
		else:
			transformed, loadings = pca_do(
				self.spec.pca["Attributes"], self.gui.p5_pca_ncomps.value()
			)
			self.spec.pca["Transformed"] = transformed
			self.spec.pca["Loadings"] = loadings
			# Updates PLS values
			self.spec.pls["NComps"] = self.gui.p5_pca_ncomps.value()
			self.spec.pls[
				"Att"
			] = f'{self.spec.pca["Mode"][0]}-{self.spec.pls["NComps"]}PC{"-FS" if self.gui.p5_pca_fs.isChecked() else ""}'
			self.gui.p5_pls_cal_att.setText(self.spec.pls["Att"])
			self.gui.p5_pls_cal_att.setStyleSheet("color:#000080; font-weight: bold;")
			self.gui.p5_pls_cal_start.setEnabled(True)
			self.gui.g_selector.setCurrentIndex(6)
			self.gui.g_current_sb.setValue(2)
			self.setgrange()

	def pls_do(self):
		if (
			self.spec.pca["Transformed"] is self.spec.base
			or self.spec.ref.columns[0] == "Empty"
		):
			self.gui.guimsg(
				"Warning",
				'You must <i>load references</i> <b>and</b> <i>create attributes from PCA</i> <b style="color:red">before</b> using this feature.',
				"w",
			)
		else:
			# This means all attributes are fine.
			# Now, we must send to PLSR algorithm the reference,
			# number of components and attribute matrix (created in PCA part)
			returned = pls_do(
				self.spec.pca["Transformed"],
				self.spec.ref[self.gui.p5_pls_cal_ref.currentText()],
				self.spec.pls["NComps"],
				self.gui.p5_pca_fs.isChecked(),
			)
			# pls, reference, predicted, residual, predict_r2, predict_rmse, cv_pred, cv_r2, cv_rmse
			self.spec.pls["Element"] = self.gui.p5_pls_cal_ref.currentText()
			self.spec.pls["Samples"] = self.spec.samples["Name"]
			self.spec.pls["Model"] = returned[0]
			self.spec.pls["Reference"] = returned[1]
			self.spec.pls["Predict"] = returned[2]
			self.spec.pls["Residual"] = returned[3]
			self.spec.pls["PredictR2"] = returned[4]
			self.spec.pls["PredictRMSE"] = returned[5]
			self.spec.pls["CrossValPredict"] = returned[6]
			self.spec.pls["CrossValR2"] = returned[7]
			self.spec.pls["CrossValRMSE"] = returned[8]
			# Update graph elements
			self.gui.p5_pls_pred_model.setText(self.gui.p5_pls_cal_ref.currentText())
			self.gui.p5_pls_pred_model.setStyleSheet(
				"color:#000080; font-weight: bold;"
			)
			self.gui.p5_pls_pred_att.setText(self.spec.pls["Att"])
			self.gui.p5_pls_pred_att.setStyleSheet("color:#000080; font-weight: bold;")
			self.gui.p5_pls_pred_start.setEnabled(True)
			self.gui.g_selector.setCurrentIndex(7)
			self.gui.g_current_sb.setValue(1)
			self.setgrange()

	def pls_predict(self):
		if self.spec.pca["Transformed"] is self.spec.base:
			self.gui.guimsg(
				"Warning",
				'You must <i>create attributes from PCA</i> <b style="color:red">before</b> using this feature.',
				"w",
			)
		else:
			# This means all attributes are fine.
			# Now, we just need to predict values usind attributes
			blind_predict = self.spec.pls["Model"].predict(self.spec.pca["Transformed"])
			self.spec.pls["BlindPredict"] = blind_predict
			# Update graph elements
			self.gui.g_selector.setCurrentIndex(7)
			self.gui.g_current_sb.setValue(2)
			self.setgrange()

	#
	# Methods for page 6 == Temperature/Electron Density
	#
	def calc_t_ne(self):
		try:
			# Saves table data into Spectra object (for load/save)
			element = self.gui.p6_element.currentText()
			parameter = self.gui.p6_parameter.currentText()
			df_element = self.gui.p6_table_dfs[element]
			self.spec.plasma["Element"] = element
			self.spec.plasma["Parameter"] = parameter
			self.spec.plasma["Tables"] = self.gui.p6_table_dfs
			self.spec.plasma["Tables"][element] = df_element
			# Checks if TNe table has a minimum size
			min_rows = self.gui.p6_table.rowCount()
			if min_rows <= 2:
				raise AttributeError(
					f"Entered rows ({min_rows}) are not enough to run Saha-Boltzmann plot"
				)
			# Checks if Fit and TNe tables have same size
			fit_rows = self.gui.p3_fittb.rowCount()
			if min_rows != fit_rows:
				raise AttributeError(
					f"T/Ne column does not have the same size ({min_rows}) as Fit/Areas table ({fit_rows}). "
					f"Please perform peak fitting before using this feature"
				)
			# Checks if there are any 0 in gAk and Ek columns
			for col in ("gAk", "Ek"):
				if (df_element[col] == "0").any():
					raise AttributeError(f"Illegal value (zero) found in {col} column")
			# If all passed, now we can actually perform the calculations
			result = tne_do(
				self.spec.samples["Name"],
				array(self.spec.fit[parameter]).T.squeeze(),
				df_element,
				self.gui.p6_ion.text(),
			)
		except Exception as ex:
			self.gui.guimsg(
				"Error",
				f"Could not calculate T/Ne.<p>"
				f'Error message: <b style="color: red">{str(ex)}</b>.</p>',
				"c",
			)
			print_exc()
		else:
			# Saves result
			self.spec.plasma["En"] = result[0]
			self.spec.plasma["Ln"] = result[1]
			self.spec.plasma["Fit"] = result[2]
			self.spec.plasma["Report"] = result[3]
			# Update elements and call plot
			self.gui.g_selector.setCurrentIndex(8)
			self.setgrange()


def spawn_gui():
	root = Path(__file__).parent
	uif = root.joinpath("env", "gui", "libssagui.ui")
	lof = root.joinpath("pic", "libssa.svg")
	QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
	app = QApplication(sys.argv)
	if uif.is_file() and lof.is_file():
		form = LIBSSA2(str(uif), str(lof))
		sys.exit(app.exec())
	else:
		form = LIBSSA2("", "")
		sys.exit(app.exec())


if __name__ == "__main__":
	# Checks the ui file and run LIBSsa main app
	spawn_gui()
