# ccRepo Utility

A utility to pull a basis set from ccRepo written by Shaun Donnelly (stedonnelly)

## Capabilities

The ccRepo package can current pull a basis set from the [ccRepo](http://www.grant-hill.group.shef.ac.uk/ccrepo/index.html) and can convert it to different formats for using in quantum chemistry packages.
Basis sets labelled with -PP should be used with ECPs from the [Stuttgart/Koeln library](https://www.tc.uni-koeln.de/PP/index.en.html).

It can currently convert a ccRepo basis to the following formats:

   - MOLPRO
   - Psi4
   - ORCA
   - Gaussian

The following formats can be read into a ccRepo basis:

   - MOLPRO

## Installation
   
You can install a local copy in a fresh environment from the top-level directory by running

    pip install -e .

## Contributing

Contributions are welcomed, either in the form of raising issues or pull requests on this repo.

## Examples

There are working examples in the examples folder, and these are (or will be) documented in the documentation. Documentation can be built by navigating to the docs folder locally 

    sphinx-build -b html . docs

You can then find the documentation by going to the docs folder and opening the index.html file in your browser.

## Acknowledging usage

If you use this information in your research, please consider citing the [ccRepo website](http://www.grant-hill.group.shef.ac.uk/ccrepo/index.html) as part of your paper.

You should also cite the original literature detailing the basis sets you use. A [full bibliography](http://www.grant-hill.group.shef.ac.uk/ccrepo/bib.html) can be found on ccRepo to help with this.
