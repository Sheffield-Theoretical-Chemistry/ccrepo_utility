# ccrepo/readers.py

# Description: This file contains functions to read basis set files in
# different formats into the ccrepo internal basis set format.

from .containers import BasisSet, Shell
import numpy as np


def read_basis_file(filename:str, basis_format: str):
    if basis_format == 'molpro':
        with open(filename, 'r') as f:
            basis_set_string = f.readlines()
            return _read_molpro_format(basis_set_string)
        
        
def _read_molpro_format(basis_set_string: str):
    current_element = None
    current_angular_momentum = None
    angular_momenta = 'spdfghijkl'
    basis_set_dict = {}
    
    for line in basis_set_string:
        if line in ['spherical', 'basis={', '}', '']:
            continue
        
        if ',' in line:
            angular_momentum, element, *values = line.replace(';','').strip().split(',')
            if angular_momentum in angular_momenta:
                current_angular_momentum = angular_momentum.lower()
                current_element = element.lower().strip()
                basis_set_dict.setdefault(current_element, {}).setdefault(current_angular_momentum, {})
                basis_set_dict[current_element][current_angular_momentum]['exponents'] = np.array(values, dtype=float)
                basis_set_dict[current_element][current_angular_momentum]['coefficients'] = []
            elif angular_momentum == 'c':
                coeff_idx_start, coeff_idx_finish = line.split(',')[1].split('.')
                coeff_idx_start = int(coeff_idx_start)-1
                coeff_idx_finish = int(coeff_idx_finish)
                coefficients_array = np.zeros(basis_set_dict[current_element][current_angular_momentum]['exponents'].shape)
                coefficients_array[coeff_idx_start:coeff_idx_finish] = np.array(values, dtype=float)
                basis_set_dict[current_element][current_angular_momentum]['coefficients'].append(coefficients_array)
    
    for element in basis_set_dict:
        basis_set = BasisSet(element=element)
        for angular_momentum in basis_set_dict[element]:
            shell = Shell()
            shell.l = angular_momentum
            shell.exps = basis_set_dict[element][angular_momentum]['exponents']
            shell.coefs = basis_set_dict[element][angular_momentum]['coefficients']
            basis_set.shells.append(shell)
        shell_exponents = [''.join([str(len(shell.exps)), shell.l]) for shell in basis_set.shells]
        shell_coefs = [''.join([str(len(shell.coefs)), shell.l]) for shell in basis_set.shells]
        basis_set.primitives_info = f'({"".join(shell_exponents)})->[{"".join(shell_coefs)}]'
        basis_set_dict[element] = basis_set
    
    return basis_set_dict
