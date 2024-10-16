import os

from ccrepo.containers import BasisSet, Shell
from ccrepo import fetch_basis

script_dir = os.path.dirname(os.path.realpath(__file__))
data_filepath = os.path.join(script_dir, "data", "sample_basis.txt")
with open(data_filepath) as sample_basis:
    sample_data = sample_basis.read()
sample_data = sample_data.lower()

basis_set = fetch_basis(["H", "B"], 'cc-pVDZ',  catalogue=sample_data)


def test_fetch_basis():
    # Assert that the basis set has the keys "B" and "H"
    assert "b" in basis_set
    assert "h" in basis_set

    # Assert that the objects in each key are ccrepo BasisSet objects
    assert isinstance(basis_set["b"], BasisSet)
    assert isinstance(basis_set["h"], BasisSet)


def test_shells():
    # Assert that the objects in the dict entry.shells are Shell objects
    for shell in basis_set["b"].shells:
        assert isinstance(shell, Shell)
    for shell in basis_set["h"].shells:
        assert isinstance(shell, Shell)


def test_exponents():
    # Assert that the exponents are correct
    assert basis_set["h"].shells[0].exps.tolist() == [
        1.301000e+01,
        1.962000e+00,
        4.446000e-01,
        1.220000e-01,
    ]
    assert basis_set["h"].shells[1].exps.tolist() == [7.270000e-01]

    assert basis_set["b"].shells[0].exps.tolist() == [
        4.570000e+03,
        6.859000e+02,
        1.565000e+02,
        4.447000e+01,
        1.448000e+01,
        5.131000e+00,
        1.898000e+00,
        3.329000e-01,
        1.043000e-01,
    ]
    assert basis_set["b"].shells[1].exps.tolist() == [
        6.001000e+00,
        1.241000e+00,
        3.364000e-01,
        9.538000e-02,
    ]

