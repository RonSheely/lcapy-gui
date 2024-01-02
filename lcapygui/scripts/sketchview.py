#!/usr/bin/env python3
"""sketchview V0.0.1
Copyright (c) 2023 Michael P. Hayes, UC ECE, NZ

Usage: sketchview infile.svg
"""

from argparse import ArgumentParser
import sys
from lcapygui.components.sketch import Sketch
from lcapygui.components.tf import TF
from lcapygui.components.cpt_maker import cpt_make_from_sketch_key
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


def sketchview(sketch_key, pins, points):

    fig, ax = subplots(1)

    sketch = Sketch.load(sketch_key)
    sketcher = Sketcher(ax)

    tf = TF()

    # Convert from points to cm
    # tf = tf.scale(2.54 / 72)
    # Convert from points to circuitikz units
    if not points:
        tf = tf.scale(2.54 / 72 / 2)

    # Note, y values are negated
    sketcher.sketch(sketch, tf, color='blue', lw=3)

    ax.axis('equal')

    # ax.set_xlim(-sketch.width_units, sketch.width_units)

    ax.plot(0, 0, 'o')

    ax.grid(which='both', axis='both')

    print('width=%.2fpt (%.3fcm), height=%.2fpt (%.3fcm)' %
          (sketch.width, sketch.width_cm, sketch.height, sketch.height_cm))

    if pins:
        cpt = cpt_make_from_sketch_key(sketch_key)
        for pinname, pin in cpt.pins.items():
            x, y = pin[1], pin[2]
            sketcher.stroke_filled_circle(
                x, y, 0.02, color='purple', alpha=1)
            print(pinname, x, y)
            sketcher.text(x, y, pinname)


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
    parser.add_argument('--pins', action='store_true',
                        default=False,
                        help="show pins")
    parser.add_argument('--points', action='store_true',
                        default=False,
                        help="show pins")
    parser.add_argument('sketch_keys', type=str, nargs='*',
                        help='schematic sketch key(s)', default=[])

    args = parser.parse_args()

    if args.pdb:
        sys.excepthook = schtex_exception

    for sketch_key in args.sketch_keys:
        sketchview(sketch_key, args.pins, args.points)

    show()

    return 0


if __name__ == '__main__':
    sys.exit(main())
