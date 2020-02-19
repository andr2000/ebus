import asyncio
import logging

from .common import add_ebus_args
from .common import add_msgdef_args
from .common import add_patterns_arg
from .common import add_read_args
from .common import create_ebus
from .common import disable_stdout_buffering
from .common import load_msgdefs


def parse_args(subparsers):
    """Parse Arguments."""
    parser = subparsers.add_parser("read", help="Read values from the bus, decode and print")
    add_ebus_args(parser)
    add_msgdef_args(parser)
    add_read_args(parser, ttl=0)
    add_patterns_arg(parser, opt=True)
    parser.set_defaults(main=main)


async def _main(args):
    disable_stdout_buffering()
    e = create_ebus(args)
    await load_msgdefs(e, args)
    msgdefs = e.msgdefs.resolve(args.patterns, filter_=lambda msgdef: msgdef.read or msgdef.update)
    print(f"Reading to {msgdefs.get_info()}")
    for msgdef in msgdefs:
        if msgdef.read:
            msg = await e.read(msgdef, prio=args.prio, ttl=args.ttl)
            if msg:
                for field in msg.fields:
                    print(f"{field.fielddef.ident:<40s} {field.unitvalue}")


def main(args):
    """Main."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(args))
    loop.close()
