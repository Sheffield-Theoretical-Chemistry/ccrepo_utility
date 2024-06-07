# ccrepo_basis_set/containers.py

import numpy as np


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

    def __init__(self, element, basis_set_name, primitives_info):
        self.element = element
        self.basis_set_name = basis_set_name
        self.contraction = primitives_info
        self.shells = []

    def add_shell(self, shell):
        self.shells.append(shell)
