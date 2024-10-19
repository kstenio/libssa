<p align="center">
	<img alt="libssa_logo" src="https://raw.githubusercontent.com/kstenio/libssa/master/src/libssa/pic/libssa.svg" width="500em">
</p>

# LIBSsa2 - Laser Induced Breakdown Spectroscopy spectra analyzer

[![PyPI - Python Version](https://badgen.net/pypi/python/libssa/?color=5500d4)](https://www.python.org/downloads/)
[![GitHub - Commits](https://badgen.net/github/commits/kstenio/libssa/?color=6c037f&icon=github)](https://github.com/kstenio/libssa/commits/)
[![GitHub - Contributors](https://badgen.net/github/contributors/kstenio/libssa/?color=902da6&icon=github)](https://github.com/kstenio/libssa/graphs/contributors)
[![GitHub - Releases](https://badgen.net/github/release/kstenio/libssa/?color=6865aa&icon=github)](https://github.com/kstenio/libssa/releases)
[![PyPI - Release](https://badgen.net/pypi/v/libssa/?color=0507ee&icon=pypi)](https://pypi.org/project/libssa/)
[![GitHub - License](https://badgen.net/github/license/kstenio/libssa/?color=05c8fe)](https://www.gnu.org/licenses/agpl-3.0.html.en)

**LIBSsa 2** is free software, licensed under the **GNU Affero General Public License version 3**,
and written in **Python 3.x** for analyzing **LIBS spectra**. It can read several formats of data inside raw/text files,
import the spectra, and perform multiple analyses on the data. The environment (spectra, peaks, and results) may also be saved
into an encapsulated **lb2e** file.

<p align="center">
	<img alt="libssa_mainwindow" src="https://raw.githubusercontent.com/kstenio/libssa/master/src/libssa/pic/examples/libssa.png" width="900em"><br>
	<i>LIBSsa main window</i>
</p>

For a full list of features implemented in LIBSsa, you may check the [FEATURES.md](https://github.com/kstenio/libssa/blob/master/FEATURES.md) file but, in short, you can:
remove outliers using SAM or MAD algorithms, perform full spectrum normalization (FSN), create correlation spectrum,
do peak isolation, peak fitting (Gaussian, Lorentzian, and Voigt), univariate linear models, multivariate partial least
squares regression (PLSR), principal components analysis (PCA), and obtain plasma temperature and electron density values
using Saha-Boltzmann (modified to LIBS) equation.

Bellow are presented some of the graphics generated by LIBSsa.
<p align="center">
	<img alt="libssa_graphics" src="https://raw.githubusercontent.com/kstenio/libssa/master/src/libssa/pic/examples/montage.png" width="900em"><br>
	<i>Some treatments available in LIBSsa: peak isolation (a), peak fitting (b), PCA (c), and Saha-Boltzmann plot (d)</i>
</p>

Finally, users can also export the results of the analysis in many common formats (**txt**, **csv**, and **xlsx**).

## Setting up the environment

You will need to install Python 3 to use the program (tested on 3.9 and 3.10 with current libraries). Python can be obtained from
the official website, [https://www.python.org/](https://www.python.org/) and, if you have any additional inquiries, there are
official instructions on how install Python on [Linux Distributions](https://docs.python.org/3/using/unix.html),
[Windows](https://docs.python.org/3/using/windows.html) and [macOS](https://docs.python.org/3/using/mac.html).

### 1. Simple install (PyPI version)

LIBSsa is distributed as a [Python Package](https://pypi.org/project/libssa/) on **PyPI**. With Python and [PIP](https://docs.python.org/3/installing/index.html)
installed, just run from inside a **terminal** or **Windows PowerShell** and type:

```shell
pip install libssa
libssa-gui
```

### 2. SRC install (GitHub version)

If you prefer interacting with the source code of LIBSsa, you may download the [software zip](https://github.com/kstenio/libssa/archive/refs/heads/master.zip),
or clone the repository using [git](https://git-scm.com/):

```shell
git clone https://github.com/kstenio/libssa.git
```

Then, you can use PIP to install LIBSsa in editable mode :

```shell
cd libssa
pip install -e .
libssa-gui
```

In editable mode, every change made to the source code will also be reflected into the package. Doing this, you'll also
install the following **_external libraries_** that LIBSsa uses:

1. [NumPy](https://numpy.org/) (~=1.25.1)
2. [SciPy](https://scipy.org/) (~=1.11.1)
3. [Pandas](https://pandas.pydata.org/) (~=2.0.3)
4. [Scikit-Learn](https://scikit-learn.org/stable/) (~=1.3.0)
5. [PySide6](https://wiki.qt.io/Qt_for_Python) (~=6.4.3)
6. [PyQtGraph](https://pyqtgraph.readthedocs.io/en/latest/index.html) (~=0.13.3)
7. [OpenPyXL](https://openpyxl.readthedocs.io/en/stable/) (~=3.1.2)
8. [Psutil](https://github.com/giampaolo/psutil) (~=5.9.5)
9. [Markdown](https://python-markdown.github.io/) (~=3.4.3)

Lastly, advanced users are encouraged to use [venv](https://docs.python.org/3/library/venv.html) (Virtual Environment).

## Contributing

If you wish to contribute to the development of LIBSsa, please check for the guidelines in the
[CONTRIBUTING.md](https://github.com/kstenio/libssa/blob/master/CONTRIBUTING.md) file.

## Warranty

LIBSsa 2 is an open-source project. It is distributed in the hope that it will be
useful, but *WITHOUT ANY WARRANTY*; without even the implied warranty of *MERCHANTABILITY*
or *FITNESS FOR A PARTICULAR PURPOSE*. See the GNU Affero General Public License
version 3 [attached](./LICENSE.txt) for more details.

## Historical background

The **LIBSsa 1** was a software created in the middle of 2017 for my personal use in a LIBS class during my doctorate.
Eventually, many colleagues from the _Optics and Photonics Laboratory_ at [Embrapa Instrumentation](https://www.embrapa.br/en/instrumentacao)
(Sao Carlos, SP, Brazil) enjoyed the application, and I continued developing it until late 2019.

At some point, the _LIBSsa_ software became an important part of my [doctorate/thesis](https://repositorio.ufscar.br/handle/ufscar/18072),
so I decided to restructure it into a new - _better_ - version. Finally, in the middle of 2020,
the development of **LIBSsa 2** started.

## Acknowledgements

The present software (up to version 2.0.99) was supported by the Coordination for the Improvement
of Higher Education Personnel - Brazil (CAPES) - Finance Code 001, and by the Laboratory of Optics and Photonics
at Embrapa Instrumentation, under the supervision of Dr. Debora Milori.

## Copyright

You are free to use and redistribute LIBSsa 2 (and are, in fact, encouraged to do so), provided that
proper credit is given to the developer and/or this repository is mentioned. The software is licensed under the AGPLv3.

To ensure the open-source nature of LIBSsa 2 and prevent any attempt to transform it into proprietary software, the source code
of a previous version (2.0.99) has been registered with the Brazilian National Institute of Industrial Property (INPI-BR).
This registration provides an additional layer of protection in accordance with the principles of the
*[TRIPS Agreement](https://www.wto.org/english/tratop_e/trips_e/intel2_e.htm)* and is documented under the process number *BR 51 2023 002165-2*.

LIBSsa also uses content from other projects: SVG icons are from [Font Awesome](https://fontawesome.com/), and the logo
is based on the [PT_Sans font](https://fonts.google.com/specimen/PT+Sans). License to those content are available in the
[doc/open_source_licenses](./doc/open_source_licenses) folder.

---

Developed by: [Kleydson Stenio](mailto:9257942+kstenio@users.noreply.github.com?Subject=LIBSsa_QUESTIONS) @ 2024
