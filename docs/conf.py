"""Sphinx configuration for Super State Machine documentation."""

import importlib.metadata

# -- Project information -----------------------------------------------------

project = "Super State Machine"
author = "Szczepan Cieślik"
copyright = "2014, Szczepan Cieślik"

release = importlib.metadata.version("super_state_machine")
version = ".".join(release.split(".")[:3])

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_mdinclude",
]

master_doc = "index"
exclude_patterns = ["_build"]
templates_path = ["_templates"]

autodoc_member_order = "bysource"

# Section labels are `document:Section title`, e.g. :ref:`usage:forced set`.
autosectionlabel_prefix_document = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"
html_title = f"Super State Machine {version}"
html_static_path = ["_static"]
html_theme_options = {
    "source_repository": "https://github.com/beregond/super_state_machine/",
    "source_branch": "master",
    "source_directory": "docs/",
}
