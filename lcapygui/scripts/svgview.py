#!/usr/bin/env python3
"""svgview V0.0.1
Copyright (c) 2023 Michael P. Hayes, UC ECE, NZ

Usage: svgview infile.svg
"""

from argparse import ArgumentParser
import sys
from lcapygui.components.sketch import Sketch
from lcapygui.components.tf import TF
from lcapygui.ui.tk.sketcher import Sketcher
from matplotlib.pyplot import subplots, show


def schtex_exception(type, value, tb):
    if hasattr(sys, 'ps1') or not sys.stderr.isatty():
        # We are not in interactive mode or we don't have a tty-like
        # device, so call the default hook
        sys.__excepthook__(type, value, tb)
    else:
        import traceback
        import pdb
        # We are in interactive mode, print the exception...
        traceback.print_exception(type, value, tb)
        print()
        # ...then start the debugger in post-mortem mode.
        pdb.pm()


def svgview(filename):

    fig, ax = subplots(1)

    sketch = Sketch.load_file(filename)
    sketcher = Sketcher(ax)

    tf = TF()
    sketcher.sketch(sketch, tf, color='blue')

    ax.set_xlim(-sketch.width, sketch.width)
    ax.set_ylim(-sketch.height, sketch.height)
    ax.axis('equal')

    ax.grid(which='both', axis='both')


def main(argv=None):

    if argv is None:
        argv = sys.argv

    parser = ArgumentParser(
        description='Generate lcapy netlists.')
    parser.add_argument('--version', action='version',
                        version=__doc__.split('\n')[0])
    parser.add_argument('--pdb', action='store_true',
                        default=False,
                        help="enter python debugger on exception")
    parser.add_argument('filenames', type=str, nargs='*',
                        help='schematic filename(s)', default=[])

    args = parser.parse_args()

    if args.pdb:
        sys.excepthook = schtex_exception

    for filename in args.filenames:
        svgview(filename)

    show()

    return 0


if __name__ == '__main__':
    sys.exit(main())
