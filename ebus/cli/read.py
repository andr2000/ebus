import asyncio

from .common import add_ebus_args
from .common import add_msgdef_args
from .common import add_patterns_arg
from .common import add_read_args
from .common import create_ebus
from .common import disable_stdout_buffering
from .common import load_msgdefs


def parse_args(subparsers):
    """Parse Arguments."""
    parser = subparsers.add_parser("read", help="Read value from the bus, decode and print")
    add_ebus_args(parser)
    add_msgdef_args(parser)
    add_read_args(parser, ttl=0)
    add_patterns_arg(parser)
    parser.set_defaults(main=main)


async def _main(args):
    disable_stdout_buffering()
    e = create_ebus(args)
    await load_msgdefs(e, args)
    for msgdef, fielddef in e.msgdefs.resolve(args.patterns):
        msg = await e.read(msgdef, prio=args.prio, ttl=args.ttl)
        if msg:
            for field in msg.fields:
                if fielddef is None or fielddef is field.fielddef:
                    print(field)


def main(args):
    """Main."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(args))
    loop.close()