# ccrepo_basis_set/writers.py

from .. import ccrepo_logger

SUPPORTED_FORMATS = {}


def supported_writers():
    return list(SUPPORTED_FORMATS.keys())


def register_format(format: str):
    """
    Decorator to register a format and add it to the supported_formats dictionary.

    Args:
        format (str): Format to be registered.

    Returns:
        callable: Decorator function.
    """

    def decorator(func):
        SUPPORTED_FORMATS[format] = func
        return func

    return decorator


def convert_to_format(basis_set, format: str) -> str:
    """
    Convert a BasisSet object to a string in the specified format.

    Args:
        basis_set (BasisSet): BasisSet object to be converted.
        format (str): Format to convert the BasisSet object to.

    Returns:
        str: String representation of the BasisSet object in the specified format.
    """
    if format in SUPPORTED_FORMATS.keys():
        return SUPPORTED_FORMATS[format](basis_set)
    else:
        raise ValueError(f"Unsupported format: {format}")


def write_basis(basis_sets, filename: str, format: str):
    """
    Export the given basis set to a file.

    Args:
        basis_set (str): The basis set to export.
        filename (str): The name of the file to export the basis set to.

    Returns:
        None
    """
    with open(filename, "w") as export_basis:
        basis_str = convert_to_format(basis_sets, format)
        export_basis.write(basis_str)
    ccrepo_logger.info(f"Exported basis set to {filename}.")
