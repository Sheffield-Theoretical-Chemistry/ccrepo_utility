# setup.py
from setuptools import find_packages, setup

setup(
    name="ccrepo",
    version="1.0.0b1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "colorlog",
        "tqdm",
        "numpy",
    ],
)
