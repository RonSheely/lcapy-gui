"""
Root-level lcapy-gui objects.
These can be imported directly from lcapy-gui.
"""

from .ui.tk import LcapyTk
import sys

from importlib.metadata import version
__version__ = version('lcapygui')


if sys.version_info < (3, 9):
    import importlib_resources
else:
    import importlib.resources as importlib_resources

pkg = importlib_resources.files('lcapygui')
__datadir__ = pkg / 'data'
