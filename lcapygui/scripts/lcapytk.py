#!/usr/bin/env python3
"""lcapy-tk V0.94dev
Copyright (c) 2023 Michael P. Hayes, UC ECE, NZ

Usage: lcapy-tk [infile.sch]
"""

from argparse import ArgumentParser
import sys
from lcapygui import LcapyTk
from lcapy import expr as lcapify
from platform import system


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

def create_shortcut():
    import os
    import sys
    from pyshortcuts import make_shortcut, platform


    package_name = 'lcapy-gui'  # Name to use for the shortcut
    integrate = True  # Whether to integrate the shortcut with the Start Menu/application launcher (not compatible on MacOS)

    # Pick the best icon for the platform
    icon_path = None
    from lcapygui import __datadir__
    if platform == 'win':
        icon_path = __datadir__ / "icon" / "lcapy-gui.ico"
    elif platform == 'linux':
        icon_path = __datadir__ / "icon" / "lcapy-gui.svg"
    elif platform == 'Darwin':
        integrate = False

    # Pick the best executable for the platform
    bindir = 'Scripts' if platform.startswith('win') else 'bin'
    executable_path = os.path.normpath(os.path.join(sys.prefix, bindir, "lcapy-tk"))

    # Pick the best python for the installation
    python_path = os.path.normpath(os.path.join(sys.prefix, bindir, "python"))

    # Create the shortcut
    launch_lcapygui = make_shortcut(f"{executable_path:s}", name=package_name, icon=icon_path, startmenu=integrate, terminal=False, folder=package_name, executable=python_path)

    print(f"Shortcut created in: {launch_lcapygui.startmenu_dir}")

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
    parser.add_argument('--create-shortcut', action='store_true',
                        help='Create a system shortcut', default=False)
    parser.add_argument('filenames', type=str, nargs='*',
                        help='schematic filename(s)', default=[])

    args = parser.parse_args()

    # Create shortcut if requested, instead of launching lcapy-gui
    if args.create_shortcut:
        create_shortcut()
        return 0

    # Add Icon path for program
    from lcapygui import __datadir__
    icon_filename = __datadir__ / "icon" / "lcapy-gui-small.png"

    # If on MacOS, don't use icon
    if system() == 'Darwin':
        icon_filename = None

    if args.pdb:
        sys.excepthook = schtex_exception

    e = LcapyTk(
        args.filenames, debug=args.debug, level=args.level, icon=icon_filename
    )

    if args.expr is not None:
        dialog = e.show_expr_dialog(lcapify(args.expr))
        dialog.topmost()

    e.display()

    return 0


if __name__ == "__main__":
    sys.exit(main())
