import asyncio

import ebus

from .common import add_connection_args


def parse_args(subparsers):
    """Parse Arguments."""
    parser = subparsers.add_parser("cmd", help="Issue Command on EBUSD")
    add_connection_args(parser)
    parser.add_argument(
        "--infinite", "-i", default=False, action="store_true", help="Do not abort command processing on empty line."
    )

    parser.add_argument("cmd", help="Command")
    parser.set_defaults(main=main)


async def _main(args):
    e = ebus.Ebus(host=args.host, port=args.port)
    async for line in e.cmd(args.cmd, infinite=args.infinite):
        print(line)


def main(args):
    """Listen."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(args))
    loop.close()
