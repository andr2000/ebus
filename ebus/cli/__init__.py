import argparse

from .. import __version__
from . import cmd
from . import listen


def main():
    """Command Line Interface."""
    parser = argparse.ArgumentParser(prog="Ebus Tool")
    parser.add_argument("--version", action="version", version=__version__)

    # Sub Commands
    subparsers = parser.add_subparsers(help="Sub Commands")
    cmd.parse_args(subparsers)
    listen.parse_args(subparsers)

    args = parser.parse_args()
    args.main(args)
