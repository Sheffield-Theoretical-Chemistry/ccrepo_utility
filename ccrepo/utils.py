# ccrepo/utils.py
# Description: Utility functions for basis set manipulation

from . import ccrepo_logger
from .containers import BasisSet, Shell


def convert_to_ccrepo(basisopt_basis):
    """Converts a basisopt internal basis to a ccrepo internal basis.

    Args:
        basisopt_basis (InternalBasis): Basisopt internal basis dictionary

    Returns:
        ccrepo_basis_set (dict): Dictionary of ccrepo BasisSet objects
    """
    ccrepo_basis_sets = {}
    for element in basisopt_basis:
        basis_set = BasisSet(element=element)
        for shell in basisopt_basis[element]:
            s = Shell()
            s.l = shell.l
            s.exps = shell.exps
            s.coefs = shell.coefs
            basis_set.shells.append(s)
        ccrepo_basis_sets[element] = basis_set
    return ccrepo_basis_sets


def convert_to_basisopt_internal(basis_sets):
    """Used for converting the ccRepo BasisSet dictionary to a format
        compatible with the BasisOpt package.

    Args:
        basis_sets (dict): A dictionary of basis sets.

    Returns:
        InternalBasis: An object compatible with the BasisOpt package.
    """
    basisopt_internal = {}
    for key in basis_sets.keys():
        basisopt_internal[key.lower()] = basis_sets[key].shells
    return basisopt_internal
