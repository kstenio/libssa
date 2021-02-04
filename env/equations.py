#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  equations.py
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

from numpy import empty, array, sum

def lorentz(x, *p):
	peaks = len(p) // 3
	lo = empty((len(x), peaks))
	for i in range(peaks):
		h, w, c = p[3 * i], p[(3 * i) + 1], p[(3 * i) + 2]
		lo[:, i] = abs(h) / (1 + ((x - c) / (0.5 * w)) ** 2)
	return sum(lo, 1)

