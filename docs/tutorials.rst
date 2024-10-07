.. tutorials file

.. _`sec:tutorials`:

=========
Use example
=========

ccRepo is a fairly easy to use package with only a handful of functions. Several example cases will be given here for retrieving different basis sets.

Fetching the basis set from the utility
----------------------------------------

A basis set can be retrieved for a single element. This can be done by specifying the element and basis set for which you wish to retrieve. If no basis set is found for the element, then an exception will be raised.

.. code-block:: python

	import ccrepo
	
	basis = ccrepo.fetch_basis('H', 'cc-pVDZ')

In addition to just a single element, basis sets for multiple elements can also be retrieved by specifying the elements as a list.

.. code-block:: python
	
	basis = ccrepo.fetch_basis(['H','He','O','C'], 'cc-pVDZ')
	
Should all elements requested be missing, an exception will be raised. However, should only some elements be available for the specified basis set, ccRepo will return the available basis sets. A warning will be printed informing the user of any missing basis sets.

This will return an dictionary containing a series of BasisSet objects. Each basis set object has attributes that contain the type of basis set, the contraction scheme, and the shells. A user can retrieve the exponents or contraction coefficients for a shell in the basis set. The shells are ordered by increasing angular momentum.

.. code-block:: python
	
	basis_sets = ccrepo.fetch_basis(['H','N','O'], 'cc-pVQZ')
	hydrogen_basis = basis_sets['H']
	hydrogen_shells = basis_sets['H'].shells
	
	s_exponents = hydrogen_shells[0].exps
	s_contractions = hydrogen_shells[0].coefs

Converting the basis set from an internal object to a text file
----------------------------------------------------------------

Users may also wish to export a basis set for an element(s) to a text file. In order to do this the internal BasisSet object is first converted into a string in the a format used by a quantum chemistry package. For instance, save the basis set in MOLPRO format. The format argument is not case sensitive.

.. code-block:: python
	
	import ccrepo
	from ccrepo.converters import convert_to_format
	from ccrepo.utils import export_basis_to_file
	
	basis_sets = ccrepo.fetch_basis(['H','He'], 'cc-pVDZ')
	
	molpro_format = convert_to_format(basis_sets, format = 'molpro')
	
	export_basis_to_file(molpro_format, './H_He_cc_pVDZ.txt')
	
Alternatively a basis set can be retrieved in a specific format and then exported.

.. code-block:: python
	
	import ccrepo
	from ccrepo.utils import export_basis_to_file
	
	molpro_format = ccrepo.fetch_basis(['H','He'], 'cc-pVDZ', format = 'molpro')
	export_basis_to_file(molpro_format, './H_He_cc_pVDZ.txt')

Currently, ccRepo supports exporting in the following formats:

* MOLPRO
