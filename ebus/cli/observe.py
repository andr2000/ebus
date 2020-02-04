import asyncio

from .common import add_ebus_args
from .common import add_msgdef_args
from .common import add_read_args
from .common import create_ebus
from .common import disable_stdout_buffering
from .common import load_msgdefs


def parse_args(subparsers):
    """Parse Arguments."""
    parser = subparsers.add_parser(
        "observe",
        help=(
            "Read all known messages once and continue listening so that ALL EBUS values are available, "
            "decode every message and print."
        ),
    )
    add_ebus_args(parser)
    add_msgdef_args(parser)
    add_read_args(parser)
    parser.set_defaults(main=main)


async def _main(args):
    disable_stdout_buffering()
    e = create_ebus(args)
    await load_msgdefs(e, args)
    async for msg in e.observe(prio=args.prio, ttl=args.ttl):
        for field in msg.fields:
            print(field)


def main(args):
    """Main."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(args))
    loop.close()
