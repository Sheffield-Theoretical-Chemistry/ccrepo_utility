# Description: Utility functions for basis set manipulation


def convert_to_basisopt_internal(basis_sets):
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
    with open(filename) as export_basis:
        export_basis.write(basis_set, "w")
