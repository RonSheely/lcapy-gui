"""
Root-level lcapy-gui objects.
These can be imported directly from lcapy-gui.
"""

from .ui.tk import LcapyTk
import sys
import pkg_resources

if sys.version_info < (3, 9):
    import importlib_resources
else:
    import importlib.resources as importlib_resources

__version__ = pkg_resources.require('lcapy-gui')[0].version

pkg = importlib_resources.files('lcapy-gui')
__datadir__ = pkg / 'data'
