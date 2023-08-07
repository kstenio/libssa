---
title: 'LIBSsa: an open source software for analyzing LIBS spectra'
tags:
  - LIBS
  - Python
  - spectroscopy
  - modelling
  - automation
authors:
  - name: Kleydson Stenio
    orcid: 0000-0002-1407-9712
    corresponding: true
    affiliation: "1, 2"
  - name: Débora Marcondes Bastos Pereira Milori
    orcid: 0000-0003-1253-7174
    corresponding: false
    affiliation: 2
affiliations:
 - name: Department of Biotechnology, Federal University of São Carlos, São Carlos, SP 13563-905, Brazil
   index: 1
 - name: Embrapa Instrumentation, São Carlos, SP 13560-970, Brazil
   index: 2
date: TODO
bibliography: paper.bib
---

# Summary

Laser Induced Breakdown Spectroscopy (LIBS) is a technique that uses a high-energy pulsed laser to detect and analyze 
elements present in a sample. The laser beam is directed through an optical system (commonly mirrors, lenses, prisms,
or optical fibers) and focused onto the sample's surface. When the laser interacts with the sample, part of it is ablated,
vaporized, and generates a high-temperature plasma. The species present in the plasma emits electromagnetic radiation
that is characteristic of each element present in the sample. This radiation is then collected by lenses and conveyed
through an optical fiber to a spectrometer, where the separation and detection of wavelengths occur, typically using a
CCD (charge-coupled device) or ICCD (intensified charge-coupled device) device. Finally, a spectrum is generated [@miziolek2006laser].

The _Laser Induced Breakdown Spectroscopy spectra analyzer_ (**LIBSsa**) is an open souce software written in Python focused in
the analysis of LIBS spectra. It combines multiple tools used in LIBS analysis into one single application, such as outliers removal,
isolation of spectral lines, curve fitting, linear models (calibration curves), Principal Components Analysis (PCA) and 
calculation of plasma temperature and electron density.

![Logo of LIBSsa. Source: [LIBSsa repository](https://github.com/kstenio/libssa/).\label{fig:1}](./pic/libssa.svg)

# Statement of need

LIBS measurement is much simpler than other common elementary characterization techniques such as Flame Absorption
Atomic Spectrometry (FAAS) or ICP (Inductively Coupled Plasma), since it does not require acid digestion for sample preparation,
and the spectrum of a sample can be obtained in seconds, however the analysis of its signal may be highly complex.

Much of the complexity in analyzing LIBS spectra arises mainly due to matrix effects, which hinder the ability to obtain 
calibration blanks and, consequently, generate universal calibration curves. As a result, analysts need to adopt various
calibration and signal processing strategies to achieve quantitative measurements.

In general, those who work with LIBS commonly develop their own tools to process the measured signal and extract satisfactory
results. However, this practice has the effect of generating highly specialized users of the technique, not only in terms
of using instrumentation but also in scientific data analysis tools, such as [R](https://www.r-project.org/),
[MATLAB](https://www.mathworks.com/products/matlab.html), [OriginLab](https://www.originlab.com/), [Weka](https://www.cs.waikato.ac.nz/ml/weka/),
among others. Although these software are powerful tools for signal analysis, they are not dedicated tools for LIBS spectra analysis.

Knowing these challenges in making the LIBS technique more widely used, Stenio [@kstenio2023] proposed the creation of a software
that would automate the LIBS analysis, incorporating strategies used in several works in the literature [@marangoni2016phosphorus, @nicolodelli2014quantification, @de2021total, @stenio2022carbon, @castro2016twelve, @stenio2022direct].
In this way, the LIBSsa software was conceived.

![LIBSsa home screen tab with spectra loaded. Source: self-authored.\label{fig:2}](./pic/libssa.png)

The main purpose of LIBSsa is to help scientist in LIBS/spectroscopy field gain speed and practicality when analyzing LIBS
spectra, allowing fast assessment of which is the best calibration strategy for they sample set.

# Brief software description

Use of LIBSsa is straight forward: the user selects the input source (where LIBS spectra are located), load them into the
program and do a wide range of treatments. In each step, it is possible to save/export data into multiple file formats 
(txt, csv and xlsx). Figure 3 shows a usual workflow of LIBSsa analysis.  

![LIBSsa working fluxogram. Source: self-authored.\label{fig:3}](./pic/libssa_fluxogram.png)

In order to properly operates, the program uses the libraries **NumPy** [@harris2020array] and **SciPy** [@virtanen2020scipy] for 
most calculations, **pandas** [@mckinney2010data] and **openpyxl** to export spreadsheets [@openpyxl2023v312], **scikit-learn** [@pedregosa2011scikit]
to do linear, PLS and PCA models, **pyqtgraph** [@pyqtgraph2023v0133] to show in program graphics, and finally **PySide6** [@pyside62023v643] as
the graphical user interface (GUI) framework.

# Author contributions

Conceptualization: K. S., D. M. B. P. M.; data curation: K. S.; formal analysis: K. S.; funding acquisition: D. M. B. P. M.;
investigation: K. S.; methodology: K. S.; project administration: K. S.; resources: D. M. B. P. M.; software: K. S.; supervision: D. M. B. P. M.;
validation: K. S., D. M. B. P. M.; visualization: K. S.; writing – original draft: K. S.; writing – review & editing: K. S., D. M. B. P. M..

# Conflicts of interest

There are no conflicts to declare.

# Acknowledgements

The development of LIBSsa software (up to version 2.0.99) was supported by the Coordination for the Improvement
of Higher Education Personnel - Brazil (CAPES) - Finance Code 001, and by Embrapa Instrumentation.

# References
