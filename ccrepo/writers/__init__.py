# __init__.py
import os
import importlib
from .writers import write_basis, convert_to_format, SUPPORTED_FORMATS, register_format, supported_writers

# Get the directory of this file
package_dir = os.path.dirname(__file__)

# Iterate over the files in the package directory
for filename in os.listdir(package_dir):
    # Check for Python files (excluding __init__.py itself)
    if filename.endswith(".py") and filename != "__init__.py" and filename != "writers.py":
        module_name = filename[:-3]  # Strip the ".py" extension
        # Import the module using importlib
        importlib.import_module(f".{module_name}", package=__name__)
