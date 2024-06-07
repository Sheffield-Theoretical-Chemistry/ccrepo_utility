#%%
# example_usage.py
from ccrepo_utility.fetch import fetch_file_from_repo, get_basis_set_block
from ccrepo_utility.process import parse_basis_set
from ccrepo_utility.utils import convert_to_basisopt_internal
from ccrepo_utility.converters import convert_to_format
from typing import Optional
from ccrepo_utility import fetch_basis 

mpro_basis = fetch_basis(["H", "He", "U"], "cc-pVDZ")
converted = convert_to_basisopt_internal(mpro_basis)
print(mpro_basis)
# %%
