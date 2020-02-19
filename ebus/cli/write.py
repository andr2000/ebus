import asyncio

from .common import add_ebus_args
from .common import add_msgdef_args
from .common import create_ebus
from .common import disable_stdout_buffering
from .common import load_msgdefs


def parse_args(subparsers):
    """Parse Arguments."""
    parser = subparsers.add_parser("write", help="Write value to the bus")
    add_ebus_args(parser)
    add_msgdef_args(parser)
    parser.add_argument("field", help="Field (i.e. 'ui/OutsideTemp/temp')")
    parser.add_argument("value", help="Value (i.e. '5')")
    parser.set_defaults(main=main)


async def _main(args):
    disable_stdout_buffering()
    e = create_ebus(args)
    await load_msgdefs(e, args)
    for msgdef in e.msgdefs.resolve(args.field):
        await e.write(msgdef, args.value)


def main(args):
    """Main."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(args))
    loop.close()
