# ccrepo/data.py

# Description: This file contains the data structures used in the ccrepo package.

from typing import Optional, Union

from .api import fetch_file_from_repo

ELEMENTS = [
    "H",
    "He",
    "Li",
    "Be",
    "B",
    "C",
    "N",
    "O",
    "F",
    "Ne",
    "Na",
    "Mg",
    "Al",
    "Si",
    "P",
    "S",
    "Cl",
    "Ar",
    "K",
    "Ca",
    "Sc",
    "Ti",
    "V",
    "Cr",
    "Mn",
    "Fe",
    "Ni",
    "Co",
    "Cu",
    "Zn",
    "Ga",
    "Ge",
    "As",
    "Se",
    "Br",
    "Kr",
    "Rb",
    "Sr",
    "Y",
    "Zr",
    "Nb",
    "Mo",
    "Tc",
    "Ru",
    "Rh",
    "Pd",
    "Ag",
    "Cd",
    "In",
    "Sn",
    "Sb",
    "Te",
    "I",
    "Xe",
    "Cs",
    "Ba",
    "La",
    "Ce",
    "Pr",
    "Nd",
    "Pm",
    "Sm",
    "Eu",
    "Gd",
    "Tb",
    "Dy",
    "Ho",
    "Er",
    "Tm",
    "Yb",
    "Lu",
    "Hf",
    "Ta",
    "W",
    "Re",
    "Os",
    "Ir",
    "Pt",
    "Au",
    "Hg",
    "Tl",
    "Pb",
    "Bi",
    "Th",
    "Pa",
    "U",
    "Np",
    "Pu",
    "Am",
    "Cm",
    "Bk",
    "Cf",
    "Es",
    "Fm",
    "Md",
    "No",
    "Lr",
    "Rf",
    "Db",
    "Sg",
    "Bh",
    "Hs",
    "Mt",
    "Ds",
    "Rg",
    "Cn",
    "Nh",
    "Fl",
    "Mc",
    "Lv",
    "Ts",
    "Og",
]

catalogue = fetch_file_from_repo()


def basis_availability(catalogue: str, elements: list = None):
    basis_set_availablity = {}
    contractions = {}
    for line in catalogue.split("\n"):
        if ':' in line:
            try:
                element, basis, contraction_scheme = line.split(':')
                if element.capitalize() in ELEMENTS:
                    if element.capitalize() not in basis_set_availablity:
                        basis_set_availablity[element.capitalize()] = []
                    basis_set_availablity[element].append(basis)
                    if element.capitalize() not in contractions:
                        contractions[element.capitalize()] = {}
                    contractions[element.capitalize()][basis] = contraction_scheme
            except:
                pass

    if elements:
        return {element: basis_set_availablity[element] for element in elements}, {
            element: contractions[element] for element in elements
        }

    return basis_set_availablity, contractions


BASIS_SETS, CONTRACTION_SCHEMES = basis_availability(catalogue)


def availability(elements: Optional[Union[list, str]] = None) -> dict:
    """
    Returns a list of all available basis sets in the ccRepo database.

    Returns:
        list: A list of all available basis sets.
    """
    if elements:
        if isinstance(elements, list):
            if isinstance(elements, tuple):
                elements = list(elements)
            else:
                elements = [elements]
        return {element: BASIS_SETS[element] for element in elements}
    return BASIS_SETS
