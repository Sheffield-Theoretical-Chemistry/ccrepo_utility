# Description: Utility functions for basis set manipulation

from . import ccrepo_logger


def convert_to_basisopt_internal(basis_sets):
    """Used for converting the ccRepo BasisSet dictionary to a format compatible with the BasisOpt package.

    Args:
        basis_sets (dict): A dictionary of basis sets.

    Returns:
        InteralBasis: An object compatible with the BasisOpt package.
    """
    basisopt_internal = {}
    for key in basis_sets.keys():
        basisopt_internal[key] = basis_sets[key].shells
    return basisopt_internal


def export_basis_to_file(basis_set, filename):
    """
    Export the given basis set to a file.

    Args:
        basis_set (str): The basis set to export.
        filename (str): The name of the file to export the basis set to.

    Returns:
        None
    """
    with open(filename, "w") as export_basis:
        export_basis.write(basis_set)
        ccrepo_logger.info(f"Exported basis set to {filename}.")
