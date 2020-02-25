import asyncio

from ..msgdefdecoder import decodetype
from ..typedecoder import get_typename
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
    parser.add_argument(
        "--name-only", "-n", default=False, action="store_true", help="Just print names.",
    )
    parser.add_argument(
        "--type", "-t", help="Type to be checked, 'r' for readable, 'w' for writeable.",
    )
    parser.set_defaults(main=_main)


async def _main(args):
    disable_stdout_buffering()
    e = create_ebus(args)
    await load_msgdefs(e, args)
    type_ = _parse_type(args.type)
    msgdefs = e.msgdefs.resolve(args.patterns.split(";"), filter_=lambda msgdef: _filter_type(msgdef, type_))
    print(f"Listing {msgdefs.summary()}")
    for msgdef in msgdefs:
        for fielddef in msgdef.children:
            values = fielddef.values
            if values:
                details = "/".join(fielddef.values.values())
            else:
                details = get_typename(fielddef.types[0]) or ""
            if fielddef.comment:
                details += f"[{fielddef.comment}]"
            if args.name_only:
                print(fielddef.ident)
            else:
                print(f"{fielddef.ident:<40s} {msgdef.type_} {details}")


def _parse_type(type_):
    if type_:
        read, _, write, update = decodetype(type_)
    else:
        read, write, update = None, None, None
    return read, write, update


def _filter_type(msgdef, type_):
    read, write, update = type_
    pairs = ((msgdef.read, read), (msgdef.write, write), (msgdef.update, update))
    return all([(exp is None or val == exp) for val, exp in pairs])
