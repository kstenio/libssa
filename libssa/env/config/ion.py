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


ionization_energies_ev = {
	"H": 13.5984345997,
	"He": 24.587389011,
	"Li": 5.391714996,
	"Be": 9.322699,
	"B": 8.298019,
	"C": 11.260288,
	"N": 14.53413,
	"O": 13.618055,
	"F": 17.42282,
	"Ne": 21.564541,
	"Na": 5.13907696,
	"Mg": 7.646236,
	"Al": 5.985769,
	"Si": 8.15168,
	"P": 10.486686,
	"S": 10.36001,
	"Cl": 12.967633,
	"Ar": 15.7596119,
	"K": 4.34066373,
	"Ca": 6.11315547,
	"Sc": 6.56149,
	"Ti": 6.82812,
	"V": 6.746187,
	"Cr": 6.76651,
	"Mn": 7.434038,
	"Fe": 7.9024681,
	"Co": 7.88101,
	"Ni": 7.639878,
	"Cu": 7.72638,
	"Zn": 9.394197,
	"Ga": 5.999302,
	"Ge": 7.899435,
	"As": 9.78855,
	"Se": 9.752392,
	"Br": 11.81381,
	"Kr": 13.9996055,
	"Rb": 4.1771281,
	"Sr": 5.69486745,
	"Y": 6.21726,
	"Zr": 6.634126,
	"Nb": 6.75885,
	"Mo": 7.09243,
	"Tc": 7.11938,
	"Ru": 7.3605,
	"Rh": 7.4589,
	"Pd": 8.336839,
	"Ag": 7.576234,
	"Cd": 8.99382,
	"In": 5.7863558,
	"Sn": 7.343918,
	"Sb": 8.608389,
	"Te": 9.009808,
	"I": 10.45126,
	"Xe": 12.1298437,
	"Cs": 3.8939057274,
	"Ba": 5.2116646,
	"La": 5.5769,
	"Ce": 5.5386,
	"Pr": 5.4702,
	"Nd": 5.525,
	"Pm": 5.58187,
	"Sm": 5.643722,
	"Eu": 5.670385,
	"Gd": 6.1498,
	"Tb": 5.8638,
	"Dy": 5.93905,
	"Ho": 6.0215,
	"Er": 6.1077,
	"Tm": 6.18431,
	"Yb": 6.25416,
	"Lu": 5.425871,
	"Hf": 6.82507,
	"Ta": 7.549571,
	"W": 7.86403,
	"Re": 7.83352,
	"Os": 8.43823,
	"Ir": 8.96702,
	"Pt": 8.95883,
	"Au": 9.225554,
	"Hg": 10.437504,
	"Tl": 6.1082873,
	"Pb": 7.4166799,
	"Bi": 7.285516,
	"Po": 8.41807,
	"At": 9.31751,
	"Fr": 4.0727411,
	"Ra": 5.2784239,
	"Ac": 5.380226,
	"Th": 6.3067,
	"Pa": 5.89,
	"U": 6.19405,
	"Np": 6.26554,
	"Pu": 6.02576,
	"Am": 5.97381,
	"Cm": 5.99141,
	"Bk": 6.19785,
	"Cf": 6.28166,
	"Es": 6.36758,
	"Fm": 6.5,
	"Md": 6.58,
	"No": 6.62621,
	"Lr": 4.96,
	"Rf": 6.02,
	"Db": 6.8,
	"Sg": 7.8,
	"Bh": 7.7,
	"Hs": 7.6
}

# # THIS IS A BACKUP CODE OF HOW I DID GET ALL PREVIOUS VALUES FOR E_ION
# from mendeleev import elements
# import pandas as pd
# from time import sleep
# # Fetch each possible Ionization energy
# link_ion_energy = 'https://physics.nist.gov/cgi-bin/ASD/ie.pl?spectra={element}+I&submit=Retrieve+Data&units=1&format=0&order=0&at_num_out=on&sp_name_out=on&ion_charge_out=on&el_name_out=on&seq_out=on&shells_out=on&level_out=on&ion_conf_out=on&e_out=0&unc_out=on&biblio=on'
# df_ion_energy = pd.DataFrame(index=elements.__all__, columns=['Ionization Energy (eV)', 'Uncertainty (eV)'], dtype=str)
# for e in df_ion_energy.index:
# 	print(e)
# 	try:
# 		df = pd.read_html(link_ion_energy.format(element=e))[1].astype(str)
# 		val1 = df['Ionization Energy (eV)'][0]
# 		val2 = df['Uncertainty\xa0(eV)'][0]
# 	except Exception as ex:
# 		print(str(ex))
# 	else:
# 		df_ion_energy.loc[e] = [val1, val2]
# 		sleep(0.15)
