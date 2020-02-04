import asyncio

from ..typedecoder import get_pytype
from .common import add_ebus_args
from .common import add_msgdef_args
from .common import create_ebus
from .common import disable_stdout_buffering
from .common import load_msgdefs


def parse_args(subparsers):
    """Parse Arguments."""
    parser = subparsers.add_parser("ls", help="List all messages")
    add_ebus_args(parser)
    add_msgdef_args(parser)
    parser.set_defaults(main=main)


async def _main(args):
    disable_stdout_buffering()
    e = create_ebus(args)
    await load_msgdefs(e, args)
    for msgdef in e.msgdefs:
        for field in msgdef.fields:
            values = field.values
            if values:
                details = ";".join(field.values.values())
            else:
                details = get_pytype(field.types[0])
            print(f"{msgdef.type_:<2s} {msgdef}/{field.uname} {details}")


def main(args):
    """Main."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(args))
    loop.close()
