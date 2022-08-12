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

import numpy as np
import pandas as pd
from pathlib import Path
from env.spectra import Spectra


def export_raw(folder_path: Path, spectra: Spectra):
	if not spectra.samples['Count']:
		raise AttributeError('Load data before trying to export it!')
	else:
		w = spectra.wavelength['Raw']
		for c, s in zip(spectra.intensities['Raw'], spectra.samples['Path']):
			df = pd.DataFrame(index=pd.Index(w, name='Wavelength'), data=c,
			                  columns=[f'Shoot_{x}' for x in range(c.shape[1])])
			df.to_csv(folder_path.joinpath(s.name), sep=' ')
			

def export_pls(file_path: Path, spectra: Spectra):
	if spectra.pls['Model'] is spectra.base:
		raise AttributeError('Perform PLS Regression before trying to export dada!')
	else:
		"""self.pls = {'Element': self.base, 'Model': self.base, 'NComps': 0, 'Reference': self.base,
		            'Predict': self.base, 'Residual': self.base, 'PredictR2': self.base, 'PredictRMSE': self.base,
		            'CrossValPredict': self.base, 'CrossValR2': self.base, 'CrossValRMSE': self.base, 'BlindPredict': self.base}"""
		# Creates clean df dict
		df = {x: y for x, y in zip(('Model', 'Metrics', 'Blind'), [pd.DataFrame() for _ in range(3)])}
		# For Model
		df['Model'].index = pd.Index(spectra.pls['Samples'], name='Samples')
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
		df['Blind'].index = pd.Index(spectra.samples['Name'], name='Samples')
		if spectra.pls['BlindPredict'] is spectra.base:
			blind = [None] * df['Blind'].index.size
		else:
			blind = spectra.pls['BlindPredict']
		df['Blind']['BlindPrediction'] = blind
		# Properly saves
		writer = pd.ExcelWriter(file_path, engine='openpyxl')
		for d in df.keys():
			df[d].to_excel(writer, sheet_name=d)
		writer.save()
		writer.close()

		
def export_correl(file_path: Path, spectra: Spectra):
	pass
