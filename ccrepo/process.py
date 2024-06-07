# ccrepo_basis_set/process.py

from .containers import Shell, BasisSet
import numpy as np


def parse_basis_set(input_data):
    basis_sets = {}
    blocks = input_data.strip().split("\n\n")

    for block in blocks:
        lines = block.strip().split("\n")

        # Parse header information
        header = lines[0].split(":")
        element, basis_set_name, contraction = header[0], header[1], header[2]
        max_angular_momentum = int(lines[1].strip())

        # Create BasisSet object
        basis_set = BasisSet(element, basis_set_name, contraction)

        # Initialize variables to store parsed data
        current_angular_momentum = ""
        exponents = []
        contraction_coeffs = []

        # Process each line of the basis set data
        for line in lines[2:]:
            parts = line.split()
            if (
                parts[0] in "SPDFGHIJKL"
            ):  # Check if the line starts with an angular momentum label
                if (
                    current_angular_momentum
                ):  # If there's an ongoing block, save it before starting a new one
                    shell = Shell()
                    shell.l = current_angular_momentum.lower()
                    shell.exps = np.array(exponents)
                    shell.coefs = [
                        np.array(coeff) for coeff in zip(*contraction_coeffs)
                    ]
                    basis_set.add_shell(shell)
                current_angular_momentum = parts[0]
                exponents = []
                contraction_coeffs = []
            else:
                exponents.append(float(parts[0]))
                contraction_coeffs.append([float(coeff) for coeff in parts[1:]])

        # Append the last block
        if current_angular_momentum:
            shell = Shell()
            shell.l = current_angular_momentum.lower()
            shell.exps = np.array(exponents)
            shell.coefs = [np.array(coeff) for coeff in zip(*contraction_coeffs)]
            basis_set.add_shell(shell)

        basis_sets[element] = basis_set

    return basis_sets
