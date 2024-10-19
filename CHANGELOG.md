# CHANGELOG


## v2.5.1b5 (2024-10-19)

### Chores

- **fix**: minor adjustment [skip-ci] ([`a52eccb`](https://github.com/kstenio/libssa/commit/a52eccb6632c0f876c2b052d573e3aff5bca3843))

### Continuous Integration

- **forcemerge**: fixing issues after a issues during previous merge ([`250c882`](https://github.com/kstenio/libssa/commit/250c88232f6c767f06523622e773041749d7fa73))
- **force-merge**: 'develop' into ci/autoversion (ours) [skip ci] ([`758c406`](https://github.com/kstenio/libssa/commit/758c406c89c61522d69d1aa697644f28cfe997a6))
- **merge**: <- develop ([`30b1e11`](https://github.com/kstenio/libssa/commit/30b1e11117aa1938f7d914470b4f1dd20e207cb4))
- **merge**: develop <- ci/autoversion [2] ([`9be401c`](https://github.com/kstenio/libssa/commit/9be401c2e29c203711160d880787b852a4cd6e23))
- **merge**: develop <- ci/autoversion [3] ([`0e8928b`](https://github.com/kstenio/libssa/commit/0e8928b6645d68dabaae5af47599bc00356efe5c))
- **merge**: develop <- ci/autoversion ([`a3d7df9`](https://github.com/kstenio/libssa/commit/a3d7df9355c46428471907733e4a63c743a5e336))

## v2.5.1b4 (2024-10-19)

### Builds

- **publish-with-uv**: added settings for publish to pypi + updated readme (main and gui) ([`822a939`](https://github.com/kstenio/libssa/commit/822a93923f74f41fe4884a8b6d8d5c16de0bf412))

## v2.5.1b3 (2024-10-19)

### Builds

- **publish-with-uv**: using uv to publish (testpypi) ([`e91f4ac`](https://github.com/kstenio/libssa/commit/e91f4ac8b78445e364fe0c8afebb20076611bc3d))

## v2.5.1b2 (2024-10-19)

### Documentation

- **readme**: updated README.md and Makefile commands ([`3393290`](https://github.com/kstenio/libssa/commit/33932903b7c0a5e9d7b00b4dacd2d6788c024629))

## v2.5.1b1 (2024-10-19)

### Chores

- **makefile**: adding Makefile aliases to project ([`412a8fd`](https://github.com/kstenio/libssa/commit/412a8fdabc57b1bcf7edf2aa095ad9cc1ba7cb95))

## v2.5.1b0 (2024-10-19)

### Continuous Integration

- **autoversion**: adding and setting up commitizen for auto-version bump mechanism ([`91a93e8`](https://github.com/kstenio/libssa/commit/91a93e803a7e91c3a1197f54071e0e286aa5b76f))

## v2.5.0 (2024-10-13)

### Breaking

* docs(basic-data)!: replacing current contact in favor of github one ([`54bdf91`](https://github.com/kstenio/libssa/commit/54bdf91ed91063ea67dbbc1f374f0c03b11d0637))

* ci(dev)!: moved files to start using src layout + publish in testpypi [attempt #4] ([`d94c5b0`](https://github.com/kstenio/libssa/commit/d94c5b0517d8f83ef7446ee8c98bc1bb54f9dd16))

* ci(dev)!: updating action for uv build and publish in testpypi [attempt #2] ([`6b647f1`](https://github.com/kstenio/libssa/commit/6b647f127c9264e418e5942f9f0a7cd646267faa))

* style(uv)!: used pre-commit with all-files flag ([`73843da`](https://github.com/kstenio/libssa/commit/73843da912c6f368814f1bec726b438585846f4b))

* test(uv)!: updating action for uv build and publish in testpy [attempt #1] ([`03d7514`](https://github.com/kstenio/libssa/commit/03d75141ad217b307943b56828e8881df97d4e47))

* feat(uv)!: replaced poetry with uv + using ruff as main formatter ([`e9734b1`](https://github.com/kstenio/libssa/commit/e9734b162c99fc2b20d03d7bd5701be7128f753f))

* feat!: replacing poetry -> uv (base adjustments) ([`b70a936`](https://github.com/kstenio/libssa/commit/b70a9361f0b2355c0689129402f928901bc9374b))

* feat!: added pre-commit with basic config ([`bf1f569`](https://github.com/kstenio/libssa/commit/bf1f5696df1b353d3a313d282a75a04e3923b4d6))

* feat!: replacing setuptools for poetry + Python 3.11 support ([`a838cec`](https://github.com/kstenio/libssa/commit/a838cec58195996520fc94268a9faef626a6a809))

### Chores

* chore(precommit): adjustments in pre-commit settings [3] ([`5de640f`](https://github.com/kstenio/libssa/commit/5de640f9d74080a253e502e81870213fed5cf220))

* chore(precommit): adjustments in pre-commit settings [2] ([`66de0ab`](https://github.com/kstenio/libssa/commit/66de0ab129f5aec618f6e91718762b8474d34271))

* chore(precommit): adjustments in pre-commit settings ([`3a7ae1e`](https://github.com/kstenio/libssa/commit/3a7ae1e0bbea47e400e24268e40b30b70032d692))

* chore(basic-data): moving sample data into a proper data folder + minor changes ([`d2a086e`](https://github.com/kstenio/libssa/commit/d2a086ecf3f12f0ecf0a6e387c74e76e625d4882))

### Code Style

* style(precommit): ran pre-commit in all files after hook changes (+ inclusion of pyupgrade hook) ([`7efc94c`](https://github.com/kstenio/libssa/commit/7efc94cec37976f7fd6af2ca6c3ecda7b210fb8b))

### Continuous Integration

* ci(testpypi): testing removal of API-TOKEN from action [4] (v2.5.0a4) ([`3cc5977`](https://github.com/kstenio/libssa/commit/3cc59779580fca0034a983d30b873ee2c02975df))

* ci(testpypi): testing removal of API-TOKEN from action [3] (v2.5.0a4) ([`54fba90`](https://github.com/kstenio/libssa/commit/54fba9039c22668e8eba58c5aa36a8e470a1120b))

* ci(testpypi): testing removal of API-TOKEN from action [2] (v2.5.0a4) ([`fb11137`](https://github.com/kstenio/libssa/commit/fb111370b289ee5ffb33da6b89a8695ba4efe2a2))

* ci(testpypi): testing removal of API-TOKEN from action (v2.5.0a3) ([`daf7fbc`](https://github.com/kstenio/libssa/commit/daf7fbc17f7266b01d0be746de5ac0415d654294))

* ci(dev): updated version (2.5.0a2) ([`ecda448`](https://github.com/kstenio/libssa/commit/ecda448cc11a0664f13364c02cb1e21ec7ac0e01))

* ci(dev): updating action for uv build and publish in testpypi [attempt #3] ([`065c37d`](https://github.com/kstenio/libssa/commit/065c37d90dc8483a96894169745f7e1f21a23da7))

### Features

* feat: created new workflow for poetry (publish-to-testpypi.yaml) [to be tested {2}] ([`7f838e0`](https://github.com/kstenio/libssa/commit/7f838e04826dc4f7ceca233adae9ed5768fdda0d))

* feat: created new workflow for poetry (publish-to-testpypi.yaml) [to be tested] ([`f7097ed`](https://github.com/kstenio/libssa/commit/f7097ed9d930a49ee8b4df7e7cbcc97fffd50442))

* feat: added extra pre-commit base hooks + using importlib.metadata to capture app/lib version ([`4a7509c`](https://github.com/kstenio/libssa/commit/4a7509c375ee8d25c35d035dfbe7532c2f226dc5))

### Fixes

* fix(uv): correctec version ([`1283239`](https://github.com/kstenio/libssa/commit/1283239cf6d5ecaf55d383379a527ab22c95e26a))

### Unknown

* Merge pull request #9 from kstenio/feat/moving-to-uv

Feat/moving to uv ([`57a6255`](https://github.com/kstenio/libssa/commit/57a6255f766bfe3f21dc4efd74bbc772d88af32a))

* Update CITATION.cff

Updated CITATION from Zenodo to JOSS data ([`d08c10a`](https://github.com/kstenio/libssa/commit/d08c10af2407a6c33ba8ef9f493fe4522fa6a508))

* Create CITATION.cff ([`3f1a42c`](https://github.com/kstenio/libssa/commit/3f1a42c48c75ae78f6af3f36c65233220c1d69ea))


## v2.2.0 (2023-12-31)

### Unknown

* LIBSsa version 2.2 (untrack)

publish-as-package.yaml
* Disabled publish (for Zenodo 1st run) ([`125ee58`](https://github.com/kstenio/libssa/commit/125ee58bffe735012ec4f21f619ac600f53f9413))

* LIBSsa version 2.2

libssa.png
* Replaced main app picture

libssagui.py
* Updated version to 2.2 ([`db765b1`](https://github.com/kstenio/libssa/commit/db765b1746075c7ac1c499e17132dbe57db317ba))

* Addressing issue #4 (tests) [test for saving areas]

test_export_areas.py
* Created a test script to check if program reads data, export values and confirms if obtained result is consistent
* A little odd to create. QThreadPool in operations resulted in unexpected behaviour, but the qtbot waitUntil implementation was the key

imports.py
* Updated delim standard ([`2007c81`](https://github.com/kstenio/libssa/commit/2007c8141ec5ba18b26eb5aba6e365a5becbbfb6))

* Addressing issue #4 (tests)

test_load_spectra.py
* Created a simple test script for loading spectra
* It is divided in 2 parts:
    1. Mocking spectra: creates folders and files in temp directory for test (auto deleted after test)
    2. Test load function: checks if values returned from load function (from libssa.env.imports) is as expected ([`6c58645`](https://github.com/kstenio/libssa/commit/6c586458cadceddae0f789ca69396bc78f4a2a2a))

* Addressing issue #7

libssa2.py
* Added false condition to path in spopen

README_GUI.md
* Changed pictures path to relative (tested on IDE) ([`0853cb9`](https://github.com/kstenio/libssa/commit/0853cb966ffadec32f05f98785c3d04ddb76f9e9))

* Addressing issue #3 (readme-3)

libssagui.ui and libssagui.py
* Added new element in menu for loading sample data

libssa2.py
* Now imports tarfile and tempfile libs
* New tempfolder class variable created to save extracted sample spectra
* New connection from menu to loadsample_spectra
* Method loadsample_spectra now extracts sampled synthetic_samples_ultra-low-res-spectrometer_c-model.tar.gz file to self.tempfolder, then triggers spopen and spload
* Method spopen now works in empty path mode (normal) and non empty (sample data)
* Spload does self.tempfolder cleanup ([`1b55489`](https://github.com/kstenio/libssa/commit/1b554893bf2a91ad0b0179fac91338896c0203ca))

* Addressing issue #3 (readme-2)

publish-as-package.yaml
* Re-enabled publish to PyPI

pyproject.toml
* Added dependencies for dev install: `pip install libssa[dev]`

README.md
* Added links for badges ([`d53f9d9`](https://github.com/kstenio/libssa/commit/d53f9d93fccb2a1887cb05013e4a710e9b11b31e))

* Merge remote-tracking branch 'origin/master' ([`3b2da9d`](https://github.com/kstenio/libssa/commit/3b2da9d11fdc3596450429b06adc271d6a20e9f4))

* Update README.md ([`fc487d9`](https://github.com/kstenio/libssa/commit/fc487d9e29dfb9ad2ea12ba5aae48ec1a7e90860))

* Addressing issues #3 (readme-1)

README.md
* Added extra badges
* Changed to shields.io do badgen.net
* Updated/included instructions for PIP to install LIBSsa in editable mode ([`28cb918`](https://github.com/kstenio/libssa/commit/28cb918a5e6b32d69c48f1dad3b12aa355a632e8))

* Addressing issues #3 and #4 (packaging-6)

libssa.svg
* Rollback...

README.md
* Updated/included instructions for PyPI install ([`2c29542`](https://github.com/kstenio/libssa/commit/2c295421e87de0d47176a517cd88d3d43edfe6de))

* Addressing issues #3 and #4 (packaging-5)

libssa.svg
* Another small adjustment with the white shadow

README.md
* Contributing and Features now references blob instead raw content (on GitHub) ([`b35a584`](https://github.com/kstenio/libssa/commit/b35a5847702e89805918be02990b09125788ad8e))

* Addressing issues #3 and #4 (packaging-5)

libssa.svg
* Added small white shadow

README.md
* Added raw path for pictures ([`7ec0ac3`](https://github.com/kstenio/libssa/commit/7ec0ac30110fa488f6c25980bc8cec097cefdfd8))

* Addressing issues #3 and #4 (packaging-4)

README.md and README_GUI.md
* Improved files based on text on _joss_ branch

CONTRIBUTING.md and FEATURES.md
* Added contributing guidelines and features in need
* Moved features text to another branch

libssa2.py
* Removed getting version from html file
* Added mode to insert pictures in about

./libssa/pic/examples
* Added pictures to improve README.md and FEATURES.md ([`86898dc`](https://github.com/kstenio/libssa/commit/86898dcfca317890692314893987d547ee1d9c65))

* Update publish-as-package.yaml

Testing publishing ([`2deeda1`](https://github.com/kstenio/libssa/commit/2deeda1e4c0efc85b0620f0b6a76f3471402ee67))

* Merge remote-tracking branch 'origin/master' ([`48a905b`](https://github.com/kstenio/libssa/commit/48a905bf11da2a2a0e9cfb34597a5139dbf8bde0))

* Update pyproject.toml ([`2b92c2e`](https://github.com/kstenio/libssa/commit/2b92c2e0718207638c769a50e57548917ede468b))

* Addressing issue #4 (packaging-3)

publish-as-package.yaml
* Added PyPI publish ([`7f68367`](https://github.com/kstenio/libssa/commit/7f68367361982bbfcf7d3f2c6ffba2228a7cfed6))

* Merge remote-tracking branch 'origin/master'

# Conflicts:
#	pyproject.toml ([`af7f2d3`](https://github.com/kstenio/libssa/commit/af7f2d3425ee5595701d8fe14ee634bca6812e7b))

* Addressing issue #4 (packaging-2)

pyproject.toml
* Added description
* Removed license field (as it is in classifiers)
* Added setuptools find entry ([`c4cb36d`](https://github.com/kstenio/libssa/commit/c4cb36d9b3bda688ca7fdfb55a2c2a9ca832445d))

* Addressing issue #4 (packaging-2)

pyproject.toml
* Added description
* Removed license field (as it is in classifiers)
* Added setuptools find entry ([`ab6e761`](https://github.com/kstenio/libssa/commit/ab6e761881573cdb34949b90ae5f55a8c6b74f1c))

* Addressing issue #4 (packaging)

publish-as-package.yaml
* Rollback to previous setting (by domna)

libssa2.py
* Indentation fix
* Replaced README.md to README_GUI.md (added new) into libssa folder (module)

MANIFEST.in
* Added markdown files as include

pyproject.toml
* Replaced ~= to <= for dependencies
* Added entry for packages['libssa'] in tool.setuptools
* Rollback to version_scheme = "no-guess-dev" and local_scheme = "node-and-date" ([`214a806`](https://github.com/kstenio/libssa/commit/214a8060c52a56499d54f0eec8f805fa4d9bc84c))

* Update pyproject.toml ([`3892d72`](https://github.com/kstenio/libssa/commit/3892d72352a0fa5ba44034474a509a93bf39d67c))

* Update pyproject.toml ([`faa7904`](https://github.com/kstenio/libssa/commit/faa79041682d28240390edaa451c2fb4fc37d549))

* Update pyproject.toml ([`cbbb7f9`](https://github.com/kstenio/libssa/commit/cbbb7f95e1e897b152865156d8a476ddfb83c68d))

* Update pyproject.toml

Attempt fixing build/deploy TestPyPI ([`afcfaf8`](https://github.com/kstenio/libssa/commit/afcfaf889cb2e374a91b0022977d0ee5225a4b7b))

* Update publish-as-package.yaml ([`3ae7e78`](https://github.com/kstenio/libssa/commit/3ae7e78106cd8860f6c1fd06543a896af1310e76))

* Update publish-as-package.yaml

Added/updated for TestPyPI ([`c10166b`](https://github.com/kstenio/libssa/commit/c10166b44ff83e2a0004f37729924e2e4eeddfbb))

* Merge pull request #5 from domna/packaging

Adds basic packaging ([`769d334`](https://github.com/kstenio/libssa/commit/769d334f1086e7901ae0757712dd25c1221aac68))

* Adds basic qt test ([`ff3e4f9`](https://github.com/kstenio/libssa/commit/ff3e4f926b3984061770ec78cdd4a27c6ef1cd68))

* Add github action for publishing ([`4a1a300`](https://github.com/kstenio/libssa/commit/4a1a300dcbf5d068dc8052c7140587184a9f677d))

* Adds basic packaging ([`8be1d16`](https://github.com/kstenio/libssa/commit/8be1d16cd3c57c1d7f0aaf5230cc85466032abfb))


## v2.1.0 (2023-08-05)

### Unknown

* LIBSsa version: 2.1 Release!

README.md
* Included copyright section

libssagui.py
* Included version and about_html as class variables
* App opens in maximized window now
* Simplified show_about
* Tiggeting menu button calls show_about inside GUI, not on main app

libssa.svg
* Corrected picture (name in US convenction)
* Removed open graph

libssa2.py
* Updated create about to just save data (version and html) into gui variables
* Removed connection ([`de7ae0b`](https://github.com/kstenio/libssa/commit/de7ae0b2b7bbbdf4e4f71fd885ea5046f2d8d498))

* LIBSsa version: 2.0.99 Pre-Release (Final)

README.md
* Added reference of thesis
* Included acknowledgements

libssagui.py
* Corrected open tags in checktable ([`1765de5`](https://github.com/kstenio/libssa/commit/1765de54a93364d17a22a8458354bfdac2f030c1))

* LIBSsa version: 2.0.98 Pre-Release

FINAL roadmap:
* Pre-Release: Minor corrections and tests [2.0.7 -> 2.0.99]
* Launch: 2.1
* This is a post thesis defense commit
* All references for year 2022 were changed to 2023

requirements.txt
* Tested the program with Python 3.9 (previous was 3.8) and updated libraries to new versions
* This had some impact in the program regarding ExcelWriter and color scheme (with new version of PySide6, now the application changes layout between light and dark modes)

README.md
* Updated text/instructions and did some grammar correction

libssa2.py
* Added extra message for import error (mainly for PySide 6.5 bug with xcb, but requirements prefer 6.4)

export.py
* In the new version of pandas/openpyxl, the object ExcelWriter does not have the method save(). Instead, they opted to hide this method, as _save()
* As result, all references of writer.save() were removed
* This will impact positively on resources, but may have problems with big environments (users will confirm eventually)

libssagui.py
* PyQtGraph new implementation of TextItem now uses html info for rendering box, including font colors
* This resulted in a bad rendering of colors
* To avoid this, a <span> tag was added in text string, containing style class with color setting ([`e564104`](https://github.com/kstenio/libssa/commit/e564104f76810b35ff13c26dcaea71ce7a97bbf0))

* LIBSsa version: 2.0.97 Pre-Release

FINAL roadmap:
* Pre-Release: Minor corrections and tests [2.0.7 -> 2.0.99]
* Launch: 2.1

libssagui.py
* Disabled autoSIPrefix for pyqtgraph
* Corrections in linplot and plsplot
    * Changed symbol from None to ''
    * Properly positioning of information box (better anchoring)
    * Added transparency to box background ([`ca7b6be`](https://github.com/kstenio/libssa/commit/ca7b6be5841f85eee090eb7d6504fe1e32fe254c))

* LIBSsa version: 2.0.96 Pre-Release

FINAL roadmap:
* Pre-Release: Minor corrections and tests [2.0.7 -> 2.0.99]
* Launch: 2.1

ALL FILES: Updated initial copyright/license message

tree.html
* Updated file list

libssagui.py
* Updated imports
* Added DOCSTRING to every method/function
* Added spinbox setting the default shape for fit after isolation
    * The valuechanged signal also updates all shapes in real time
* Minor improvements in some methods

export.py
* Discovered bug when saving PCA data based on Areas or Heights. Corrected now.
* Inserted Full-Mean as column 0 in the export_correl function

spectra.py
* Improved DOCSTRINGS

libssa2.py
* Discovered major bug in isolation: wasn't using outliers removed intensities for isolation
    * Added extra checks for this behaviour
    * Two solutions: for intime use, and when loading lb2e file
* Minor corrections and inprovements

README.md
* Changed location of Warranty section ([`41a8ee8`](https://github.com/kstenio/libssa/commit/41a8ee8ca97c841c7b80b7ad2aed4a10784c0cf4))

* LIBSsa version: 2.0.95 Pre-Release

FINAL roadmap:
* Pre-Release: Minor corrections and tests [2.0.7 -> 2.0.99]
* Launch: 2.1

ion.py
* Added backup code of how data was scrapped for ionization energy

libssagui.py
* Discovered a bug where combobox (pages 4 and 5) were not reset when reloading reference spreadsheet ([`733aefc`](https://github.com/kstenio/libssa/commit/733aefcbacf062a3f483499a55f8ffb06397550e))

* Merge remote-tracking branch 'origin/master' ([`ff7759f`](https://github.com/kstenio/libssa/commit/ff7759fec2a8428f29749ff0ed44a31d3d4fa257))

*  LIBSsa version: 2.0.93 Pre-Release

FINAL roadmap:
* Pre-Release: Minor corrections and tests [2.0.7 -> 2.0.99]
* Launch: 2.1

export.py
* Corrected condiction to export PCA data
* Replaced index in the second worksheet to sample names
* Increased value for resize columns ([`8f4acb0`](https://github.com/kstenio/libssa/commit/8f4acb0ce13bef43fad8c936a2b725921e665b3d))

* LIBSsa version: 2.0.94 Pre-Release

FINAL roadmap:
* Pre-Release: Minor corrections and tests [2.0.7 -> 2.0.99]
* Launch: 2.1

libssagui.py
* Corrected error where isolation algorythm wasn't using data without outliers (when performed by user) ([`32b9296`](https://github.com/kstenio/libssa/commit/32b9296fed9e5ba05a829aab43575f04c86748eb))

*  LIBSsa version: 2.0.93 Pre-Release

FINAL roadmap:
* Pre-Release: Minor corrections and tests [2.0.7 -> 2.0.99]
* Launch: 2.1

libssagui.py
* Corrected tables in update_tables_from_spreadsheet

export.py
* Corrected tables in export_iso_table

README.md
* Minor updates to text ([`78f91b6`](https://github.com/kstenio/libssa/commit/78f91b60f07d3d6e41acc31380b8ea140f4f5261))

* Minor update in export.py: added with_suffix to csv/txt exportation ([`f2d3b23`](https://github.com/kstenio/libssa/commit/f2d3b233e7b4a1b76db6bea4579ed965adf053c2))

* Minor changes in the README.md file ([`e158f30`](https://github.com/kstenio/libssa/commit/e158f30780fd224b42fb9016c300db514c74dfef))

* LIBSsa version: 2.0.92 Pre-Release

FINAL roadmap:
* Pre-Release: Minor corrections and tests [2.0.7 -> 2.0.99]
* Launch: 2.1

tree.html
* Added tree.html file - generated by linux tree application - containing all files in the project structure

libssagui.py
* Minor corrections in text

libssa2.py
* Minor corrections in text ([`d1733b0`](https://github.com/kstenio/libssa/commit/d1733b061f77690d99c1f48684e6fbd83738c55a))

* LIBSsa version: 2.0.91 Pre-Release 

LIBSsa version: 2.0.91 Pre-Release 

FINAL roadmap:
* Pre-Release: Minor corrections and tests [2.0.7 -> 2.0.99]
* Launch: 2.1

.idea
* Deleting the folder, as it was from my personal IDE settings ([`235f56f`](https://github.com/kstenio/libssa/commit/235f56fed4f80d3da73a0fb51112cfd9e5ccc45f))

* LIBSsa version: 2.0.9 Pre-Release

FINAL roadmap:
* Pre-Release: Minor corrections and tests [2.0.7 -> 2.0.99]
* Launch: 2.1

libssa-repository-open-graph.png
* Added open graph picture (uploaded to GitHub as well)

readme.html
* File created based on README.md

libssagui.py
* Added translators for menu entry for Help/About
* Added new class LIBSsaAbout, for showing the about
* This class is called in a show_about method

libssa2.py
* Added create about, connected with the about menu entry
    * This is basically a wrapper for show_about method inside GUI
    * It reads the README.md file and transforms it into HTML using the markdown library
* Improved changestatus in environment method ([`e91f4c3`](https://github.com/kstenio/libssa/commit/e91f4c332e00af179f5980e317bedcbe8de73cc1))

* LIBSsa version: 2.0.8 Pre-Release

FINAL roadmap:
* Pre-Release: Minor corrections and tests [2.0.7 -> 2.0.99]
* Launch: 2.1

Global modifications
* Added updated headers and Copyright notice in each _py_ file
* Added/revised docstrings for each module inside _env_ folder
* Restructured file locations to a better/simpler way

requirements.txt
* Updated versions of libraries
* Added markdown lib

README.md
* Wrote the 1st version of readme file
* Contains software description, how to install and features
TODO1: add a method to show readme inside gui/help
TODO2: saves a new html based on readme file ([`6216a18`](https://github.com/kstenio/libssa/commit/6216a18cc87ae52404b69c5e9268f2ec5f0d1dc7))

* LIBSsa version: 2.0.7 Pre-Release

MILESTONE: Plasma parameters (calculation and data exportation) are finally done!
Now, moving in better organizing data, minor performance improvements, write README.md,
adds proper LICENCE, etc.

FINAL roadmap:
* Pre-Release: Minor corrections and tests [2.0.7 -> 2.0.99]
* Launch: 2.1

functions.py
* Extra imports
* Actually created tne_do algorythm
    * Gets all data from the GUI and calculates plasma temperature and electron density
    * Returns curves (for plots) and DF report (exportation)

spectra.py
* Better organization of self.plasma parameters
    * 'Ln': y-values (ln combination of parameters)
    * 'En': x-values (difference between energies)
    * 'Fit': adjusted line (slope and intercept are used to obtain data)
    * 'Parameter': stores parameter used, being 'Area' or 'Height'

export.py
* Actually created export_tne method
    * It receives data from GUI (spectra.plasma) and creates 2 DFs
    * One mainly swaps the 'Report' from plasma
    * Another gets all curves from each Saha-Boltzmann plot
    * TODO: improve performance

libssagui.py
* Updated axis labels for Saha-Boltzmann energy plot in setgoptions (ci == 8)
* Created saha_b_plot method, for showing the Saha-Boltzmann plot

libssa.py
* Added file name in the message after loading environment
* Implemented call of export_mechanism for Saha-Boltzmann
* Updated title and plot call in doplot for S-B
* Method calc_t_ne is now getting properly the result from tne_to (from functions)  , and saving values in self.spec.plasma
* Minor changes and corrections in the code

* Created saha_b_plot method, for showing the Saha-Boltzmann plot
* Added translators and connects for new items (menu and combobox in page 6: T/Ne)
* Extra error handling sintax in loadui
* Method update_tne_values only creates dfs if none was created before; also, it sets row count to 0 before populating the T/Ne table
* New method update_table_from_spreadheet
    * Receives the mode (Iso or TNe) and spreadsheet location
    * If al is fine with column names, constructs the table

libssa.py
* Improve error message when loading ui file
* New menu entries (imports) are connected to new method spreadsheet_to_table
    * This method is just a bypass to get filedialog
    * Also, shows warning regarding importing T/Ne table
* Method environment nows updates values for T/Ne Dfs and tables, if saved in self.spec.plasma
* Created method calc_t_ne, which checks is all is fine with the T/Ne table and then call main function (method connect with start button in p6) ([`a8a202a`](https://github.com/kstenio/libssa/commit/a8a202a4ae0d9a438e9421a4263f1f7f4be31e5f))

* LIBSsa version: 2.0.6 RC 2

Expected roadmap:
* RC: Plasma Parameters [2.0.6] (calc and export)
* Release: Minor corrections and tests [2.0.7 -> 2.1.0]

functions.py
* Created prototype function for T/Ne calculations

spectra.py
* Added new entry in self.plasma to store the current element in use

libssagui.ui
* Added menu entries for importing iso and tne tables
* Added new combo box in page 6 order to get what parameter will me used for T/Ne calculations

libssagui.py
* Main class now inherits from QMainWindow
* Added translators and connects for new items (menu and combobox in page 6: T/Ne)
* Extra error handling sintax in loadui
* Method update_tne_values only creates dfs if none was created before; also, it sets row count to 0 before populating the T/Ne table
* New method update_table_from_spreadheet
    * Receives the mode (Iso or TNe) and spreadsheet location
    * If al is fine with column names, constructs the table

libssa.py
* Improve error message when loading ui file
* New menu entries (imports) are connected to new method spreadsheet_to_table
    * This method is just a bypass to get filedialog
    * Also, shows warning regarding importing T/Ne table
* Method environment nows updates values for T/Ne Dfs and tables, if saved in self.spec.plasma
* Created method calc_t_ne, which checks is all is fine with the T/Ne table and then call main function (method connect with start button in p6) ([`77994ad`](https://github.com/kstenio/libssa/commit/77994ad231185a74822efb0507029bca7141178f))

* LIBSsa version: 2.0.6 RC 1

Expected roadmap:
* RC: Plasma Parameters [2.0.6] (calc and export)
* Release: Minor corrections and tests [2.0.7 -> 2.1.0]

ion.py
* Added new file (json-like) containing all values for 1st order Ionization Energies (from NIST)

spectra.py
* Added new entry in self.plasma to store DFs for tne table

libssagui.ui/py
* Added keyboard shortcuts for menu
* Added new elements for Plasma Parameters (Temperature and Electron Density)
    * 2 labels, one combo box, one table widget and finally a push button
* Created translators and connects for the new items
* Created methods to deal with those new elements
    * update_tne_values: gets values from ion.py and adds in the combo box + label. Also, is connected with the signal of the combo box, changing data with index
    * check_tne_table: checks if cell value is in order with column parameters. If not, restores previous value
* Above methods are linked with spectra.plasma['Tables'], being one DF for each element in ion.py. Those DFs are used to store and (eventually) save tne table environment

libssa.py
* Added with_suffix to path in export_mechanism, in this way, even if user deletes extension, the corect one will still be used
* Also, added some change statusbar to warn user
* In peakfit, now there's a call to update_tne_values ([`55071af`](https://github.com/kstenio/libssa/commit/55071af82a95294ff13b60caa00b9a49e182a391))

* LIBSsa version: 2.0.5 beta 1

MILESTONE: Finished saving and loading environment. This includes all spectra data, including reference and iso table.

Expected roadmap:
* RC: Plasma Parameters [2.0.6] (calc and export)
* Release: Minor corrections and tests [2.0.7 -> 2.1.0]

spectra.py
* Added new entry in self.isolated do store iso table

libssagui.py
* Added menu entries for load/save environment

libssa.py
* New imports: lzma (compression) and psutil (check RAM usage)
* New class variables to deal with ram usage
* Created method self.environment, to address saving and loading spectra environment
    * It is connected with the File/Menu entries
    * Has two modes, 'load' and 'save'
        * 'Save' mode warns user of how much RAM are available and about the process maybe taking a long time
        * 'Load' mode is faster, uncompress data and properly enables gui elements (such as buttons and iso table)
* Method peakiso/result() now constructs a DataFrame with data in the iso table (this DF is used in load environment) ([`2ad2bb1`](https://github.com/kstenio/libssa/commit/2ad2bb12dfd2f3678dc3fb16182f761171190c85))

* LIBSsa version: 2.0.4 beta 1

MILESTONE: Finished data exportation, now moving forward into save environment.

Expected roadmap:
* Beta: Load and save environment [2.0.5]
* RC: Plasma Parameters [2.0.6] (calc and export)
* Release: Minor corrections and tests [2.0.7 -> 2.1.0]

export.py
* New imports
* Huge performance leap in export_fit_peaks, as now dataframes are created with a matrix, instead by appending columns
* Moved export_correl from main program to here, properly using the export_mechanism and resizing writer columns
* Created template for export_tne (plasma temperature and electron density)

libssagui.py
* Added new zero-plot for pca/loadings

libssa.py
* Updated export_mechanism to better adress correlation spectrum
* Removed pickle dumps ([`c2178ca`](https://github.com/kstenio/libssa/commit/c2178ca342112247bfb0684d9e5838ab9781c3dc))

* LIBSsa version: 2.0.3 beta 4

New roadmap:
* Beta: Export data (XLSX and ASCII) [2.0.4] -> Load and save environment [2.0.5]
* RC: Plasma Parameters [2.0.6] (calc and export)
* Release: Minor corrections and tests [2.0.7 -> 2.1.0]

export.py
* New imports
* Created new functions to export data:
    * export_raw: not new, but now can manage outliers removed spectra
    * export_iso_table: saves just the data in the isolation table
    * export_iso_peaks: export each shoot for each peak saved (high demand on RAM)
    * export_fit_peaks: salves all original and fitted data for peaks
    * export_fit_areas: saves report of peak fitting (need better performance)
    * export_linear: saves data regarding linear models
    * export_pca: saves all pca data, including loadings and scores
    * resize_writer_columns: helper function to style Excel Writer

spectra.py
* Added "Element" in self.linear

libssagui.py
* Added new menu entry for export_peak_fitted (and translators)
* Updated translators for menu entries that needed

libssa.py
* Updated connects and dicts in export_mechanism (corrected name as well)
    * Also added new mode options to work with the new export.py functions
* Added some dumps to check structures (will delete later) ([`835b32d`](https://github.com/kstenio/libssa/commit/835b32dbb156fe30f268b9d71d406417d41550d3))

*  LIBSsa version: 2.0.3 beta 3

Expected roadmap:
* Beta: Plasma Parameters [2.0.4] ---> RC
* RC: Export data (XLSX and ASCII) [2.0.5] -> Load and save environment [2.0.6] ---> Release
* Release: Minor corrections and tests [2.0.7 -> 2.1.0]

WARNING: Minor change in roadmap, since in this commit I've started the development of data exportation

export.py
* Created the first 2 functions for exportation
    * export_raw: after loading sample, can export data in single format
    * export_pls: export models, metrics and predictions for PLS Regression predictions

functions.py
* Commented subtract by minimum in isolation

spectra.py
* Added "Att", "Samples" and "BlindPredict" as keys for self.pls
* Method clear now saves a backup of self.pls if a model is created (basically, for validation/blind predictions)

libssagui.py
* Added new translators for each export menu item/QAction
* Corrected lists in setgoptions (graphics labels and units)
* Removed redundant g.clear() methods (since it is called before in the main application)
* plsplot now is actualling plotting a blindprediction, using Bars instead of common line/scatter plot

libssa.py
* Created connects for each export menu entry
* Created function export_mecanism, which will adress each type of exportation
    * For now, implemented main method base elements (gui calls, errors handling)
    * Implemented export for RAW and PLS data
* Corrected doplot
    * Was not properly calling setgoptions in PLS option/elif
    * Corrected titles in PLS option
* Method pca_do now saves in self.spec.pls['Att'] instead of old 'Parameters'
* Method pls_do now saves correct data, including samples names, and updates GUI elements for prediction
* Created new method pls_predict, which uses calibration model for blindpredictions (this method is connected with the start prediction button) ([`15d92ec`](https://github.com/kstenio/libssa/commit/15d92ec84bc549a13234a86d64b22d627ddddd4f))

* LIBSsa version: 2.0.3 beta 2

Expected roadmap:
* Beta: Plasma Parameters [2.0.4] ---> RC
* RC: Export data (XLSX and ASCII) [2.0.5] -> Load and save environment [2.0.6] ---> Release
* Release: Minor corrections and tests [2.0.7 -> 2.1.0]

functions.py
* cv_r2 now returns the max value

libssagui.py
* Added proper box for plot results in plsplot
* Corrected ReziseMode for QTableWidgets (from SetResizeMode -> SectionResizeMode) ([`c418c19`](https://github.com/kstenio/libssa/commit/c418c19eef9bfaff5856a0411e12c4be090c56c6))

* LIBSsa version: 2.0.3 beta 1

Milestone achieved! PLS implemented! (minimal, but working)

Expected roadmap:
* Beta: Plasma Parameters [2.0.4] ---> RC
* RC: Export data (XLSX and ASCII) [2.0.5] -> Load and save environment [2.0.6] ---> Release
* Release: Minor corrections and tests [2.0.7 -> 2.1.0]

functions.py
* Reorganized pls_do and bug fixes

libssagui.py
* Discovered bug in splot that wasn't accepting column vectors for plot. Added reshape(-1) to x and y
* Corrected ReziseMode for QTableWidgets (from SetResizeMode -> SectionResizeMode)

libssa.py
* Replaced wrong comparison for self.spec.base (== -> is)
* Added connect for pls_do (from gui button) ([`4f3ea62`](https://github.com/kstenio/libssa/commit/4f3ea6202efca5ba3489eef1f9e29445fb1e2693))

* LIBSsa version: 2.0.2 beta 6

Expected roadmap:
* Beta: PLS [2.0.3] -> Plasma Parameters [2.0.4] ---> RC
* RC: Export data (XLSX and ASCII) [2.0.5] -> Load and save environment [2.0.6] ---> Release
* Release: Minor corrections and tests [2.0.7 -> 2.1.0]

functions.py
* New import for numpy and sklearn.model_selection
* Proper function to do pls (needs testing)

spectra.py
* Added new parameters for self.pls, following the ones in pls_do function (inside functions.py)

libssagui.py
* Created plsplot method, which gets the self.spec.pls dict and does plotting (cv mode)
TODO: implement blind mode and test/improve plot

libssa.py
* Now, pls_do actually calls a pls model
* Returned values populates self.spec.pls
* Graph elements and self.setgrange are called
* Doplot now calls gui.plsplot with proper parameters ([`21f6e9c`](https://github.com/kstenio/libssa/commit/21f6e9caa0a69551e128ce66a70f7ea6184d6e8b))

* LIBSsa version: 2.0.2 beta 5

Expected roadmap:
* Beta: PLS [2.0.3] -> Plasma Parameters [2.0.4] ---> RC
* RC: Export data (XLSX and ASCII) [2.0.5] -> Load and save environment [2.0.6] ---> Release
* Release: Minor corrections and tests [2.0.7 -> 2.1.0]

functions.py
* New import for PLSRegression
* New prototype function to perform PLS

spectra.py
* Moved base to class variable (cls instead self)
* Updated self.pls variables in a better format (similar to linear)

libssa.py
* loadref moved to menu methods (removed from page 2)
* Updated elements to save in pca_do
* Created prototype for pls_do ([`3f494c6`](https://github.com/kstenio/libssa/commit/3f494c6cc06ef71a01ab47d59ac59b66e6f86844))

* LIBSsa version: 2.0.2 beta 4

Expected roadmap:
* Beta: PLS [2.0.3] -> Plasma Parameters [2.0.4] ---> RC
* RC: Export data (XLSX and ASCII) [2.0.5] -> Load and save environment [2.0.6] ---> Release
* Release: Minor corrections and tests [2.0.7 -> 2.1.0]

libssa.ui
* Properly renamed gui elements in page 5 (PLS part) to start programming those elements

libssagui.py
* Created translators for p5/PLS
* Corrected some names for p4 combo boxes

libssa.py
* loadref now also adds columns into p5/PLS calibration combo box
* When PCA is complete, now changes widgets for PLS part (labels and start button) ([`be1b9ff`](https://github.com/kstenio/libssa/commit/be1b9ffa20903be665fc3ce261bccbeff4939bf2))

* LIBSsa version: 2.0.2 beta 3

Expected roadmap:
* Beta: PLS [2.0.3] -> Plasma Parameters [2.0.4] ---> RC
* RC: Export data (XLSX and ASCII) [2.0.5] -> Load and save environment [2.0.6] ---> Release
* Release: Minor corrections and tests [2.0.7 -> 2.1.0]

imports.py
* Finished implementing FSN to Single and Multi mode
* Added try/except for outliers

libssa.py
* Fixed error in spload (wrong call to worker signals error function wrapper)
* Fixed eror in FSN (wasn't running except for IS)
* Added error callback for outliers
** Minor data checks before FSN

libssagui.py
* Added variables, translators, connects and configs for FSN

libssa.ui
* Updated version: 2.0.2b3 ([`9cc4a80`](https://github.com/kstenio/libssa/commit/9cc4a8047cd88d6dd5807c0ae5e32bd77f3b8d3a))

* LIBSsa version: 2.0.2 beta 2

Expected roadmap:
* Beta: PLS [2.0.3] -> Plasma Parameters [2.0.4] ---> RC
* RC: Export data (XLSX and ASCII) [2.0.5] -> Load and save environment [2.0.6] ---> Release
* Release: Minor corrections and tests [2.0.7 -> 2.1.0]

Medium update: started to work on FSN (Full Spectrum Normalization) during spectra importation (Page 1)

imports.py
* Added parameter for FSN
* Prototype in single mode for FSN (all modes: Area, Norm, Max and IS)
TODO: finish implementing and adding it to Multi mode

libssa.py
* Implemented calls for FSN parameters and added it to load function
** Minor data checks before FSN

libssagui.py
* Added variables, translators, connects and configs for FSN

libssa.ui
* Created objects for FSN (Full Spectrum Normalization) during Page 1 (imports)
* Updated version: 2.0.2b2

requirements.txt
* Updated values (maybe I'll change again later in final revisions) ([`0d3fa00`](https://github.com/kstenio/libssa/commit/0d3fa00da6a5a8375ba5e7a31e59bb764b28fd9a))

* LIBSsa version: 2.0.2 beta 1

MAJOR Update: Changed main GUI library from PySide2 --> PySide6
Because of this, I decided to change the roadmap. Now, the expected roadmap is:
* Beta: PLS -> Plasma Parameters ---> RC (release candidate) [2.0.3]
* RC: Export data (XLSX and ASCII) -> Load and save environment ---> Release [2.0.4]

LICENSE
* Moved from doc to root

libssa.py
* PySide2 -> PySide6 replacement
* Replaced import error message
** Added instructions for libopengl0 (dependency of PySide6)

libssagui.py, functions.py, imports.py, spectra.py
* PySide2 -> PySide6 replacement

libssa.ui
* Updated version: 2.0.2b1 ([`3b6c409`](https://github.com/kstenio/libssa/commit/3b6c409e9cd49306c88cbb6c9182107aec3f4a43))

* LIBSsa version: 2.0.1 beta 4

libssagui.py
* New menu entry for export correl
* Added option for getSaveFileName in guifd

libssa.py
* Extra imports
* Implemented new section for Menu methods
** Created export correl method, connected with the new menu entry
*** It exports data from correl spectrum and saves a DataFrame/Spreadsheet
*** Each row is a wavelength and each column a Pearson for specific parameter (reference)

libssa.ui
* Updated version: 2.0.1b4
* Added new menu entry for export: Correlation Spectra ([`c07ea42`](https://github.com/kstenio/libssa/commit/c07ea42fe8a292e1e9c9bbfdbd90165d6dda2c7f))

* LIBSsa version: 2.0.1 beta 3

functions.py
* Extra import from numpy and sklearn (PCA)
* Isopeaks now normalizes the noise value for norm mode
* New function pca_scan
** Gets attributes and scans minimum components for PCA containing +95% of variance
** If requested, also normalizes the attribures
* New funciton pca_do
** Gets the final attributes (may have been normalized by pca_scan)
** With the number of components (user defined), returns the transformed data and the loadings

imports.py
* Added openpyxl as import and default engine for read_excel

spectra.py
* Removed PCA key from self.models and created an entire new global variable, self.pca
** It contains: 'Mode', 'OptComp', 'ExpVar', 'Attributes', 'Transformed' and 'Loadings' keys

libssagui.py
* New imports
* Added translators and elements for PCA in Page 5
* Created new legend object for graphic
* Updated axis in setgoptions (pca=5)
* Removed legend creation in fitplot
* Updated pretty colors to return tuple if number of colors == 1
* Created pcaplot function
** Based on index and operation mode, do the appropriate plot for PCA
** Will handle idx==0 (cummulative variance) and idx==5 (loadings) plots

libssa.py
* Extra imports
* New connects for Page 5: "PCA Scan" and "PCA Do"
* Doplot received some updates
** Legend now is cleared in the beginning of doplot
** Fit plot does not adds legend anymore
** Created actions for plotting PCA data
*** For PCA plots, a border is draw around legend
*** If idx in (0, 4), plot is passed to gui.pcaplot
*** For other options, plots are made inside module
**** PCA data are expvar, transformed and loadings
* Adde methods for Page 5 (PCA/PLS)
* For now, just PCA is implemented
* Two functions were created:
** pca_perform_scan: that handles input from program and user, and creates appropriated attributes matrix (rows = samples)
** pca_do: gets result from scan, plus user entry for number of components, and actually does the PCA
** After steps are done, setgrange is called (and also doplot)
* Minor update in the init [row 651] (using program root as Path.cwd())

requirements.txt
* Added compatible versions for libraries
* Removed: xlsx
* Added: matplotlib, sklearn

libssa.ui
* Updated version: 2.0.1b3
* Swapped Single and Multiple modes in import spectra (Page 1), and toggled Single as default
* Added main elements for PCA (Page 5) ([`34ece03`](https://github.com/kstenio/libssa/commit/34ece0335bba9db258f8507263bff2232a4ab01e))

* LIBSsa version: 2.0.1 beta 2

functions.py
* Modified title of plot (linear_model) to use subscript, X<sub>n</sub>, instead X-Pn (X = element, n = peak number)
* Changed how sigma is created for normalized models (now uses average) [may need some extra thinking...]
* Added new mode, 'Equivalent peak'
** This mode uses parameter = p1*p2/(p1+p2), and same for sigma/noise

libssa.py
* Added mode option for 'Equivalent peak'

libssagui.py
* Added translator for new radiobutton (every equivalent peak)

libssa.ui
* Updated version: 2.0.1b2
* Added radio button for equivalent peak model
** Button was added to button group p4bg2 ([`e9ab747`](https://github.com/kstenio/libssa/commit/e9ab747f346364873a0d93a7588bb5992f4d7adb))

* LIBSsa version: 2.0.1 beta 1

MAJOR Update: Program now enters Beta stage! 2.0 alpha 29 -> 2.0.1 beta 1
I've decided to change the release channel because now one can use the program ang get true results from it. The expected line of development is:
* Beta: PCA -> PLS -> Plasma Parameters ---> RC (release candidate) [2.0.2]
* RC: Export data (XLSX and ASCII) -> Load and save environment ---> Release [2.0.3]

spectra.py
* Now self.isolated has a 'Noise' parameter. This will store the noise of peaks (for limits of detection and quantification)

functions.py
* Isopeaks now performs the calculation of the noise for each isolated peak
** It uses the 20% of the peak in the beginning and in the end to calculate the standard deviation of the noise (minimum value are 2 points)
** The result is stored into a 3D array (len(elements), len(samples), 2)
* Added docstring for linear_model
* Linear_model receives noise and calculates sigma parameter
** Sigma is used to calculate LoD (Limit of Detection) and LoQ (Limit of Quantification)
** Main sigma is calculated using as base the sample with lower value of the reference
** If the linear model is based on normalization ('peak norm' or 'all norm' modes), a normalized sigma is also calculated
*** The LoD and LoQ for normalized models uses normalized sigma for correction
** Function returns the arrays of LoD and LoQ

libssa.py
* Peakiso gets noise return from result from isopeaks and saves in self.spec.isolated['Noise']
* Docalibrationcurve now sends noise to linear_model and gets value from the returned into self.spec.linear['LoD', 'LoQ']

libssagui.py
* Added 2 lines in the plot box with the values of LoD and LoQ

libssa.ui
* Updated version: 2.0.1b1 ([`134f6a1`](https://github.com/kstenio/libssa/commit/134f6a1138fae72aa8a8b123d855703175cbd225))

* LIBSsa version: 2.0 alpha 29

spectra.py
* Depreciated self.models['Linear'] to a more complex structure to store values from linear models. In this case, self.linear

imports.py
* Refcorrel nox gets the first column as index

functions.py
* New imports (sklearn)
* Created linear_model function
** It receives the reference, parameters to be used in the model (areas or heights), and also the parameters for nomalization
** The function has 3 modes: no normalization, normalization by specific peak, or normalization by all peaks isolated by the program
** Model is made using LinearModel from sklearn library
** Function returns reference, predicted values, R2*, RMSE*, slope* and intercept* (* arrays if all mode is chosen)

libssagui.py
* Updated logic for mode changer signals (enable or disable an element based on checkbox or radiobutton)
* Added new type inside guimsg: reference. This type returns a template DataFrame, to assist users when loading reference spreadsheet
* Added new connection when p4_pnorm_combo changes its index (or user does so)
** The method setnpealsnorm updates the range for the new spinbox added to the gui (to select the peak of an element as base for normalization)
* Finally, created linplot, a method to plot results from linear model
** It plots two curves: ref/pred and ref/ref
** Also shows a box containg the parameters of the linear plot: slope, intercept, R2 and RMSE
* (for some odd reason, had to add two g.autoRange)

libssa.py
* Extra imports (linear_model from functions.py)
* Loadref now shows a special message for users when trying to import reference into program
** Now a message containing instructions and a proper template spreadsheet are shown inside a messagebox
** This will minimize errors in reference importations (although it is kinda annoying)
* Changed position os setgrange (now is before doplot)
* Updated how plots are called in the application
** Depreciated self.ranged variable
** Now, when a operation is finished, the program changes g_selector current index and then calls setgrange
** Setgrange updates the ranges and calls doplot (this is much cleaner then the old way)
** Also, the plot is updated when user selects new element of combobox from the GUI (better behaviour as well)
* Created fully functional docalibrationcurve method
** It calls linear_model with proper parameters, and the returned values are updated into self.spec.linear
* Doplot updated to address linear models fits

libssa.ui
* Updated version: 2.0a29
* Added QSpinBox for selecting the peak for normalization (Page 4)
* Replaced 'Intensities' for 'Heights' (Page 4) ([`4556c79`](https://github.com/kstenio/libssa/commit/4556c79b4b3cf40bf8a6ae7e55ab3b571073401b))

* LIBSsa version: 2.0 alpha 28

spectra.py
* self.ref properly created with an empty DataFrame

functions.py
* Had to do A LOT of work to figure out a bug when tried to access the values for more than a single isolated peak
** Inside isopeaks, discovered that returnet center has to be initializated as array(dtype=object)
** Inside fitpeaks, much more had to be done/tested. In short lines:
*** Needs to use len(c/center) instead c/center.size
*** Can not use arrays for data, total, areas, widths and heights. Structures must be created as list. By preference, I opted to return tuples instead lists

libssagui.py
* Created peaknormitems as global variable. This will be useful when dealing with model with normalized peaks
* Added translators for the new p4_npeak SpinBox
* Setpeaknorm will also set range for p4_npeaks, based on value in p3_isotb (column 5)

libssa.py
* Extra imports (np.where)
* Swapped position of linear in doplot (not functional yet)
* Spectra object now is cleared everytime new samples are imported
* Updated and implemented minimal functional version os docalibrationcurve
** Only for "no norm mode"
** Gets values from areas/intensities (after fit) and reference (from file)
** User can select inside GUI: the element and the peak for the linear model, reference, and parameter (areas/intensities)
* TODO: Implement the linear model itself, adding values inside self.spec.models['Linear']

libssa.ui
* Updated version: 2.0a28
* Added QSpinBox for selecting the peak for calibration (Page 4) ([`67405ee`](https://github.com/kstenio/libssa/commit/67405ee7cbff3c6eb6a54354fbf6ce66bc3f5d10))

* LIBSsa version: 2.0 alpha 27

Rebased "master" from "updating_spectra_object"
Now program is fully updates with Spectra object, with dicts and a more easy-to-track data structure

equations.py | export.py | spectra.py | libssagui.py | libssa.py
* Minor updates

spectra.py
* Added 'AreaSTD' key to self.fit

functions.py
* Added docstring for each function so far
* Updated the code and comments
* Updated fitpeaks
** Bug when tried use Trapezoidal rule fit when more than one peak as entered
** Added extra commentaries explaining some data structures
** Created elements as array rather than doing so before returning

imports.py
* Added docstring for each function so far
* Updated the code and comments

libssa.ui
* Updated version: 2.0a27 ([`703bd0b`](https://github.com/kstenio/libssa/commit/703bd0b85bb4d96f0d23cf876a1b5faa98cd9cd3))

* LIBSsa version: 2.0 alpha 26

spectra.py
* Added 'AreaSTD' key to self.fit

functions.py
* Fitpeaks is now fully functional when user chooses area1st
* Now it returns also an array for area_std

libssa_gui.py -> libssagui.py
* Fitplot received as parameter teh value for area_std
* Made some adjustments regardless the fitbox
** Updated how strings are created, and added a row for area_std (is not null)
** Better adjust of anchor position, as now it is outside the main data by a 1/20 factor of axis size

libssa.py
* Doplot (fitplot call) sends also self.spec.fit['AreaSTD']
* Disabled some prints (commented so far; will be removed after other tests)

libssa.ui
* Updated version: 2.0a26

worker.py -> Deleted ([`76230c5`](https://github.com/kstenio/libssa/commit/76230c5b9df1354d1c276a4968be3320d9bb5e32))

* LIBSsa version: 2.0 alpha 25

spectra.py
* Added 'NSamples' key to self.isolated

functions.py
* Fitresults now create raw numpy.zeros to return heights, widths and areas
* Fitpeaks had MANY changes in how data are stored
** It now returns shape
** Changed pre-alocation of nfevs, convergences, data, total, areas, widths and heights
** Tested on mean1st so far, but for every shape and multiple peak fitting
*** Size of elements may vary depend on how many peaks are being fitted
*** Now it creates numpy.zeros arrays
**** For nfevs and convergences it is plain vector (1D)
**** For data and total it is a cube (3D)
**** For areas, widths and heights it is a matrix (2D)
* TODO: area1st and multiple peaks

libssa_gui.py
* Fitplot received some updates to work with the new Spectra object
* Instead of just one parameter, now function has many
** ndarray: wavelength_iso, area, width, height, data, total
** str: shape
** int: nfev
** bool: convergence
* Adjusted inner elements for plotting to new data structure

libssa.py
* Changed loadrefcorrel name to loadref
* Peakiso saves spec.isolated['NSamples'] value
* Peakfit now gets returned values and stores in spec.fit structure dict (Spectra object)
** Doplot updated to use this new variable
* gui.p4_peak now uses spec.isolated['Element'] as item constructor

libssa.ui
* Updated version: 2.0a25 ([`2f942b2`](https://github.com/kstenio/libssa/commit/2f942b2178a80b5cebfb4da442c188717f9d765b))

* LIBSsa version: 2.0 alpha 24

spectra.py
* Split self.fit into two parts:
** self.isolated: contains count, element, center, upper and lower keys
** self.fit: contains area, width, height, shape, nfev, convergence, data and total keys

functions.py
* Removed List typing inside imports
* Isopeaks was adjusted to address new Spectra objects
** Now it returns aldo elements, lower, upper and center as numpy arrays
* Fitresults was updated to return: data, total_fit, heights, widths and areas
** Older fields were depreciated
* Started to work on fitpeaks to proper address the new Spectra object
** Returns were changed to: nfev, convercence, data, total, heights, widths and areas (as numpy arrays)
** As fitresults changed, many parts of the function needs updates
** For now, mean1st into single peak was tested
** TODO: area1st and multiple peaks

libssa.py
* Peakiso now is fully functional with new Spectra object
** Updated doplot to properly plot data based on new data structures.
*** Also changed strings in plots using format
* Started to work on peakfit to use new Spectra

libssa.ui
* Updated version: 2.0a24 ([`ffd7906`](https://github.com/kstenio/libssa/commit/ffd790688d92480417bc78e3286a0760a966ce00))

* LIBSsa version: 2.0 alpha 23

MAJOR CHANGE: In this version I've decided to start to work in a new branch namely "updating_spectra_object", as I realized that some of the strictures were starting to become more and more complicated to deal as complexity/modules were added.
After some thought, I opted to use dictionaries to better store the elements in the Spectra object. Now, every major global variable, for example, "wavelengths" have two or more keys (in this case, 'Raw' and 'Isolated'). Spectra-wise information are in "samples" variable, containing the keys 'Count', 'Name' and 'path', and so on...
This will take some time to finish because all functions that operates in those objects must be rewritten. But in the end everything is going to be fine. ;-)

spectra.py
* Major update. Changed names of almost every global variable
* Added clear method
* Added prototype methods for load and save
* Changed objects from worker.py to here. Also, made some tweaks in the Worker and WorkerSignals objects (still testing)

worker.py
* Minor changes (will be removed eventually)

imports.py
* Updated load and outliers functions to properly work with the new structures

libssa.py
* Replaced Worker import from worker.py to spectra.py
* Updated functions until page 2 to work with the new Spectra object
** doplot (will need further updates)
** setgrange (will need further updates)
** spopen
** spload
** outliers
** loadrefcorrel (TODO: change name in the next commit)
** docorrel

libssa.ui
* Updated version: 2.0a23 ([`87b2a00`](https://github.com/kstenio/libssa/commit/87b2a00f09d237bd64a0aa240a3f23204cea94d7))

* LIBSsa version: 2.0 alpha 21

spectra.py
* Renamed element prearson_ref to just _ref_

libssa_gui.py
* Added translator and connects for page 4 elements
* Created curvechanger do enable and disable combobox for normalization (calibration curve)
* Changed index in setgooptions for Calibration curve and PCA/PLS
* Created setpeaknorm method to add items to peak_norm_combo

libssa.py
* Added extra imports
* Implemented prototype method for page 4, docalibrationcurve, connected with the apply button in page 4
* Replaced self.spec.pearson_ref -> self.spec.ref in the code
* Reorganized indexes in setgrange
* Removed 'as_posix' in the code for Path elements (Windows/Linux better compatibility)
* Loadrefcorrel now creates elements lists for calibration curve combo box (TODO: change the name of this method)
* After peak fitting is done, the combo boxes in p4 are populated (peaks and norm_combo)

libssa.ui
* Swapped pages: Calibration Curve <-> PCA/PLS
* Added gui elements for page 4: Calibration curve
* Updated version: 2.0a22 ([`fdf6291`](https://github.com/kstenio/libssa/commit/fdf6291644f98495daf7db8ab5c2b5624c6b60c5))

* LIBSsa version: 2.0 alpha 21

functions.py
* Extra imports
* Implemented area first method for fitpeaks
* Inserted progress signal in fitpeaks

spectra.py
* Changed variable from counts_fit to fitresults

libssa_gui.py
* Organized fitplot to proper address box report if area1st and/or trapezoidal was selected

libssa.py
* Implemented worker/multithreading for peakfit
** However, seems like the effect is minimal (needs more investigation in the future)

libssa.ui
* Updated version: 2.0a21 ([`68848ad`](https://github.com/kstenio/libssa/commit/68848ad2783fee7d692cff592e5d950213799503))

* LIBSsa version: 2.0 alpha 20

functions.py
* Updated fit_results
** Now the results are a list of tuples instead an array
** Returns the shape
* Increase fit_peaks inner array from 6 to 7 (because of the extra shape parameter)

libssa_gui.py
* New imports: numpy std and pyqtgraph textitem
* Multiple updates to fitplot
** Added doctype
** Organizes better the variables
** Creates a box with multiple information of the fit, including shape,  results and RMSD (root mean square deviation)
*** Box need to proper show values for Trapezoidal (TO DO)

libssa.ui
* Updated version: 2.0a20 ([`b040b5c`](https://github.com/kstenio/libssa/commit/b040b5c50ad313797401d510869011c2b6fc7be9))

* LIBSsa version: 2.0 alpha 19

equations.py
* Updated Lorentzian equations to better address performance

functions.py
* Updated fit_guess to create guesses using a ratio
** Now the guesses are more accurate, what impacts in performance during least_squares
* Changed input for least_squares in fitpeaks
** Reduced tolerance for (f, g, x)tol from 1e-8 to 1e-7
** Added max_fev as 1000 (evaluations before declaring non convergence)

libssa_gui.py
* Created fitplot method, to address plot from fit more polished
** It receives the fitresults parameter, and condenses all needed plots
** Still need to show extra information. (TO DO!)

libssa.py
* Changed inner plots to calls fitplot from gui

libssa.ui
* Updated version: 2.0a19
* Fix inclination pre-selected as default
* Norm pre-enabled as default ([`fb6df21`](https://github.com/kstenio/libssa/commit/fb6df21d188b9b4f2c4611a71c8af2c97b606838))

* LIBSsa version: 2.0 alpha 18

functions.py
* Extra imports
* Moved position for fit guess
* Created two new siblings functions: fit_results and fit_values
** fit_results receives the optimized parameters and return every result from least_squares
** fit_values receives individual data for peaks and returns height, width and area of peak
* Now, fitpeaks calls fit_results for organizing data
** Added more elements to returned array (3 -> 6)

libssa_gui.py
* Imported mkPen from pyqtgraph (needed for plot width)
* Did some updates in splot in order to properly shows fit spectra
** Added 2 extra parameters: name and width
** MAYBE I'll create another method for fit plots... still thinking about it

libssa.py
* Updated doplot to [better] address fitted peaks graphics
** Organized data according to new data inside self.spec.counts_fit
** Added a legend for plot (original data, residuals, each peak and total)

libssa.ui
* Updated version: 2.0a18 ([`67c9fa0`](https://github.com/kstenio/libssa/commit/67c9fa09e7cc38db009b511ca5bc9af72d500fcf))

* LIBSsa version: 2.0 alpha 17

equations.py
* Added boundaries for asymmetry: needs to be between 0.2 and 0.8

functions.py
* Extra imports
* Now residuals return zero for trapezoidal rule shape
* Added val input type for fit_guess
* Corrected fig_guess to create guess correctly for asymmetric lorentzian
* Created equations_translator to return a dict with necessary data for fit
* Updated fit peaks to a proper functional version
** It woks only for mean 1st for now
** It returns a special structure with vectors for fit (will be changed in near versions to return more data)
** TO IMPLEMENT: Multi Threading!

libssa_gui.py
* Imported mkBrush from pyqtgraph
* Updated splot to do scatter plot (with brush instead of pen)
* Checktablevalues now raises error if user tries to isolate data before loading spectra
* Added translator for mean1st radio button

libssa.py
* Updated doplot to address fitted peaks graphics (same for setgrange)
* Peakfit method now is minimally functional, getting result from fitpeaks

libssa.ui
* Updated version: 2.0a17 ([`17f75a7`](https://github.com/kstenio/libssa/commit/17f75a754955fd8abb4a3c902c3286ed94804725))

* LIBSsa version: 2.0 alpha 16

functions.py
* Minor update in fitpeaks

libssa_gui.py
* Checktablevalues now receives as parameter the values of lower and upper wavelengths of spec.wavelength
** With these values, now is checks if user entered iso range inside spectra range
** Shows an error message in case of errors
* Minor update in names of shapes for fit table

libssa.py
* Now imports fitpeaks from functions
* Created minimal functional operations for peakfit
* Added error function for load spectra (!)
** New error is inside spload, and error signal is connected to this function
** If an error occurs, shows the exception type and error message
** Also, tells user to try change and/or header (commonly main causes for import errors)

libssa.ui
* Updated version: 2.0a16 ([`7dd89cb`](https://github.com/kstenio/libssa/commit/7dd89cb0607c09c034dc98232c4a9c21899282e5))

* LIBSsa version: 2.0 alpha 15

functions.py
* Corrected way new wavelength iso is created in isopeaks.

libssa_gui.py
* Created method for creating fit table by reading data from iso table

libssa.py
* Corrected the way center is sent to isopeaks

libssa.ui
* Updated version: 2.0a15

pic/icons
* Added new icons, "plus" and "minus" ([`74f4a22`](https://github.com/kstenio/libssa/commit/74f4a22372ada870ece1004ff7aa45acd75bf975))

* LIBSsa version: 2.0 alpha 14

equations.py
* Added extra imports and organized them better
* Created functions for Gaussian and Voigt(!) shapes (normal and fixed center variants)
* Updated previous Lorentzian shapes
* Moved residuals to -> functions.py

functions.py
* Received residuals from <- equations.py
* Added fit_guess function to auto create guess vector for fittings

spectra.py
* Added new element for receiving fit results: counts_fit

libssa.ui
* Updated version: 2.0a14 ([`e31f2ba`](https://github.com/kstenio/libssa/commit/e31f2baa678395df7ef804798c737240593d9d61))

* LIBSsa version: 2.0 alpha 13

equations.py
* Created functions for Lorentz shape (normal, fixed center and asymmetric variants)
* Created residuals function

libssa.ui
* Updated version: 2.0a13 ([`c4bb615`](https://github.com/kstenio/libssa/commit/c4bb6156cfe14567cd08db27ec96005ee71827f0))

* LIBSsa version: 2.0 alpha 12

equations.py
* Created new file
* Added equation for basic Lorentzian

functions.py
* Isopeaks now receives center list and adds values returned variables
* Created prototype for fitpeaks function

libssa_gui.py
* New import for strings punctuation
* Wide restructure of checktable method (addressed extra error possibilities)

libssa.py
* Sends center list to isopeaks

libssa.ui
* Updated version: 2.0a12 ([`109303d`](https://github.com/kstenio/libssa/commit/109303d950d9b176e9f504462cc0d715a60d271a))

* LIBSsa version: 2.0 alpha 11

ALL_FILES
* Updated year to 2021

LICENSE
* Changed folder: root -> doc

functions.py
* Added function isopeaks for peak isolation
* Function receives wavelength, counts, and elements/peaks range in order to cut spectra
* Multithreading fully functional

imports.py
* Changed PosixPath to Path in file declatarions

libssa_gui.py
* Added widgets declarations for linear and normalize check boxes
* Created connection for turing on and off norm based on linar correction
* Updated checktable to properly adress empty values in element name (inside iso table 1st column)
* Swaped "breaks" for "return False" in chacktablevalues, as in this way is easier to adress inconsistencies in main application

libssa.py
* Imports isopeaks from functions.py
* Added connection when p3_isoapply is pressed
* Updated doplot to acress particularities of isolated peaks data structure
** Same for setrange
* Added peakiso method for page 3
** It checks table data and perform isolation
** Results are passed to self.spec.wavelength_iso[elements] and self.spec.counts_iso[elements][samples]
* Created prototype for peakfit method

libssa.ui
* Updated version: 2.0a11 ([`1522c8c`](https://github.com/kstenio/libssa/commit/1522c8c79bfefc9e298e0b7c36e09a6b985c590c))

* libssa_gui.py
* Checktable method now checks if an element is repeated on 1st column and warn users
* Minor changes and corrections

libssa.ui
* Updated version: 2.0a10 ([`6c3ca9f`](https://github.com/kstenio/libssa/commit/6c3ca9fd63804cef7931faea4564895963f1cd5f))

* libssa_gui.py
* Updated changetable method (now it properly adds and removes rows)
* Created checktablevalues method for... check table values!
** This method is called chen isoapply button is pressed
** It checks all values in table: element, wavelength (range and center) and number of peaks
** Values can not be empty, center must be inside range, and center must match number of peaks

libssa.ui
* Updated version: 2.0a09 ([`70b288b`](https://github.com/kstenio/libssa/commit/70b288b8275ad25259981a28d43ce6d6628ff43c))

* Changes in files
* gui.py -> renamed to libssa_gui.py
* libssa_gui.py -> moved from /env to /pic

libssa.py
* Minor code changes

libssa_gui.py
* Added elements for page 3 (peaks)
* Organized connects as per page
* Created changetable method for add and remove isotable rows
** When row is added, '#Peaks' default value is set as '1'
* Created checktable method for signal emited by cellChanged signal
** This method checks if values entered by user are string, float or int (based on column)

libssa.ui
* Updated version: 2.0a08
* Added elements for page 3: Peaks and Fitting ([`26ad453`](https://github.com/kstenio/libssa/commit/26ad45395d2c18bfd00a7fcff627a6d4d66c554d))

* libssa.py
* Added try/except for major imports
* Created function which opens file dialog for selecting an spreadsheet and checks references
** If number of rows is not equal as number of samples, says an error message
** Connected menu entry (load reference) with new function
* Created new function to fully implement correlation spectrum with multi data
** Reference file is a spreadsheet with multiple columns, each for one element
** Plot engine updated to show Pearson, Zero and Average spectrum (from entire set)
** Tool button connected with function
* Added timestamp to prints

imports.py
* Extra imports
* Fully implemented correlation spectrum creation

gui.py
* Added menu entry for reference load
* Now all graph elements are disabled at start, and a graphenable method was implemented
* Minor changes in splot, now using dark random colors and with clear as parameter
* Minor changes in mplot, which can disable hsl if needed
* Added getOpenFileName in guifd
* Added method and connects for graph change buttons, minus and plus

spectra.py
* Added another element to carry references (self.pearson_ref)

libssa.ui
* Updated version: 2.0a07
* Changed names for all menu/actions ([`183171b`](https://github.com/kstenio/libssa/commit/183171b4595410df24b3c92cef0d52d039fd6c57))

* libssa.py
* Corrected dynamic box for MAD

imports.py
* Extra imports
* Fully implemented revised MAD (now performance is almost equal as SAM)

libssa.ui
* Updated version: 2.0a06
* Enabled elements for SAM (page 2) ([`aeee6b1`](https://github.com/kstenio/libssa/commit/aeee6b16768c84b1b49ac16d00f62d38b89a4547))

* libssa.py
* Connects for outliers apply button and double spin boxes
* Corrected plot for outliers
* Corrected dynamic box for imports (uses len of samples)
* Added main method for outliers removal algorithm. Does not depends on mode (SAM or MAD)
** Needs some error handling

gui.py
* Disabled keyboard tracking for outliers criteria (needed to proper connect valuechanged in main app)
* Changed name apply_out to apply_dot

imports.py
* Extra imports
* Added outliers removal function (so far, just SAM, needs MAD)

libssa.ui
* Updated version: 2.0a05 ([`4f2914d`](https://github.com/kstenio/libssa/commit/4f2914de32f5fd0ac86a01991a954d5d0d28b3e9))

* libssa.py
* Created prototype for outliers
* Minor code tweaks

gui.py
* Added elements of page 2 (__init__ and loadp2)
* Mode changer improved
* Moved connects to proper method
* Created method to enable and disable double spin boxes based on selected radio button

libssa.ui
* Updated version: 2.0a04
* Added menu instances
** File -> Load, save and quit entries
** Import -> References
** Export -> Multiple options (txt, xls and table)
** Help -> About
* Many menu entries have custom icons (by Font Awesome)

doc
* Added licence for Font Awesome Icons

pic/font
* Moved PT_Sans to folder

pic/icons
* Added multiple SVG files to folder ([`e48cac1`](https://github.com/kstenio/libssa/commit/e48cac17954d62e34c2bd28bdae40e73ac8270ab))

* libssa.py
* Minor organization of variables
* Added method for setting ranges and Titles for graph
** Method connected with activated signal of QComboBox (selg.gui.g_selector)
* New doplot method created
** It reads current graph type selected and select apropriated title and plots
* Graph spinbox (self.gui.g_current_sb) now plots graph after finished editing
* Method spload now just change selector index and asks for plot

gui.py
* Replaced color creation in graph
** Now uses hls_to_rgb from colorsys and colors are themed with application (purple)
* Added a new method for setting graph axis (setconfigoptions)
** Method connected with currentIndexChanged from QComboBox
* Minor organization of variables and helpers

spectra.py
* Added prototypes vectors for pca, pls, linear and temperature variables

libssa.ui
* Updated version: 2.0a03
* Changed graph selector names and added 2 extra types ([`7c1a87c`](https://github.com/kstenio/libssa/commit/7c1a87c7288f09c20bc01c1f7aa5c24b7da25383))

* Moved some GUI methods from main app to env.gui for better coding.

libssa.py
* Moved guimsg and guifd -> gui.py

functions.py
* Moved changestatus -> gui.py

gui.py
* Received changestatus as extra function
* Received guifd and guimsg as class methods

libssa.ui
* Updated version: 2.0a02 ([`1963d67`](https://github.com/kstenio/libssa/commit/1963d6790e800b3e9ad678f6636fcc691bd08fa8))

* gui.py
* Overall update of comments and descriptions
* Added PlotWidget (from pyqtgraph) and registered it as custom (promoted) widget in loadui
** Created methods for configuring graphic, single plot and matrix plot
** Wrote outer function for random HSV colors
* Moved main and graph elements to a loader method, as was already for the pages
* GUI connects are now inside class
** Added connect to disable wavelength and counts QSpinBox(es) if mode is changed (Single/Multiple)

spectra.py
* Updated wavelength is_sorted logic
** Now, instead of all(equal(arr1, arr2)), it is used array_equal(arr1, arr2)
* Replaced dtype in read_csv parameter and added inside to_numpy method of DataFrame

libssa.ui
* Updated version: 2.0a01

libssa.py
* Minor code organization ([`2c223ec`](https://github.com/kstenio/libssa/commit/2c223ec30112a1d0c4b05e1d35ed7a352dc0400f))

* gui.py
* Implemented new way to load/define elements in GUI
** This is done by creating the "clean" proprieties as QtWidgets, and the loading elements from self.loadpX (X == page number)
** As advantage, IDE now know element type, what makes easy to program
* Loaded statusbar

spectra.py
* Added arrays for samples and samples_pathlib, and n_samples int as well

worker.py
* Enabled finished signal

import.py -> imports.py
* Added delimiter selection into load module
* Corrected usecols (must be a list - 1)

functions.py
* Added function for showing messages in statusbar

libssa.ui
* Changed names structures for UI. Now it uses p1lB1 style (page 1 label 1)

libssa.py
* Extra imports
* Updated global variables
* Added variables() and connects() for simplifying __init__()
* Added main config for threadpool
* Added GUI helper for showing message boxes
* Added GUI helper for showing file dialogs
* Added GUI helper for showing dynamic message box
* Added prototype for global variables and connects (instead of using in __init__)
* Implemented methods spopen and spload (for selecting input folders and loading spectra into LIBSsa)
** Data is properly loaded, but performance is not improved. Needs more tweak. ([`abd87f8`](https://github.com/kstenio/libssa/commit/abd87f8dd850cff7152639ca135c0b240056080c))

* gui.py
* Updated tabulation for file

spectra.py
* Updated numpy array imports. Now the default is to use just the needed functions/methods/classes

worker.py
* Created classes for dealing with multithreading: WorkerSignals and Worker

import.py
* created load module, for importing spectra in Single and Multiple modes into LIBSsa

libssa.py
* Added prototype for global variables and connects (instead of using in __init__) ([`afe4b06`](https://github.com/kstenio/libssa/commit/afe4b0659d360caf638e20744587ea8775884146))

* gui.py
* Added methods for logo loading and qtoolbox styles

spectra.py
* Added prototype for Spectra class

libssa.svg
* Converted text to path

libssa.ui
* Change elements name and main h-spacer hint (7 to 10px)

libssa.py
* Added doctype
* Organized exceptions if ui or svg files are not found. ([`a3390b5`](https://github.com/kstenio/libssa/commit/a3390b5afff4ef1e94f9ab123c7813ba50e5092d))

* Added licence header in each py file.

libssa.ui
* Added graph widgets and prototype for QToolBox

gui.py
* Created module for load UI file
* Added variables for graph frame

libssa.py
* App class prototype
* Added loader of UI file ([`1d20e6b`](https://github.com/kstenio/libssa/commit/1d20e6b3b8c7228903be5fde91e38eafda2a491b))

* Second commit. Added base file structure for the application;
Created LIBSsa logo;
Created starter LIBSsa UI file;
In ".idea" folder all IDE configs are stored. ([`801f21d`](https://github.com/kstenio/libssa/commit/801f21d593b7f2991e5b7f6c647a85b3ceeba095))

* Initial commit ([`d084c12`](https://github.com/kstenio/libssa/commit/d084c1223624e4c41d42840ba861eb1079611ed6))