# docs/conf.py
"""Sphinx configuration."""
from datetime import datetime


author = "Austin Kenny"
project = "My Python Setup"
copyright = f"{datetime.now().year}, {author}"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx_autodoc_typehints"]
