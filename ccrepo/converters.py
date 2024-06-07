# ccrepo_basis_set/converters.py

from . import ccrepo_logger


def convert_to_format(basis_set, format: str) -> str:
    """
    Convert a BasisSet object to a string in the specified format.

    Args:
        basis_set (BasisSet): BasisSet object to be converted.
        format (str): Format to convert the BasisSet object to.

    Returns:
        str: String representation of the BasisSet object in the specified format.
    """
    if format == "nwchem":
        return _convert_to_nwchem(basis_set)
    elif format == "molpro":
        return _convert_to_molpro(basis_set)
    else:
        raise ValueError(f"Unsupported format: {format}")


def _convert_to_molpro(basis_sets: list) -> str:
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
        return (
            f"! {basis_set.element} {basis_set.contraction}"
            + "\n"
            + "\n".join([_convert_shell(shell, basis_set.element) for shell in basis_set.shells])
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
