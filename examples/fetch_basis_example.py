import ccrepo
from ccrepo.writers import write_basis, convert_to_format

basis_sets = ccrepo.fetch_basis(['H', 'He'], 'cc-pVDZ')

write_basis(basis_sets, filename='./H_He_cc_pVDZ.txt', format='molpro')  # Writes basis to file

molpro_str = convert_to_format(basis_sets, 'molpro')  # Returns molpro string
