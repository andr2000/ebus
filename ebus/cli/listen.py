import asyncio

import ebus

from .common import add_connection_args


def parse_args(subparsers):
    """Parse Arguments."""
    parser = subparsers.add_parser("listen", help="Listen on the bus")
    add_connection_args(parser)

    # parser.add_argument(
    #     "--all", default=False, action="store_true", help="Listen to all message, set EBUSD polling priority to 9"
    # )
    parser.set_defaults(main=main)


async def _main(args):
    e = ebus.Ebus(host=args.host, port=args.port)
    await e.load_msgdefs()
    m = len(e.msgdefs)
    print(f"{m} message definitions found.")
    async for line in e.listen():
        print(line)


def main(args):
    """Listen."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(args))
    loop.close()
