## LIBSsa Features

This file provides a full list of LIBSsa implemented features:

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

## Additional information on the features

If you encounter any issues on how to use LIBSsa, or how the features mentioned above works, I describe them thoroughly in my 
[thesis](https://repositorio.ufscar.br/handle/ufscar/18072) (chapter 9). Please be aware tha the text is writen in _Brazilian Portuguese_. 

## LIBSsa flowchart

Figure above shows a usual workflow of LIBSsa analysis.

<p align="center">
	<img alt="libssa_flowchart" src="https://github.com/kstenio/libssa/raw/master/libssa/pic/examples/libssa_fluxogram.png" width="900em"><br>
	<i>LIBSsa working flowchart</i>
</p>
