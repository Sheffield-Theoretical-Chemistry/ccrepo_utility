# %%
from ccrepo.fetch import fetch_basis
from ccrepo.containers import BasisSet, Shell

script_dir = os.path.dirname(os.path.realpath(__file__))
data_filepath = os.path.join(script_dir, 'data', 'sample_basis.txt')
with open(data_filepath) as sample_basis:
    sample_data = sample_basis.read()
    
basis_set = fetch_basis(["H", "B"], "cc-pVDZ", catalogue=sample_data)

def test_fetch_basis():
    # Assert that the basis set has the keys "B" and "H"
    assert "B" in basis_set
    assert "H" in basis_set

    # Assert that the objects in each key are ccrepo BasisSet objects
    assert isinstance(basis_set["B"], BasisSet)
    assert isinstance(basis_set["H"], BasisSet)


def test_shells():
    # Assert that the objects in the dict entry.shells are Shell objects
    for shell in basis_set["B"].shells:
        assert isinstance(shell, Shell)
    for shell in basis_set["H"].shells:
        assert isinstance(shell, Shell)


def test_exponents():
    # Assert that the exponents are correct
    assert basis_set["H"].shells[0].exps.tolist() == [
        1.301000e01,
        1.962000e00,
        4.446000e-01,
        1.220000e-01,
    ]
    assert basis_set["H"].shells[1].exps.tolist() == [7.270000e-01]

    assert basis_set["B"].shells[0].exps.tolist() == [
        4.570000e03,
        6.859000e02,
        1.565000e02,
        4.447000e01,
        1.448000e01,
        5.131000e00,
        1.898000e00,
        3.329000e-01,
        1.043000e-01,
    ]
    assert basis_set["B"].shells[1].exps.tolist() == [
        6.001000e00,
        1.241000e00,
        3.364000e-01,
        9.538000e-02,
    ]


# %%
