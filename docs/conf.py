"""Configuration file for the Sphinx documentation build of mdpo."""

import os
import re
import subprocess
import sys


SPHINX_IS_RUNNING = 'sphinx' in sys.modules


# -- Path setup --------------------------------------------------------------
rootdir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, rootdir)

# -- Project information -----------------------------------------------------
pyproject_toml_path = os.path.join(rootdir, 'pyproject.toml')
with open(pyproject_toml_path, encoding='utf-8') as f:
    pyproject_lines = f.read().splitlines()

metadata = {'name': None, 'author': None, 'version': None}
for line in pyproject_lines:
    if line.startswith('name ='):
        metadata['name'] = line.split(' = ')[1].strip().strip('"').strip("'")
    elif line.startswith('version ='):
        metadata['version'] = line.split(
            ' = ',
        )[1].strip().strip('"').strip("'")
    elif line.startswith('authors ='):
        metadata['author'] = re.search("name = \"([^\"]+)\"", line).group(1)
    elif not line:
        break

license_path = os.path.join(rootdir, 'LICENSE')
with open(license_path, encoding='utf-8') as f:
    license_years_range = re.search(
        r'Copyright \(c\) (\d+-\d+)', f.read(),
    ).group(1)

project = metadata['name']
author = metadata['author']
project_copyright = f'{license_years_range}, {author}'
release = metadata['version']
version = '.'.join(release.split('.')[:2])

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosectionlabel',
    'sphinx_argparse_cli',
    'sphinx_github_changelog',
    'sphinx_tabs.tabs',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'venv', 'dist']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'logo_only': True,
    'style_nav_header_background': 'white',
}
html_logo = os.path.join(rootdir, 'mdpo.png')

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = [
    os.path.join('css', 'override-styles.css'),
]

# -- Options for `sphinx.ext.intersphinx` ------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'polib': ('https://polib.readthedocs.io/en/latest', None),
}

# -- Options for `sphinx.ext.autosectionlabel` -------------------------------

autosectionlabel_prefix_document = True

# --- sphinx-apidoc ---

if SPHINX_IS_RUNNING:
    subprocess.run(
        [
            'sphinx-apidoc',
            '-o',
            os.path.join(rootdir, 'docs/dev/reference'),
            '-H',
            'Reference',
            '-ePMf',
            os.path.join(rootdir, 'src/mdpo'),
        ],
        check=True,
    )

# ---------------------------------------------------------
