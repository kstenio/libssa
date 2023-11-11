# Contributing to LIBSsa

Thank you for your interest in supporting LIBSsa! I aim to make contributing to this project as easy and transparent as possible, whether it's for:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Contacting or even becoming a maintainer

Additionally, there's a [Features in need](#Features-in-need) section, where I've highlighted functionalities that I believe LIBSsa 
should have but currently lack due to time constraints. If you're looking for a place to start, consider these.

## Version Control System: GitHub

LIBSsa is hosted on [GitHub](https://github.com/kstenio/libssa), and the entire history of software development is available 
in the [repository commits](https://github.com/kstenio/libssa/commits). I also use this platform to track issues and feature 
requests and to accept pull requests.

## LIBSsa uses GitHub Flow

[GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow) is a branch-based workflow. This means that all 
code changes happen through **pull requests**. So, until you become an official contributor, pull requests are the only way to 
propose changes to the codebase. You can follow these steps:

1. Fork the [LBSsa repository](https://github.com/kstenio/libssa) and create your branch from `master`.
2. If you've added code that should be tested, please include tests.
3. Ensure the tests (if applicable) pass.
4. Ensure your code adheres to our linting standards.
5. Open a pull request!

## Any contributions will be under the AGPLv3 License

In short, when you submit code changes, your submissions are understood to be under the same license as the official repository, 
which is the [GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html.en). This is a strong copyleft license, 
ensuring that LIBSsa will remain open and free for all.

## Reporting bugs using GitHub's _issues_

I use GitHub issues to track public bugs. Reporting a bug is as simple as [opening a new issue](https://github.com/kstenio/libssa/issues).

## Writing bug reports with detail, background, data, and/or sample code

**Great Bug Reports** tend to include:

- A quick summary and/or background
- Specific steps to reproduce the issue
	- Providing sample code, data, or spectra, if possible
- What you expected to happen
- What actually happened
- Notes, possibly including your insights into why the issue is happening or details of what you've already tried that didn't work

## Using a Consistent Coding Style

* LIBSsa uses **tabs** for indentation rather than spaces.
* I recommend using an integrated development environment (IDE) like [PyCharm](https://www.jetbrains.com/pycharm/) to help identify issues, typos, etc.
* Functions and methods should have docstrings.
* Variable names should be in English.
* Whenever possible, use comments to explain your code.

## Features in need

These are previously identified improvements that LIBSsa could benefit from. If you'd like to contribute, this is a good place to start. 
Additional features that could be implemented include:

1. Testing
	1. Implementing automated tests as LIBSsa currently lacks additional testing algorithms.
2. Performance improvements
	1. Restructuring data within the program, for instance, using larger order NumPy arrays.
	2. Enhancing algorithms to use fewer loops and apply more matrix algebra.
	3. Studying variable types for format optimizations to reduce RAM memory consumption.
	4. Optimizing cache usage.
3. Architectural improvements
	1. Creating a new Spectra class or updating the existing one to implement class methods for data processing (minimizing the main program operations).
	2. Modifying the GUI library or updating the program to new versions of PySide, including new features for better use of processing and RAM memory.
	3. Updating LIBSsa to work with newer versions of Python, like 3.10 and 3.11 (this includes checking newer versions of libraries as well) 
4. Feature improvements, including:
	1. New data processing algorithms.
	2. New quantification models, including non-linear ones.
	3. New classification models.
5. Adjustments and fixes
	1. Improving current functions.
	2. Correcting any bugs.
	3. Optimizing the existing code.

## Contact

You can find my contact information throughout the code. In case you missed it, you can [email me](mailto:kleydson.stenio@gmail.com?Subject=LIBSsa_Contributing). 
Feel free to contact me for any information not available in this guide, or if you're interested in becoming a maintainer. 
I'm available to provide feedback and assistance with code and issues.

## References

This document was adapted from [this template](https://gist.github.com/briandk/3d2e8b3ec8daf5a27a62).
