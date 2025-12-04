# ccrepo_basis_set/containers.py

import numpy as np

from .data import get_element_name
from .writers import convert_to_format


class Shell:
    """Lightweight container for basis set Shells.

    Attributes:
         l (char): the angular momentum name of the shell
         exps (numpy array, float): array of exponents
         coefs (list): list of numpy arrays of equal length to exps,
             corresponding to coefficients for each exponent
    """

    def __init__(
        self, l: str = None, exponents: np.ndarray = None, coefficients: np.ndarray = None
    ):
        self.l = l if l else "s"
        self.exps = exponents if exponents is not None else np.array([])
        self.coefs = coefficients if coefficients is not None else []
        self.leg_params = ()
        self.segments = []

    def __repr__(self):
        return f"Shell(l='{self.l}', n_exps={len(self.exps)}, n_contractions={len(self.coefs)})"


class Segment:
    """Lightweight container for basis set Segments.

    Attributes:
        exps (numpy array, float): array of exponents
        coefs (numpy array, float): array of coefficients
    """

    def __init__(self):
        self.exps = np.array([])
        self.coefs = np.array([])
        self.l = str


class BasisSet:
    """Container for basis set data for an element.

    Attributes:
        element (str): Element symbol.
        basis_set_name (str): Name of the basis set.
        primitives_info (str): Information about primitives.
        shells (list): List of Shell objects.
    """

    def __init__(
        self, element: str = None, basis_set_name: str = 'Untitled', primitives_info: str = None
    ):
        self.name = get_element_name(element)
        self.element = element
        self.basis_set_name = basis_set_name
        self.contraction = primitives_info
        self.shells = []

    def add_shell(self, shell: Shell):
        """Add a shell to the basis set.

        Args:
            shell (Shell): Shell object to add to the basis set.
        """
        self.shells.append(shell)
        self.segment_shell(shell)

    def segment_shell(self, shell):
        """Segment the shells into segments of exponents and coefficients."""
        exps = shell.exps
        coefs = shell.coefs

        segments = [np.array([exps, coef]) for coef in coefs]
        segments = [segment[:, segment[1] != 0] for segment in segments]
        for segment in segments:
            segment_container = Segment()
            segment_container.exps = segment[0]
            segment_container.coefs = segment[1]
            segment_container.l = shell.l
            shell.segments.append(segment_container)

    def export_to_file(self, filename: str, format: str):
        """
        Export the basis set to a file.

        Args:
            format (str): The format to export the basis set to.
            filename (str): The name of the file to export the basis set to.

        Returns:
            None
        """
        basis_set = convert_to_format(self, format)
        with open(filename, "w") as export_basis:
            export_basis.write(basis_set)
        print(f"Exported basis set to {filename}.")
