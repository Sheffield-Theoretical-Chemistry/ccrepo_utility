# ccrepo_basis_set/__init__.py

from .fetch import fetch_file_from_repo, get_basis_set_block
from .process import parse_basis_set
from .utils import convert_to_basisopt_internal
from .converters import convert_to_format
from typing import Optional

personal_access_token = "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"


def fetch_basis(elements: list, basis_set_name: str, format: Optional[list] = None) -> dict:
    """Fetches a basis set from the ccRepo basis set catalogue.

    Args:
        elements (list): List of element symbols.
        basis_set_name (str): Basis set name to fetch
        format (Optional[list]): If specified, the basis set will be converted to the specified format.

    Returns:
        dict: Dictionary containing the basis set information.
    """
    catalogue = fetch_file_from_repo(personal_access_token)
    basis_set_block = get_basis_set_block(catalogue, elements, basis_set_name)
    parsed_basis_sets = parse_basis_set(basis_set_block)
    if format:
        converted_basis = convert_to_format(parsed_basis_sets, format)
        return converted_basis
    else:
        return parsed_basis_sets
