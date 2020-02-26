from .common import add_ebus_args
from .common import create_ebus
from .common import disable_stdout_buffering


def parse_args(subparsers):
    """Parse Arguments."""
    parser = subparsers.add_parser("state", help="Show EBUSD state")
    add_ebus_args(parser)
    parser.set_defaults(main=_main)


async def _main(args):
    disable_stdout_buffering()
    e = create_ebus(args)
    print(await e.get_state())
