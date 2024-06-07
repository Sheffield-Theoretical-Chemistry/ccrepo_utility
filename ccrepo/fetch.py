# ccrepo_basis_set/fetch.py

from typing import Union, Optional

from .process import parse_basis_set
from .converters import convert_to_format

from . import ccrepo_logger

from . import catalogue


def get_basis_set_block(
    content: str, elements: Union[str, list], basis_set_name: str
) -> str:
    """
    Extract the basis set block for a given element and basis set name.

    Parameters:
        content (str): The content of the basis set file.
        element (list or str): The element symbol.
        basis_set_name (str): The name of the basis set.

    Returns:
        str: The block of the basis set for the specified element and basis set name.
    """
    lines = content.split("\n")
    blocks = []
    capture = False
    current_block = []

    if type(elements) == str:
        elements = [elements]

    available_basis = []

    for line in lines:
        if any(line.startswith(f"{element}:{basis_set_name}:") for element in elements):
            available_basis.append(line.split(":")[0])
            capture = True
            current_block = [line]
        elif capture:
            if line.strip() == "":
                capture = False
                blocks.append("\n".join(current_block))
                current_block = []
            else:
                current_block.append(line)

    # Append the last captured block if it wasn't appended yet
    if capture and current_block:
        blocks.append("\n".join(current_block))

    # for element in elements:
    #     if element not in available_basis:
    #         print(
    #             f"No {basis_set_name} found for element {element} in the ccRepo catalogue."
    #         )

    unavailable_basis = [
        element for element in elements if element not in available_basis
    ]
    if blocks:
        ccrepo_logger.info(
            f"Found {basis_set_name} for element(s) {','.join(available_basis)} in the ccRepo catalogue."
        )
        if unavailable_basis:
            ccrepo_logger.warning(
                f"No {basis_set_name} found for element(s) {','.join(unavailable_basis)} in the ccRepo catalogue."
            )
        return "\n\n".join(blocks), available_basis
    else:
        raise ValueError(
            f"No basis set blocks found for elements {elements} with basis set {basis_set_name}"
        )


def fetch_basis(
    elements: list,
    basis_set_name: str,
    format: Optional[list] = None,
    export: Optional[bool] = None,
    filepath: str = None,
) -> dict:
    """Fetches a basis set from the ccRepo basis set catalogue.

    Args:
        elements (list): List of element symbols.
        basis_set_name (str): Basis set name to fetch
        format (Optional[list]): If specified, the basis set will be converted to the specified format.

    Returns:
        dict: Dictionary containing the basis set information.
    """
    basis_set_block, available_basis = get_basis_set_block(
        catalogue, elements, basis_set_name
    )
    parsed_basis_sets = parse_basis_set(basis_set_block)
    if format:
        converted_basis = convert_to_format(parsed_basis_sets, format.lower())
        ccrepo_logger.info(
            f"Fetched basis set for element(s) {', '.join(available_basis)} with basis set {basis_set_name} from the ccRepo catalogue and converted fo format {format}."
        )
        if not export:
            return converted_basis
        elif export:
            if not filename:
                raise ValueError(
                    "No filename specified for export. Please set this using the filename parameter."
                )
            return converted_basis

        return
    else:
        ccrepo_logger.info(
            f"Fetched basis set for element(s) {', '.join(available_basis)} with basis set {basis_set_name} from the ccRepo catalogue."
        )
        return parsed_basis_sets
