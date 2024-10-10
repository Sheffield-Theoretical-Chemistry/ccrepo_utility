from . import register_format


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
        segments_str = '\n     '.join(
            [
                (
                    f"{exp:.6E}      {coef:.6E}"
                    if str(coef).startswith('-')
                    else f"{exp:.6E}\t{coef:.6E}"
                )
                for exp, coef in zipped_segment
            ]
        ).replace('E', 'D')
        return f"""{segment.l.upper()}    {len(segment.exps)}    1.00\n     {segments_str}"""

    def write_shell(shell):
        return '\n'.join([write_segment(segment) for segment in shell.segments])

    def write_element(element):
        return f'{element.element.capitalize()}     0\n' + '\n'.join(
            [write_shell(shell) for shell in element.shells]
        )

    def write_basis(basis_set):
        return (
            '****\n'
            + '\n****\n'.join([write_element(basis_sets[element]) for element in basis_sets])
            + '\n****'
        )

    psi4_str = write_basis(basis_sets)
    return psi4_str
