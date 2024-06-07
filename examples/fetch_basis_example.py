#%%

from ccrepo.fetch import fetch_basis
from ccrepo.converters import convert_to_format
from ccrepo.utils import export_basis_to_file

basis = fetch_basis("H", "cc-pVDZ")

#molpro_format = convert_to_format(basis, "molpro")

#export_basis_to_file(molpro_format, "H_He_cc_pVDZ.txt")

# %%

basis2 = fetch_basis("He", "cc-pVDZ")
# %%
