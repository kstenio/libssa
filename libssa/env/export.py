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
from pathlib import Path
from libssa.env.spectra import Spectra
from PySide6.QtWidgets import QTableWidget
from numpy import linspace, array, hstack, zeros
from pandas import DataFrame, Index, ExcelWriter
from openpyxl.utils import get_column_letter as gcl


def export_raw(folder_path: Path, spectra: Spectra, spectra_type: str = 'Raw') -> None:
	"""
	Export RAW function. This function receives a Spectra object and saves all
	spectrum per sample in a single (.txt) file. The function may also receive a
	spectra_type parameter, where it is possible to choose the outliers removed
	version of the Spectra.
	
	:param folder_path: Path object containing the location to save the files
	:param spectra: LIBSsa 2.0 Spectra object
	:param spectra_type: Type of data to export. It can be 'Raw' or 'Outliers'
	:return: None
	"""
	if spectra_type not in ('Raw', 'Outliers'):
		raise AssertionError('Illegal value for spectra type!')
	if not spectra.samples['Count']:
		raise AttributeError('Load data before trying to export it!')
	else:
		w = spectra.wavelength['Raw']
		for c, s in zip(spectra.intensities[spectra_type], spectra.samples['Path']):
			df = DataFrame(
				index=Index(w, name='Wavelength'), data=c,
				columns=[f'Shoot_{x}' for x in range(c.shape[1])])
			df.to_csv(folder_path.joinpath(s.name).with_suffix('.txt'), sep=' ')


def export_iso_table(file_path: Path, widget: QTableWidget) -> None:
	"""
	Export Iso Table function. This function receives a QTableWidget and saves
	the values contained in its cells in a single spreadsheet (.xlsx) file.
	
	:param file_path: Path object containing location and name to save the file
	:param widget: QTableWidget to save data from
	:return: None
	"""
	rows = widget.rowCount()
	cols = widget.columnCount()
	if rows == 0:
		raise AttributeError('Perform peak isolation before using this feature!')
	else:
		writer = ExcelWriter(file_path, engine='openpyxl')
		df = DataFrame(
			index=range(rows),
			columns=['Element', 'Lower WL', 'Upper WL', 'Center WL', '#Peaks'], data='', dtype=str)
		for i in range(rows):
			for j in range(cols):
				df.iloc[i, j] = widget.item(i, j).text()
		df.set_index('Element', drop=True).to_excel(writer, sheet_name='Iso Table')
		resize_writer_columns(writer)
	

def export_iso_peaks(file_path: Path, spectra: Spectra) -> None:
	"""
	Export Iso Peaks function. This function receives a Spectra object and then
	saves all isolated peaks into a single spreadsheet (.xlsx) file.
	The saved file may have as many worksheets as the number of samples multiplied
	by the number of isolated peaks. Each worksheet contains in the columns the
	individual (isolated) spectrum for the peak/region.
	
	:param file_path: Path object containing location and name to save the file
	:param spectra: LIBSsa 2.0 Spectra object
	:return: None
	"""
	isolated_peaks = spectra.isolated['Count']
	if isolated_peaks == 0:
		raise AttributeError('Perform peak isolation before using this feature!')
	else:
		writer = ExcelWriter(file_path, engine='openpyxl')
		for i in range(isolated_peaks):
			w_iso = spectra.wavelength['Isolated'][i]
			for c_iso, s in zip(spectra.intensities['Isolated'][i], spectra.samples['Name']):
				cols = c_iso.shape[1]
				zf = len(str(cols))
				df = DataFrame(data=c_iso, index=w_iso, columns=[f'S_{str(x).zfill(zf)}' for x in range(cols)])
				df.to_excel(writer, sheet_name=s)
		resize_writer_columns(writer)


def export_fit_peaks(file_path: Path, spectra: Spectra) -> None:
	"""
	Export Fit Peaks function. This function receives a Spectra object and then
	saves all data of the averaged isolated peak, plus the adjusted curves into a
	single spreadsheet (.xlsx) file.
	The saved file have 3 worksheets for each isolated region/element:
		* Observed: the averaged observed data/points
		* Residuals: the subtraction of observed and adjusted points
		* Peak-Fitting: the curves obtained with the parameters in the fit equation
	
	:param file_path: Path object containing location and name to save the file
	:param spectra: LIBSsa 2.0 Spectra object
	:return: None
	"""
	if spectra.fit['Area'] is spectra.base:
		raise AttributeError('Perform peak fitting before using this feature!')
	else:
		writer = ExcelWriter(file_path, engine='openpyxl')
		for i, e in enumerate(spectra.isolated['Element']):
			w = spectra.wavelength['Isolated'][i]
			# Creating DFs, each to save a specific variable
			# df1 -> Original (averaged) signal
			# df2 -> Residuals for each fit
			# df3 -> Each peak (and sum) after curve fitting
			columns1 = [f'{s}_Data' for s in spectra.samples['Name']]
			df1 = DataFrame(data=spectra.fit['Data'][i][:, :, 0].T, index=Index(w, name='Wavelength'), columns=columns1)
			columns2 = [f'{s}_Residuals' for s in spectra.samples['Name']]
			df2 = DataFrame(data=spectra.fit['Data'][i][:, :, 1].T, index=Index(w, name='Wavelength'), columns=columns2)
			# To save peak fitting data, another loop is needed
			parameters = spectra.fit['Total'][i].shape
			zero_peaks_matrix = zeros((parameters[1], parameters[0]*parameters[2]))
			columns3 = [''] * parameters[0]*parameters[2]
			for j, t in enumerate(spectra.fit['Total'][i].T):
				columns3[j::parameters[2]] = [f'Sample_{s}_Fit_{j+1}' for s in spectra.samples['Name']]
				zero_peaks_matrix[:, j::parameters[2]] = t
			try:
				df3 = DataFrame(
					data=zero_peaks_matrix,
					index=Index(linspace(w[0], w[-1], 1000), name='Wavelength'), columns=columns3)
			except ValueError:
				df3 = DataFrame(data=zero_peaks_matrix, index=Index(w, name='Wavelength'), columns=columns3)
			# Saves DFs to writer
			df1.to_excel(writer, sheet_name=f'{e}_Observed')
			df2.to_excel(writer, sheet_name=f'{e}_Residuals')
			df3.to_excel(writer, sheet_name=f'{e}_Peak-Fitting')
		resize_writer_columns(writer)


def export_fit_areas(file_path: Path, spectra: Spectra) -> None:
	"""
	Export Fit Areas function. This function receives a Spectra object and then
	saves all report data of the peak fittings into a single spreadsheet (.xlsx) file.
	The saved file have one worksheet for each fitted peak, and contains all the parameters:
		* Lower Wavelength
		* Upper Wavelength
		* #Evaluations
		* Convergence
		* Center of the i-th Peak
		* Width of the i-th Peak
		* Height of the i-th Peak
		* Area of the i-th Peak
		* Standard Deviation of the Area of the i-th Peak
	
	:param file_path: Path object containing location and name to save the file
	:param spectra: LIBSsa 2.0 Spectra object
	:return: None
	"""
	if spectra.fit['Area'] is spectra.base:
		raise AttributeError('Perform peak fitting before using this feature!')
	else:
		writer = ExcelWriter(file_path, engine='openpyxl')
		for i, e in enumerate(spectra.isolated['Element']):
			# Creates empty DF to save report for the specific element
			df = DataFrame(index=Index(spectra.samples['Name'], name='Samples'))
			df['Lower_Wavelength'] = [spectra.isolated['Lower'][i]]*len(df.index)
			df['Upper_Wavelength'] = [spectra.isolated['Upper'][i]]*len(df.index)
			df[f'#Evaluations'] = spectra.fit['NFev'][i]
			df[f'Convergence'] = spectra.fit['Convergence'][i].astype(int)
			# Run into a loop based on number of peaks
			for j in range(spectra.fit['Area'][i].shape[1]):
				df[f'Center_Peak_{j + 1}'] = [spectra.isolated['Center'][i][j]] * len(df.index)
				df[f'Width_Peak_{j + 1}'] = spectra.fit['Width'][i][:, j]
				df[f'Height_Peak_{j + 1}'] = spectra.fit['Height'][i][:, j]
				df[f'Area_Peak_{j + 1}'] = spectra.fit['Area'][i][:, j]
				df[f'AreaSTD_Peak_{j + 1}'] = spectra.fit['AreaSTD'][i][:, j]
			# Now, saves the DF
			shape = spectra.fit['Shape'][i].replace('[', '').replace(']', '')
			df.to_excel(writer, sheet_name=f'{e}_{shape.replace("/", "+")}')
		resize_writer_columns(writer)


def export_linear(file_path: Path, spectra: Spectra) -> None:
	"""
	Export Linear model function. This function receives a Spectra object and then
	saves all parameters and curves of the adjusted Linear Model into a single
	spreadsheet (.xlsx) file.
	The saved file have 2 worksheets, containing:
		* Model: reference, prediction and residual curves
		* Metrics: slope, intercept, RMSE, R2, LoD/Q and the parameter (heights or areas).
	
	:param file_path: Path object containing location and name to save the file
	:param spectra: LIBSsa 2.0 Spectra object
	:return: None
	"""
	if spectra.linear['Predict'] is spectra.base:
		raise AttributeError('Perform Linear Regression before trying to export dada!')
	else:
		# Creates clean DF dict
		df = {x: y for x, y in zip(('Model', 'Metrics'), [DataFrame() for _ in range(2)])}
		element = spectra.linear['Reference'][0]
		reference = spectra.linear['Reference'][1]
		parameter = spectra.linear['Reference'][2]
		# For Model
		df['Model'].index = Index(spectra.samples['Name'], name='Samples')
		df['Model']['Reference'] = reference
		df['Model']['Prediction'] = spectra.linear['Predict'][0][1]
		df['Model']['Residuals'] = df['Model']['Reference'] - df['Model']['Prediction']
		# For Metrics
		df['Metrics'].loc[element, 'Model_Parameter'] = parameter
		df['Metrics'].loc[element, 'Model_R2'] = spectra.linear['R2']
		df['Metrics'].loc[element, 'Model_RMSEC'] = spectra.linear['RMSE']
		df['Metrics'].loc[element, 'Model_Slope'] = spectra.linear['Slope']
		df['Metrics'].loc[element, 'Model_Intercept'] = spectra.linear['Intercept']
		df['Metrics'].loc[element, 'Model_LoD'] = spectra.linear['LoD']
		df['Metrics'].loc[element, 'Model_LoQ'] = spectra.linear['LoQ']
		# Properly saves
		writer = ExcelWriter(file_path, engine='openpyxl')
		for d in df.keys():
			df[d].to_excel(writer, sheet_name=f'{element}_{d}')
		resize_writer_columns(writer)


def export_pls(file_path: Path, spectra: Spectra) -> None:
	"""
	Export PLS model function. This function receives a Spectra object and then
	saves all parameters and curves of the adjusted PLS Model into a single
	spreadsheet (.xlsx) file.
	The saved file have 3 worksheets, containing:
		* Model: reference, prediction, cross validation prediction and residual curves
		* Metrics: RMSE, R2, and attributes of the model
		* Blind: predictions for blind samples using the model
	
	:param file_path: Path object containing location and name to save the file
	:param spectra: LIBSsa 2.0 Spectra object
	:return: None
	"""
	if spectra.pls['Model'] is spectra.base:
		raise AttributeError('Perform PLS Regression before trying to export dada!')
	else:
		# Creates clean DF dict
		df = {x: y for x, y in zip(('Model', 'Metrics', 'Blind'), [DataFrame() for _ in range(3)])}
		# For Model
		df['Model'].index = Index(spectra.pls['Samples'], name='Samples')
		df['Model']['Reference'] = spectra.pls['Reference']
		df['Model']['Prediction'] = spectra.pls['Predict']
		df['Model']['Residuals'] = spectra.pls['Residual']
		df['Model']['CVPrediction'] = spectra.pls['CrossValPredict']
		# For Metrics
		df['Metrics'].loc[spectra.pls['Element'], 'Model_R2'] = spectra.pls['PredictR2']
		df['Metrics'].loc[spectra.pls['Element'], 'Model_RMSEC'] = spectra.pls['PredictRMSE']
		df['Metrics'].loc[spectra.pls['Element'], 'CV_R2'] = spectra.pls['CrossValR2']
		df['Metrics'].loc[spectra.pls['Element'], 'CV_RMSE'] = spectra.pls['CrossValRMSE']
		df['Metrics'].loc[spectra.pls['Element'], 'Attributes'] = spectra.pls['Att']
		# For Blind Prediction
		df['Blind'].index = Index(spectra.samples['Name'], name='Samples')
		if spectra.pls['BlindPredict'] is spectra.base:
			blind = [None] * df['Blind'].index.size
		else:
			blind = spectra.pls['BlindPredict']
		df['Blind']['BlindPrediction'] = blind
		# Properly saves
		writer = ExcelWriter(file_path, engine='openpyxl')
		for d in df.keys():
			df[d].to_excel(writer, sheet_name=d)
		resize_writer_columns(writer)


def export_pca(file_path: Path, spectra: Spectra) -> None:
	"""
	Export PCA function. This function receives a Spectra object and then saves all
	generated data of a Principal Components Analysis (PCA) into a single spreadsheet (.xlsx) file.
	The saved file have 3 worksheets:
		* Explained Variance: the explained cumulative variance as function of attributes/samples
		* Scores: the data points in the principal components space
		* Loadings: its values as functions of the attributes/regions/wavelengths
	
	:param file_path: Path object containing location and name to save the file
	:param spectra: LIBSsa 2.0 Spectra object
	:return: None
	"""
	if spectra.pca['Loadings'] is spectra.base:
		raise AttributeError('Perform PCA algorythm before trying to export dada!')
	else:
		# Saves useful variables
		mode = spectra.pca['Mode']
		t_samples = spectra.samples['Count']
		n_samples = Index(spectra.samples['Name'], name='Samples')
		components = Index(range(1, t_samples+1), name='Components')
		w = spectra.wavelength[mode] if mode in ('Raw', 'Isolated') else range(1, spectra.pca['Loadings'].shape[0]+1)
		# Explained Variance
		df1 = DataFrame({'Cumulative ExpVar': spectra.pca['ExpVar']}, index=components)
		# Scores
		pcs = spectra.pca['Transformed']
		df2 = DataFrame(data=pcs, index=n_samples, columns=[f'PC_{x+1}' for x in range(pcs.shape[1])])
		# Loadings
		if mode == 'Isolated':
			att = array([])
			for w_ in w:
				att = hstack((att, w_))
		else:
			att = array(w)
		sort = att.argsort()
		att = att[sort]
		loadings = spectra.pca['Loadings'][sort, :]
		df3 = DataFrame(
			data=loadings,
			index=Index(att[sort], name=mode), columns=[f'Loading_{x+1}' for x in range(loadings.shape[1])])
		# Creates Writer and saves each DF into the writer
		writer = ExcelWriter(file_path, engine='openpyxl')
		df1.to_excel(writer, sheet_name='Explained Variance')
		df2.to_excel(writer, sheet_name='Scores')
		df3.to_excel(writer, sheet_name='Loadings')
		resize_writer_columns(writer)


def export_tne(file_path: Path, spectra: Spectra) -> None:
	"""
	Export T/Ne function. This function receives a Spectra object and then saves all
	generated data of a Saha-Boltzmann plot (in the case, plasma temperature and electrons density)
	into a single spreadsheet (.xlsx) file.
	The saved file have 2 worksheets:
		* Report: a table containing values of T, Ne, R2, R and deviations for each sample
		* Saha-Boltzmann Plot: the plot for all samples. Contains the Ln's, Energies and adjusted curve
	
	:param file_path: Path object containing location and name to save the file
	:param spectra: LIBSsa 2.0 Spectra object
	:return: None
	"""
	if spectra.plasma['Report'] is spectra.base:
		raise AttributeError('Run Saha-Boltzmann plot before trying to export dada!')
	else:
		writer = ExcelWriter(file_path, engine='openpyxl')
		# We will save 2 worksheets: one for report, and another for the curves
		df1 = spectra.plasma['Report']
		# Although the 1st one was easy, the second is a bit more tricky
		samples = df1.index.tolist()
		x = spectra.plasma['En'].T
		y = spectra.plasma['Ln'].T
		fit = spectra.plasma['Fit'].T
		zero_t_matrix = zeros((x.shape[0], 3 * x.shape[1]))
		column_names, j = [''] * 3 * x.shape[1], 0
		for i in range(0, 3 * x.shape[1], 3):
			zero_t_matrix[:, i+0] = x[:, j]
			zero_t_matrix[:, i+1] = y[:, j]
			zero_t_matrix[:, i+2] = fit[:, j]
			column_names[i] = f'Sample_{samples[j]}_En'
			column_names[i+1] = f'Sample_{samples[j]}_Ln'
			column_names[i+2] = f'Sample_{samples[j]}_Fit'
			j += 1
		df2 = DataFrame(data=zero_t_matrix, columns=column_names)
		# Saves DFs
		df1.to_excel(writer, sheet_name='Report')
		df2.to_excel(writer, index=False, sheet_name='Saha-Boltzmann Plot')
		resize_writer_columns(writer)


def export_correl(file_path: Path, spectra: Spectra) -> None:
	"""
	Export Correl function. This function receives a Spectra object and then saves all
	generated data of a Pearson Correlation Spectrum for all elements/parameters entered
	by the user (in the reference spreadsheet). The spectra are saved into a single spreadsheet (.xlsx) file.
	
	:param file_path: Path object containing location and name to save the file
	:param spectra: LIBSsa 2.0 Spectra object
	:return: None
	"""
	if spectra.pearson['Data'] is spectra.base:
		raise AttributeError('Perform Correlation Spectrum routine before trying to export dada!')
	else:
		writer = ExcelWriter(file_path, engine='openpyxl')
		exdf = DataFrame(
			index=Index(spectra.wavelength['Raw'], name='Wavelength'),
			columns=[f'{chr(961)}_{x}' for x in spectra.ref.columns],
			data=spectra.pearson['Data'])
		exdf.insert(0, 'Full Mean', spectra.pearson['Full-Mean'])
		exdf.to_excel(writer, sheet_name='Correlation')
		resize_writer_columns(writer)


def resize_writer_columns(writer: ExcelWriter, close: bool = True) -> None:
	"""
	Resize Writer Columns function. This is a helper function, which receives a pandas
	ExcelWriter, walks into each column of all worksheets and resizes the columns based on
	header name.
	The function also may avoid closing the writer.
	
	:param writer: ExcelWriter to have the columns resized before saving the .xlsx file
	:param close: boolean to decide whether close the writer or not
	:return: None
	"""
	for w in writer.sheets:
		worksheet = writer.sheets[w]
		for col in worksheet.iter_cols():
			name = col[0].value
			if type(name) is str:
				worksheet.column_dimensions[gcl(col[0].column)].width = max(10, int(len(name) * 1.8))
	if close:
		writer.close()
