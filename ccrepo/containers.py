# ccrepo_basis_set/containers.py

import numpy as np

from .writers import convert_to_format


class Shell:
    """Lightweight container for basis set Shells.

    Attributes:
         l (char): the angular momentum name of the shell
         exps (numpy array, float): array of exponents
         coefs (list): list of numpy arrays of equal length to exps,
             corresponding to coefficients for each exponent
    """

    def __init__(self):
        self.l = "s"
        self.exps = np.array([])
        self.coefs = []
        self.leg_params = ()


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

    def export_to_file(self, format: str, filename: str):
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
