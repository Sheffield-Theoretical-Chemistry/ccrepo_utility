# setup.py
from setuptools import find_packages, setup

setup(
    name="ccrepo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "colorlog",
        "tqdm",
        "numpy",
    ],
)
