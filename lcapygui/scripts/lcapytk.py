#!/usr/bin/env python3
"""lcapy-tk V0.0.3
Copyright (c) 2023 Michael P. Hayes, UC ECE, NZ

Usage: lcapy-tk [infile.sch]
"""

from argparse import ArgumentParser
import sys
from lcapygui import LcapyTk
from lcapy import expr as lcapify


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
    parser.add_argument('--debug', type=int, default=None,
                        help="enable debugging")
    parser.add_argument('--level', type=int, default=10,
                        help="sophistication level")
    parser.add_argument('--expr', type=str, default=None,
                        help="Lcapy expression")
    parser.add_argument('--model', type=str,
                        dest='model', default="UIModelMPH",
                        help="select the UI model: UIModelMPH, UIModelDnD")
    parser.add_argument('filenames', type=str, nargs='*',
                        help='schematic filename(s)', default=[])

    args = parser.parse_args()

    icon_filename = "./lcapygui/data/icon/lcapy-gui.png"

    if args.pdb:
        sys.excepthook = schtex_exception

    e = LcapyTk(
        args.filenames, debug=args.debug, level=args.level, uimodel_class=args.model, icon=icon_filename
    )

    if args.expr is not None:
        dialog = e.show_expr_dialog(lcapify(args.expr))
        dialog.topmost()

    e.display()

    return 0


if __name__ == "__main__":
    sys.exit(main())
