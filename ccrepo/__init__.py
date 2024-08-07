# ccrepo_basis_set/__init__.py

from .api import ccrepo_logger
from .data import availability
from .fetch import fetch_basis
from .utils import convert_to_ccrepo, convert_to_basisopt_internal
from .readers import read_basis_file
from .writers import write_basis

__author__ = "Dr. Shaun T E Donnelly, J. Dr. Grant Hill"
__author_email__ = "shaun.t.e.donnelly@gmail.com, grant.hill@sheffield.ac.uk"
__license__ = "MIT"
__url__ = "https://github.com/Sheffield-Theoretical-Chemistry/ccrepo_utility"
__description__ = "A utility for interfacing with the ccrepo database"
__version__ = "1.0.1b1"