import argparse
import asyncio
import inspect
import logging
import sys

from .. import __version__
from . import cmd
from . import listen
from . import ls
from . import observe
from . import read
from . import write


def argvhandler(argv):
    """Command Line Interface."""
    parser = argparse.ArgumentParser(prog="ebustool")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--debug", action="store_true", default=False)
    parser.set_defaults(main=lambda args: _print_help(parser))

    # Sub Commands
    subparsers = parser.add_subparsers(help="Sub Commands")
    cmd.parse_args(subparsers)
    listen.parse_args(subparsers)
    ls.parse_args(subparsers)
    observe.parse_args(subparsers)
    read.parse_args(subparsers)
    write.parse_args(subparsers)

    args = parser.parse_args(argv)
    loglevel = logging.DEBUG if args.debug else logging.WARN
    logging.basicConfig(format="%(levelname)10s %(name)15s %(message)s", level=loglevel)
    if inspect.iscoroutinefunction(args.main):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(args.main(args))
        loop.close()
    else:
        args.main(args)


def _print_help(parser):
    parser.print_help()
    sys.exit(2)


def main():  # pragma: no cover
    """Command Line Hookup."""
    try:
        argvhandler(sys.argv[1:])
    except (RuntimeError, ValueError) as e:
        print("ERROR: %r" % e)
        sys.exit(1)
