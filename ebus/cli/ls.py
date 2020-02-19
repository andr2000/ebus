import asyncio

from ..typedecoder import get_pytype
from .common import add_ebus_args
from .common import add_msgdef_args
from .common import add_patterns_arg
from .common import create_ebus
from .common import disable_stdout_buffering
from .common import load_msgdefs


def parse_args(subparsers):
    """Parse Arguments."""
    parser = subparsers.add_parser("ls", help="List all messages")
    add_ebus_args(parser)
    add_msgdef_args(parser)
    add_patterns_arg(parser, opt=True)
    parser.set_defaults(main=main)


async def _main(args):
    disable_stdout_buffering()
    e = create_ebus(args)
    await load_msgdefs(e, args)
    for msgdef in e.msgdefs.resolve(args.patterns):
        for fielddef in msgdef.fields:
            values = fielddef.values
            if values:
                details = "/".join(fielddef.values.values())
            else:
                details = get_pytype(fielddef.types[0]) or ""
            if fielddef.comment:
                details += f"[{fielddef.comment}]"
            print(f"{fielddef.ident:<40s} {msgdef.type_} {details}")


def main(args):
    """Main."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(args))
    loop.close()
