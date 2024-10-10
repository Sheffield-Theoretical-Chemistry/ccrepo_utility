# ccrepo_basis_set/writers.py

from . import ccrepo_logger

SUPPORTED_FORMATS = {}


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


@register_format("molpro")
def _convert_to_molpro(basis_sets: dict) -> str:
    """
    Convert a BasisSet object to a string in Molpro format.

    Args:
        basis_set (BasisSet): BasisSet object to be converted.

    Returns:
        str: String representation of the BasisSet object in Molpro format.
    """

    def _convert_shell(shell, element):
        """Convert a shell to a molpro shell string"""

        def format_coefficients(coefs):
            non_zero_indices = [i for i, coef in enumerate(coefs) if coef != 0.0]
            if not non_zero_indices:
                return ""

            start_index = non_zero_indices[0] + 1
            end_index = non_zero_indices[-1] + 1
            non_zero_coefs = coefs[start_index - 1 : end_index]
            non_zero_coefs = [f"{coef:.6E}" for coef in non_zero_coefs]
            return f"c, {start_index}.{end_index}, {', '.join(non_zero_coefs)};"

        return (
            f"{shell.l.lower()}, {element}, {', '.join(map(str,[f'{val:.6E}' for val in shell.exps.tolist()]))};\n"
            + "\n".join(
                [format_coefficients(coefs) for coefs in shell.coefs if format_coefficients(coefs)]
            )
        )

    def _create_element_string(basis_set):
        if basis_set.contraction:
            return (
                f"! {basis_set.element.capitalize()} {basis_set.contraction}"
                + "\n"
                + "\n".join(
                    [_convert_shell(shell, basis_set.element) for shell in basis_set.shells]
                )
                + "\n\n"
            )
        else:
            return (
                f"! {basis_set.element.capitalize()}"
                + "\n"
                + "\n".join(
                    [_convert_shell(shell, basis_set.element) for shell in basis_set.shells]
                )
                + "\n\n"
            )

    molpro_str = f"""
! Basis set from ccRepo https://grant-hill.group.shef.ac.uk/ccrepo/

spherical
basis={{

{''.join(_create_element_string(basis_sets[key]) for key in basis_sets)}
}}"""

    ccrepo_logger.info("Converted basis set to Molpro format.")
    return molpro_str

@register_format("psi4")
def _convert_to_psi4(basis_sets: dict) -> str:
    """
    Convert a BasisSet object to a string in psi4 format.

    Args:
        basis_set (BasisSet): BasisSet object to be converted.

    Returns:
        str: String representation of the BasisSet object in psi4 format.
    """
    def write_segment(segment):
        zipped_segment = zip(segment.exps, segment.coefs)
        segments_str = '\n     '.join([f"{exp:.6E}      {coef:.6E}" if str(coef).startswith('-') else f"{exp:.6E}\t{coef:.6E}" for exp, coef in zipped_segment]).replace('E', 'D')
        return f"""{segment.l.upper()}    {len(segment.exps)}    1.00\n     {segments_str}"""
    
    def write_shell(shell):
        return '\n'.join([write_segment(segment) for segment in shell.segments])
    
    def write_element(element):
        return f'{element.element.capitalize()}     0\n'+'\n'.join([write_shell(shell) for shell in element.shells])
    
    def write_basis(basis_set):
        return '****\n'+'\n****\n'.join([write_element(basis_sets[element]) for element in basis_sets])+'\n****'

    psi4_str = write_basis(basis_sets)
    return psi4_str

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