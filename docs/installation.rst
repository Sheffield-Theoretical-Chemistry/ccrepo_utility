.. ccRepo installation

.. _`sec:installation`:

=============
Installation
=============

ccRepo can be installed via pip using the command::

		pip install ccrepo

Installing from source
----------------------

ccRepo can also be installed from the github source directly::

		pip install git+ https://github.com/Sheffield-Theoretical-Chemistry/ccrepo_utility.git
		
Alternatively, ccRepo can be installed from a local directory which you may have locally developed. It is recommended that you do this in a clean python environment.
You can install it by navigating to the top-level directory using the command::

		pip install -e .
		
Dependencies
-------------

* Python >= 3.10
* color >= 2.32.3
* tqdm >= 4.66.4
* numpy >= 1.26.4
* requests >= 2.32.3


