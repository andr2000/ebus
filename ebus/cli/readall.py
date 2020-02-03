import asyncio

from .common import add_ebus_args
from .common import add_msgdef_args
from .common import create_ebus
from .common import disable_stdout_buffering
from .common import load_msgdefs


def parse_args(subparsers):
    """Parse Arguments."""
    parser = subparsers.add_parser("readall", help="Read all known messages.")
    add_ebus_args(parser)
    add_msgdef_args(parser)
    parser.set_defaults(main=main)


async def _main(args):
    disable_stdout_buffering()
    e = create_ebus(args)
    await load_msgdefs(e, args)
    async for line in e.readall():
        print(line)


def main(args):
    """Main."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(args))
    loop.close()
