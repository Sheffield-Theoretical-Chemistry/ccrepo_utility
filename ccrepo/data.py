# ccrepo/data.py

# Description: This file contains the data structures used in the ccrepo package.

from typing import Optional, Union

from .api import fetch_file_from_repo

ELEMENT_NAMES = {
    "H": "Hydrogen",
    "He": "Helium",
    "Li": "Lithium",
    "Be": "Beryllium",
    "B": "Boron",
    "C": "Carbon",
    "N": "Nitrogen",
    "O": "Oxygen",
    "F": "Fluorine",
    "Ne": "Neon",
    "Na": "Sodium",
    "Mg": "Magnesium",
    "Al": "Aluminum",
    "Si": "Silicon",
    "P": "Phosphorus",
    "S": "Sulfur",
    "Cl": "Chlorine",
    "Ar": "Argon",
    "K": "Potassium",
    "Ca": "Calcium",
    "Sc": "Scandium",
    "Ti": "Titanium",
    "V": "Vanadium",
    "Cr": "Chromium",
    "Mn": "Manganese",
    "Fe": "Iron",
    "Co": "Cobalt",
    "Ni": "Nickel",
    "Cu": "Copper",
    "Zn": "Zinc",
    "Ga": "Gallium",
    "Ge": "Germanium",
    "As": "Arsenic",
    "Se": "Selenium",
    "Br": "Bromine",
    "Kr": "Krypton",
    "Rb": "Rubidium",
    "Sr": "Strontium",
    "Y": "Yttrium",
    "Zr": "Zirconium",
    "Nb": "Niobium",
    "Mo": "Molybdenum",
    "Tc": "Technetium",
    "Ru": "Ruthenium",
    "Rh": "Rhodium",
    "Pd": "Palladium",
    "Ag": "Silver",
    "Cd": "Cadmium",
    "In": "Indium",
    "Sn": "Tin",
    "Sb": "Antimony",
    "Te": "Tellurium",
    "I": "Iodine",
    "Xe": "Xenon",
    "Cs": "Cesium",
    "Ba": "Barium",
    "La": "Lanthanum",
    "Ce": "Cerium",
    "Pr": "Praseodymium",
    "Nd": "Neodymium",
    "Pm": "Promethium",
    "Sm": "Samarium",
    "Eu": "Europium",
    "Gd": "Gadolinium",
    "Tb": "Terbium",
    "Dy": "Dysprosium",
    "Ho": "Holmium",
    "Er": "Erbium",
    "Tm": "Thulium",
    "Yb": "Ytterbium",
    "Lu": "Lutetium",
    "Hf": "Hafnium",
    "Ta": "Tantalum",
    "W": "Tungsten",
    "Re": "Rhenium",
    "Os": "Osmium",
    "Ir": "Iridium",
    "Pt": "Platinum",
    "Au": "Gold",
    "Hg": "Mercury",
    "Tl": "Thallium",
    "Pb": "Lead",
    "Bi": "Bismuth",
    "Po": "Polonium",
    "At": "Astatine",
    "Rn": "Radon",
    "Fr": "Francium",
    "Ra": "Radium",
    "Ac": "Actinium",
    "Th": "Thorium",
    "Pa": "Protactinium",
    "U": "Uranium",
    "Np": "Neptunium",
    "Pu": "Plutonium",
    "Am": "Americium",
    "Cm": "Curium",
    "Bk": "Berkelium",
    "Cf": "Californium",
    "Es": "Einsteinium",
    "Fm": "Fermium",
    "Md": "Mendelevium",
    "No": "Nobelium",
    "Lr": "Lawrencium",
    "Rf": "Rutherfordium",
    "Db": "Dubnium",
    "Sg": "Seaborgium",
    "Bh": "Bohrium",
    "Hs": "Hassium",
    "Mt": "Meitnerium",
    "Ds": "Darmstadtium",
    "Rg": "Roentgenium",
    "Cn": "Copernicium",
    "Nh": "Nihonium",
    "Fl": "Flerovium",
    "Mc": "Moscovium",
    "Lv": "Livermorium",
    "Ts": "Tennessine",
    "Og": "Oganesson",
}

NAME_ELEMENTS = {v: k for k, v in ELEMENT_NAMES.items()}

ELEMENTS = list(ELEMENT_NAMES.keys())

catalogue = fetch_file_from_repo()


def basis_availability(catalogue: str):
    """Get the availability of basis sets and contraction schemes for each element.

    Args:
        catalogue (str): ccRepo catalogue fetched from github

    Returns:
        tuple: A tuple containing the availability of basis sets and contraction schemes for each element.
    """
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
    basis_set_availablity = {
        element: basis_set_availablity[element]
        for element in ELEMENTS
        if element in basis_set_availablity
    }
    contractions = {
        element: contractions[element] for element in ELEMENTS if element in contractions
    }
    return basis_set_availablity, contractions


def element_availability(catalogue: str):
    """Get the availability of elements for a given basis set.

    Args:
        catalogue (str): ccRepo catalogue fetched from github

    Returns:
        dict: A dictionary containing the availability of elements for a given basis set.
    """
    elements_for_basis = {}
    for line in catalogue.split("\n"):
        if ':' in line:
            element, basis, contraction_scheme = line.split(':')
            if basis.lower() not in elements_for_basis:
                elements_for_basis[basis.lower()] = []
            elements_for_basis[basis.lower()].append(element)
    elements_for_basis = {
        basis: sorted(
            elements_for_basis[basis], key=lambda element: ELEMENTS.index(element.capitalize())
        )
        for basis in elements_for_basis
    }
    return elements_for_basis


BASIS_SETS, CONTRACTION_SCHEMES = basis_availability(catalogue)
BASIS_ELEMENTS = element_availability(catalogue)


def get_elements(basis_set: str) -> list:
    """
    Returns a list of elements for which a basis set is available.

    Args:
        basis_set (str): The basis set for which elements are required.

    Returns:
        list: A list of elements for which the basis set is available.
    """
    return BASIS_ELEMENTS[basis_set.lower()]


def get_basis(elements: Optional[Union[list, str]] = None) -> dict:
    """
    Returns a list of all available basis sets in the ccRepo database.

    Args:
        elements (Optional[Union[list, str]], optional): List of elements for which basis sets are required. Defaults to None.

    Returns:
        list: A list of all available basis sets.
    """
    if elements:
        if not isinstance(elements, list):
            if isinstance(elements, tuple):
                elements = list(elements)
            else:
                elements = [elements]
        return {element.capitalize(): BASIS_SETS[element.capitalize()] for element in elements}
    return BASIS_SETS


def get_element_name(element: str) -> str:
    """
    Returns the name of an element given its symbol.

    Args:
        element (str): The symbol of the element.

    Returns:
        str: The name of the element.
    """
    return ELEMENT_NAMES[element.capitalize()]


def get_element_symbol(element: str) -> str:
    """
    Returns the symbol of an element given its name.

    Args:
        element (str): The name of the element.

    Returns:
        str: The symbol of the element.
    """
    return NAME_ELEMENTS[element.capitalize()]