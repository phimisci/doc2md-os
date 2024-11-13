# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'DOC2MD'
copyright = '2024, Thomas Jurczyk'
author = 'Thomas Jurczyk'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',        # For generating documentation from docstrings
    'sphinx.ext.napoleon',       # For Google and NumPy style docstrings
    'sphinx.ext.viewcode',       # Adds links to highlighted source code
    'sphinx.ext.autosummary',    # For generating summary tables]
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Other options
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
