import argparse
import sys

from .. import __version__
from . import cmd
from . import listen
from . import observe
from . import readall


def argvhandler(argv):
    """Command Line Interface."""
    parser = argparse.ArgumentParser(prog="Ebus Tool")
    parser.add_argument("--version", action="version", version=__version__)
    parser.set_defaults(main=lambda args: _print_help(parser))

    # Sub Commands
    subparsers = parser.add_subparsers(help="Sub Commands")
    cmd.parse_args(subparsers)
    listen.parse_args(subparsers)
    readall.parse_args(subparsers)
    observe.parse_args(subparsers)

    args = parser.parse_args(argv)
    args.main(args)


def _print_help(parser):
    parser.print_help()
    sys.exit(2)


def main():  # pragma: no cover
    """Command Line Hookup."""
    try:
        argvhandler(sys.argv[1:])
    except RuntimeError as e:
        print("ERROR: %r" % e)
        sys.exit(1)
