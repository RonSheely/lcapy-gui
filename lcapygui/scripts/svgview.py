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
from matplotlib.path import Path


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


def svgview(filename, centre=False, scale=False):

    fig, ax = subplots(1)

    sketch = Sketch.load_file(filename)
    sketcher = Sketcher(ax)

    tf = TF()

    xmin = 1000
    ymin = 1000
    xmax = -1000
    ymax = -1000
    for m, spath in enumerate(sketch.paths):
        path = spath.path
        for v, c in zip(path.vertices, path.codes):
            if c in (Path.MOVETO, Path.LINETO):
                pos = v
                if pos[0] > xmax:
                    xmax = pos[0]
                if pos[0] < xmin:
                    xmin = pos[0]
                if pos[1] > ymax:
                    ymax = pos[1]
                if pos[1] < ymin:
                    ymin = pos[1]

    xoff = (xmin + xmax) / 2
    yoff = (ymin + ymax) / 2
    print(xmin, xmax, ymin, ymax, xoff, yoff)

    # Some components are asymmetrical and so need to look for wires
    xoff1, yoff1 = sketch.offsets_find()
    if xoff1 is not None:
        xoff, yoff = xoff1, yoff1
    else:
        print('Guessing offsets')

    tf = tf.translate(-xoff, yoff)

    if centre:
        tf = tf.translate(-sketch.width / 2, sketch.height / 2)
    if scale:
        # Convert from points to cm
        # tf = tf.scale(2.54 / 72)
        # Convert from points to circuitikz units
        tf = tf.scale(2.54 / 72 / 2)

    # Note, y values are negated
    sketcher.sketch(sketch, tf, color='blue')

    ax.axis('equal')

    if centre:
        ax.set_xlim(-sketch.width / 2, sketch.width / 2)
        ax.plot(0, 0, 'o')
    else:
        ax.set_xlim(xmin - xoff, xmax - xoff)

    ax.grid(which='both', axis='both')

    print('width=%s, height=%s' % (sketch.width, sketch.height))


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
    parser.add_argument('--scale', action='store_true',
                        default=False, help="scale")
    parser.add_argument('--centre', action='store_true',
                        default=False, help="centre")
    parser.add_argument('filenames', type=str, nargs='*',
                        help='schematic filename(s)', default=[])

    args = parser.parse_args()

    if args.pdb:
        sys.excepthook = schtex_exception

    for filename in args.filenames:
        svgview(filename, args.centre, args.scale)

    show()

    return 0


if __name__ == '__main__':
    sys.exit(main())
