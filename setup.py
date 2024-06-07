# setup.py
from setuptools import find_packages, setup

setup(
    name="ccrepo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.3",
        "colorlog>=2.32.3",
        "tqdm>=4.66.4",
        "numpy>=1.26.4",
    ],
    author="Dr. Shaun Thomas Edward Donnelly",
    author_email="shaun.t.e.donnelly@gmail.com",
    description="A utility for calling and using a basis set from ccrepo",
    url="https://github.com/stedonnelly/ccrepo_utility",
    license="MIT License (Non-Commercial)",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
