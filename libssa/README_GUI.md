# LIBSsa2 - Laser Induced Breakdown Spectroscopy spectra analyzer

### Current stable version: _2.1_

## About the software

**LIBSsa 2** is free software, licensed under the **GNU Affero General Public License version 3**, 
and written in **Python 3.x** for analyzing **LIBS spectra**. It can read multiple formats of data inside raw/text files,
import the spectra, and perform multiple analyses on the data. The environment (spectra, peaks, and results) may be saved into an encapsulated **lb2e** file.
Finally, users can also export the results of the analysis in many common formats (**txt**, **csv**, and **xlsx**).

## Features

1. **Importing Spectra**: Users can import data into LIBSsa 2 from any kind of raw/text data, including **txt**, **csv**, **esf**, and **ols**.
There are also many options for how data can be loaded:
   1. **Load methods**: How files are read by the program
      1. **Multi**: One folder per sample, several files per sample
      2. **Single**: One file per sample, multiple columns in each file
   2. **Delimiters**: TAB ("**\t**"), SPACE ("**\s+**"), comma ("**,**"), and semicolon ("**;**")
   3. **Header**: Number of rows to skip
   4. **Wavelength and Counts**: Columns containing the wavelength and counts data
   5. **Decimals**: If the user wants to round the loaded signal (for improved performance)
   6. **FSN** (Full Spectrum Normalization): Can use signal information during the loading for normalization
2. **Outliers Removal**: There are 2 algorithms for outliers removal in LIBSsa 2:
   1. **SAM** (Spectral Angle Mapper): Removes outliers based on how different a sample is from the average
   2. **MAD** (Median Absolute Deviation): Removes outliers based on a per-wavelength criterion
3. **Correlation Spectrum**: If a reference is provided, calculates Pearson-R as a function of wavelength
4. **Peak Isolation**: Can isolate multiple peaks at once
5. **Peak Fitting**: Can perform peak fitting to obtain areas and heights for multiple functions/curves:
   1. Lorentzian
   2. Gaussian
   3. Voigt
   4. Trapezoidal*
6. **Linear Regression**: Can use one or two peaks for obtaining linear models
7. **PLS Regression**: Can create models and predict blind samples
8. **PCA** (Principal Components Analysis): Can run PCA on the dataset, using RAW data or fitted data
9. **Plasma Parameters**: By using the Saha-Boltzmann equation, can obtain plasma temperature (**T [K]**) and electron density (**Ne [cm-3]**)
10. **Save Environment**: If the user wants to keep all analysis in a single file, it is possible to save a _LIBSsa 2 environment file_ (**lb2e**).
The file is a lzma-compressed pickle containing all the data loaded and processed, with about **40%** of the size of the original/text spectra.
11. **Export Data**: It is also possible to export analyzed data into **csv** and **xlsx** files.

## Installing Python

You will need to install Python 3.x to use the program (tested on 3.9 with current libraries).
Python can be obtained from the official website: [https://www.python.org/](https://www.python.org/).

### 1. Linux Users

If you use **Linux**, you probably already have it, as most modern distributions come with Python pre-installed.
However, if for some reason Python 3 is not installed, you'll have to install it either from the website or from your distribution repository.
As an example, for Debian-based distributions, you can use **apt** (_Advanced Package Tool_):

```bash
sudo apt install python3-minimal python3-pip python3-setuptools python3-wheel build-essential
```

In case of any problems, check the official documentation about [installing Python on
Unix platforms](https://docs.python.org/3/using/unix.html).

### 2. Windows users

**Windows** users may obtain Python either from the [Microsoft Store](https://apps.microsoft.com/store/detail/python-39/9P7QFQMJRFP7)
(if you use Windows 8+) or by downloading it from the [official website](https://www.python.org).
Also, one should not forget to mark during the installation to *ADD PYTHON TO PATH* and
to _REMOVE MAX PATH 260 LENGTH LIMIT_.

I also recommend checking the official documentation about [installing Python on
Windows platforms](https://docs.python.org/3/using/windows.html).

## External Libraries

To work properly, this program uses the following external libraries:

1. [NumPy](https://numpy.org/) (tested on ~=1.22.3 and ~=1.25.1)
2. [SciPy](https://scipy.org/) (tested on ~=1.8.0 and ~=1.11.1)
3. [Pandas](https://pandas.pydata.org/) (tested on ~=1.4.1 and ~=2.0.3)
4. [Scikit-Learn](https://scikit-learn.org/stable/) (tested on ~=1.1.2 and ~=1.3.0)
5. [PySide6](https://wiki.qt.io/Qt_for_Python) (tested on ~=6.2.3 and ~=6.4.3)
6. [PyQtGraph](https://pyqtgraph.readthedocs.io/en/latest/index.html) (tested on ~=0.12.4 and ~=0.13.3)
7. [OpenPyXL](https://openpyxl.readthedocs.io/en/stable/) (tested on ~=3.0.5 and ~=3.1.2)
8. [Psutil](https://github.com/giampaolo/psutil) (tested on ~=5.9.1 and ~=5.9.5)
9. [Markdown](https://python-markdown.github.io/) (tested on ~3.4.1 and ~=3.4.3)

And, besides those libraries, its dependencies as well.

### Installing external libraries

External libraries can be installed using the [PIP](https://docs.python.org/3/installing/index.html)
tool and the file _**requirements.txt**_. Just open a **terminal** or **Windows PowerShell**
and type:

```powershell
pip install -r requirements.txt --user
```

With the command above, you'll install all the needed libraries in a compatible (_tested_)
version of the program. You may also install them directly, but be aware that this may lead
to **unstable behaviour**:

```powershell
pip install numpy scipy pandas scikit-learn PySide6 pyqtgraph openpyxl psutil markdown --user
```

You may also use `python -m pip install [COMMAND]` for installing libraries. Finally,
advanced users are encouraged to use [venv](https://docs.python.org/3/library/venv.html)
(Virtual Environment).

## Historical background

The **LIBSsa 1** was a software created in the middle of 2017 for my personal use in a LIBS class during my doctorate.
Eventually, many colleagues from the _Optics and Photonics Laboratory_ at [Embrapa Instrumentation](https://www.embrapa.br/en/instrumentacao)
(Sao Carlos, SP, Brazil) enjoyed the application, and I continued developing it until late 2019.

At some point, the _LIBSsa_ software became an important part of my [doctorate/thesis](https://repositorio.ufscar.br/handle/ufscar/18072),
so I decided to restructure it into a new - _better_ - version. Finally, in the middle of 2020,
the development of **LIBSsa 2** started.

## Acknowledgements

The present software (up to version 2.0.99) was supported by the Coordination for the Improvement
of Higher Education Personnel - Brazil (CAPES) - Finance Code 001, and by Embrapa Instrumentation.

## Warranty

LIBSsa 2 is an open-source project. It is distributed in the hope that it will be
useful, but *WITHOUT ANY WARRANTY*; without even the implied warranty of *MERCHANTABILITY*
or *FITNESS FOR A PARTICULAR PURPOSE*. See the GNU Affero General Public License
version 3 attached for more details.

## Copyright

You are free to use and redistribute LIBSsa 2 (and are, in fact, encouraged to do so), provided that proper credit is given to the developer
and/or this repository is mentioned. Please be aware that the source code (v2.0.99) is registered with the Brazilian National Institute of
Industrial Property (INPI-BR) *– a member of the [TRIPS Agreement](https://www.wto.org/english/tratop_e/trips_e/intel2_e.htm) –* under
the process number BR512023002165-2.

---

Developed by: [Kleydson Stenio](mailto:kleydson.stenio@gmail.com?Subject=LIBSsa_QUESTIONS) @ 2023
