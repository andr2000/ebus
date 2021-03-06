import asyncio

from .common import add_ebus_args
from .common import add_msgdef_args
from .common import add_patterns_arg
from .common import create_ebus
from .common import disable_stdout_buffering
from .common import format_field
from .common import load_msgdefs


def parse_args(subparsers):
    """Parse Arguments."""
    parser = subparsers.add_parser("listen", help="Listen on the bus, decode messages and and print")
    add_ebus_args(parser)
    add_msgdef_args(parser)
    add_patterns_arg(parser, opt=True)
    parser.set_defaults(main=_main)


async def _main(args):
    disable_stdout_buffering()
    e = create_ebus(args)
    await load_msgdefs(e, args)
    msgdefs = e.msgdefs.resolve(args.patterns.split(";"))
    print(f"Listening to {msgdefs.summary()}")
    if msgdefs:
        async for msg in e.listen(msgdefs=msgdefs):
            for field in msg.fields:
                print(format_field(field))
