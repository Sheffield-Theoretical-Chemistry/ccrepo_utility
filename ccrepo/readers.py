# ccrepo/readers.py

# Description: This file contains functions to read basis set files in
# different formats into the ccrepo internal basis set format.

import re
from collections import defaultdict

import numpy as np

from .containers import BasisSet, Shell

SUPPORTED_FORMATS = {}


def read_basis_file(filename: str, format: str) -> BasisSet:
    if format in SUPPORTED_FORMATS.keys():
        with open(filename, 'r') as f:
            basis_set_string = f.read()
            return SUPPORTED_FORMATS[format](basis_set_string)


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
def _read_molpro_format(basis_set_string: str) -> BasisSet:
    current_element = None
    current_angular_momentum = None
    angular_momenta = 'spdfghijkl'
    basis_set_dict = {}

    basis_set_string = basis_set_string.strip().splitlines()

    for line in basis_set_string:
        if line in ['spherical', 'basis={', '}', '']:
            continue

        if ',' in line:
            angular_momentum, element, *values = line.replace(';', '').strip().split(',')
            if angular_momentum in angular_momenta:
                current_angular_momentum = angular_momentum.lower()
                current_element = element.lower().strip()
                basis_set_dict.setdefault(current_element, {}).setdefault(
                    current_angular_momentum, {}
                )
                basis_set_dict[current_element][current_angular_momentum]['exponents'] = np.array(
                    values, dtype=float
                )
                basis_set_dict[current_element][current_angular_momentum]['coefficients'] = []
            elif angular_momentum == 'c':
                coeff_idx_start, coeff_idx_finish = line.split(',')[1].split('.')
                coeff_idx_start = int(coeff_idx_start) - 1
                coeff_idx_finish = int(coeff_idx_finish)
                coefficients_array = np.zeros(
                    basis_set_dict[current_element][current_angular_momentum]['exponents'].shape
                )
                coefficients_array[coeff_idx_start:coeff_idx_finish] = np.array(values, dtype=float)
                basis_set_dict[current_element][current_angular_momentum]['coefficients'].append(
                    coefficients_array
                )

    for element in basis_set_dict:
        basis_set = BasisSet(element=element)
        for angular_momentum in basis_set_dict[element]:
            shell = Shell()
            shell.l = angular_momentum
            shell.exps = basis_set_dict[element][angular_momentum]['exponents']
            shell.coefs = basis_set_dict[element][angular_momentum]['coefficients']
            basis_set.add_shell(shell)
        shell_exponents = [''.join([str(len(shell.exps)), shell.l]) for shell in basis_set.shells]
        shell_coefs = [''.join([str(len(shell.coefs)), shell.l]) for shell in basis_set.shells]
        basis_set.primitives_info = f'({"".join(shell_exponents)})->[{"".join(shell_coefs)}]'
        basis_set_dict[element] = basis_set

    return basis_set_dict


def _parse_gaussian_format(basis_text: str) -> dict[str, list[Shell]]:
    """
    Parse a Gaussian-style basis set and return Shells organized by element.

    Returns:
        dict mapping element symbol to list of Shell objects
    """
    lines = basis_text.strip().split('\n')

    # Storage: {element: {ang_mom: [(exps, coefs), ...]}}
    raw_data = defaultdict(lambda: defaultdict(list))
    current_element = None

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Check for element header (e.g., "B     0" or "He    0")
        elem_match = re.match(r'^([A-Z][a-z]?)\s+\d+$', line)
        if elem_match:
            current_element = elem_match.group(1)
            i += 1
            continue

        # Check for angular momentum header (e.g., "S    6    1.00")
        header_match = re.match(r'^([SPDFGHIKLMN])\s+(\d+)\s+[\d.]+$', line)
        if header_match and current_element:
            ang_mom = header_match.group(1).lower()
            n_prims = int(header_match.group(2))

            exps = []
            coefs = []

            for j in range(n_prims):
                i += 1
                data_line = lines[i].replace('D', 'E')
                parts = data_line.split()
                exps.append(float(parts[0]))
                coefs.append(float(parts[1]))

            raw_data[current_element][ang_mom].append((exps, coefs))

        i += 1

    # Build result: consolidate by angular momentum into Shell objects
    result = {}

    for element, ang_mom_blocks in raw_data.items():
        basis_set = BasisSet(element=element)

        for ang_mom, blocks in ang_mom_blocks.items():
            # Collect all unique exponents
            all_exps = []
            exp_to_idx = {}

            for exps, _ in blocks:
                for exp in exps:
                    key = round(exp, 10)
                    if key not in exp_to_idx:
                        exp_to_idx[key] = len(all_exps)
                        all_exps.append(exp)

            # Build coefficient arrays aligned to all_exps
            all_coefs = []
            for exps, coefs in blocks:
                coef_array = np.zeros(len(all_exps))
                for exp, coef in zip(exps, coefs):
                    key = round(exp, 10)
                    idx = exp_to_idx[key]
                    coef_array[idx] = coef
                all_coefs.append(coef_array)

            shell = Shell(l=ang_mom, exponents=np.array(all_exps), coefficients=all_coefs)
            basis_set.add_shell(shell)

        result[element.lower()] = basis_set

    return result


@register_format("gaussian")
def read_gaussian_basis_file(basis_set_string) -> dict[str, BasisSet]:
    basis_set_string_split = [block for block in basis_set_string.split("*") if block]
    basis_sets = {}
    for block in basis_set_string_split:
        parsed_sets = _parse_gaussian_format(block)
        basis_sets.update(parsed_sets)
    return basis_sets
