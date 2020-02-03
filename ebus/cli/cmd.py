import asyncio

import ebus

from .common import add_ebus_args
from .common import create_ebus


def parse_args(subparsers):
    """Parse Arguments."""
    parser = subparsers.add_parser("cmd", help="Issue Command on EBUSD")
    add_ebus_args(parser)
    parser.add_argument(
        "--infinite", "-i", default=False, action="store_true", help="Do not abort command processing on empty line."
    )

    parser.add_argument("cmd", help="Command")
    parser.set_defaults(main=main)


async def _main(args):
    e = create_ebus(args)
    async for line in e.cmd(args.cmd, infinite=args.infinite):
        print(line)


def main(args):
    """Main."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(args))
    loop.close()
