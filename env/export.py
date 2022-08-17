#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  ./env/export.py
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
from pathlib import Path
from numpy import linspace, array, hstack, zeros
from env.spectra import Spectra
from PySide6.QtWidgets import QTableWidget
from pandas import DataFrame, Index, ExcelWriter
from openpyxl.utils import get_column_letter as gcl


# Export Functions
def export_raw(folder_path: Path, spectra: Spectra, spectra_type: str = 'Raw'):
	if spectra_type not in ('Raw', 'Outliers'):
		raise AssertionError('Illegal value for spectra type!')
	if not spectra.samples['Count']:
		raise AttributeError('Load data before trying to export it!')
	else:
		w = spectra.wavelength['Raw']
		for c, s in zip(spectra.intensities[spectra_type], spectra.samples['Path']):
			df = DataFrame(index=Index(w, name='Wavelength'), data=c,
			                  columns=[f'Shoot_{x}' for x in range(c.shape[1])])
			df.to_csv(folder_path.joinpath(s.name), sep=' ')


def export_iso_table(file_path: Path, widget: QTableWidget):
	rows = widget.rowCount()
	cols = widget.columnCount()
	if rows == 0:
		raise AttributeError('Perform peak isolation before using this feature!')
	else:
		writer = ExcelWriter(file_path, engine='openpyxl')
		df = DataFrame(index=range(rows), columns=['Element', 'Lower WL', 'Center WL', 'Upper WL', '#Peaks'], data='', dtype=str)
		for i in range(rows):
			for j in range(cols):
				df.iloc[i, j] = widget.item(i, j).text()
		df.set_index('Element', drop=True).to_excel(writer, sheet_name='Iso Table')
		resize_writer_columns(writer)
	

def export_iso_peaks(file_path: Path, spectra: Spectra):
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
			writer.save()
		resize_writer_columns(writer)


def export_fit_peaks(file_path: Path, spectra: Spectra):
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
				df3 = DataFrame(data=zero_peaks_matrix, index=Index(linspace(w[0], w[-1], 1000), name='Wavelength'), columns=columns3)
			except ValueError:
				df3 = DataFrame(data=zero_peaks_matrix, index=Index(w, name='Wavelength'), columns=columns3)
			# Saves DFs to writer
			df1.to_excel(writer, sheet_name=f'{e}_Observed')
			df2.to_excel(writer, sheet_name=f'{e}_Residuals')
			df3.to_excel(writer, sheet_name=f'{e}_Peak-Fitting')
			writer.save()
		resize_writer_columns(writer)


def export_fit_areas(file_path: Path, spectra: Spectra):
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
			writer.save()
		resize_writer_columns(writer)


def export_linear(file_path: Path, spectra: Spectra):
	if spectra.linear['Predict'] is spectra.base:
		raise AttributeError('Perform Linear Regression before trying to export dada!')
	else:
		# Creates clean df dict
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
		writer.save()
		resize_writer_columns(writer)


def export_pls(file_path: Path, spectra: Spectra):
	if spectra.pls['Model'] is spectra.base:
		raise AttributeError('Perform PLS Regression before trying to export dada!')
	else:
		# Creates clean df dict
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
		writer.save()
		resize_writer_columns(writer)


def export_pca(file_path: Path, spectra: Spectra):
	if spectra.pca['ExpVar'] is spectra.base:
		raise AttributeError('Perform PCA algorythm before trying to export dada!')
	else:
		# Saves useful variables
		mode = spectra.pca['Mode']
		t_samples = spectra.samples['Count']
		components = Index(range(1, t_samples+1), name='Components')
		w = spectra.wavelength[mode] if mode in ('Raw', 'Isolated') else range(1, t_samples+1)
		# Explained Variance
		df1 = DataFrame({'Cumulative ExpVar': spectra.pca['ExpVar']}, index=components)
		# Scores
		pcs = spectra.pca['Transformed']
		df2 = DataFrame(data=pcs, index=components, columns=[f'PC_{x+1}' for x in range(pcs.shape[1])])
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
		df3 = DataFrame(data=loadings, index=Index(att[sort], name=mode), columns=[f'Loading_{x+1}' for x in range(loadings.shape[1])])
		# Creates Writer and saves each df into the writer
		writer = ExcelWriter(file_path, engine='openpyxl')
		df1.to_excel(writer, sheet_name='Explained Variance')
		df2.to_excel(writer, sheet_name='Scores')
		df3.to_excel(writer, sheet_name='Loadings')
		writer.save()
		resize_writer_columns(writer)


def export_tne(file_path: Path, spectra: Spectra):
	if spectra.pearson['Data'] is spectra.base:
		raise AttributeError('Perform Correlation Spectrum routine before trying to export dada!')
	else:
		writer = ExcelWriter(file_path, engine='openpyxl')
		exdf = DataFrame(index=Index(spectra.wavelength['Raw'], name='Wavelength'),
		                 columns=[f'{chr(961)}_{x}' for x in spectra.ref.columns],
		                 data=spectra.pearson['Data'])
		exdf.to_excel(writer, sheet_name='Correlation')
		writer.save()
		resize_writer_columns(writer)


def export_correl(file_path: Path, spectra: Spectra):
	if spectra.pearson['Data'] is spectra.base:
		raise AttributeError('Perform Correlation Spectrum routine before trying to export dada!')
	else:
		writer = ExcelWriter(file_path, engine='openpyxl')
		exdf = DataFrame(index=Index(spectra.wavelength['Raw'], name='Wavelength'),
		                 columns=[f'{chr(961)}_{x}' for x in spectra.ref.columns],
		                 data=spectra.pearson['Data'])
		exdf.to_excel(writer, sheet_name='Correlation')
		writer.save()
		resize_writer_columns(writer)


def resize_writer_columns(writer: ExcelWriter, close: bool = True):
	for w in writer.sheets:
		wsheet = writer.sheets[w]
		for col in wsheet.iter_cols():
			name = col[0].value
			if type(name) is str:
				wsheet.column_dimensions[gcl(col[0].column)].width = max(10, int(len(name) * 1.5))
	if close:
		writer.close()
