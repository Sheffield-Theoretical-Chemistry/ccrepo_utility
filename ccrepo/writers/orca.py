from ..data import get_element_name
from . import register_format


@register_format("orca")
def _convert_to_orca(basis_sets: dict) -> str:
    """
    Convert a BasisSet object to a string in psi4 format.

    Args:
        basis_set (BasisSet): BasisSet object to be converted.

    Returns:
        str: String representation of the BasisSet object in psi4 format.
    """

    def write_segment(segment):
        zipped_segment = zip(segment.exps, segment.coefs)
        segments_str = '\n'.join(
            [
                (
                    f"{idx+1}         {exp:.6E}          {coef:.6E}"
                    if str(coef).startswith('-')
                    else f"{idx+1}         {exp:.6E}           {coef:.6E}"
                )
                for idx, (exp, coef) in enumerate(zipped_segment)
            ]
        )
        return f"""{segment.l.upper()}   {len(segment.exps)}\n{segments_str}"""

    def write_shell(shell):
        return '\n'.join([write_segment(segment) for segment in shell.segments])

    def write_element(element):
        return f'{get_element_name(element.element.capitalize()).upper()}\n' + '\n'.join(
            [write_shell(shell) for shell in element.shells]
        )

    def write_basis(basis_set):
        return (
            "$DATA \n\n"
            + ('\n\n'.join([write_element(basis_sets[element]) for element in basis_sets]))
            + "\n\n$END"
        )

    psi4_str = write_basis(basis_sets)
    return psi4_str
