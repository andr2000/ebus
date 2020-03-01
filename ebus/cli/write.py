from .common import add_msgdef_args
from .common import create_ebus
from .common import disable_stdout_buffering
from .common import load_msgdefs


def parse_args(subparsers):
    """Parse Arguments."""
    parser = subparsers.add_parser("write", help="Write value to the bus")
    add_msgdef_args(parser)
    parser.add_argument("field", help="Field (i.e. 'ui/OutsideTemp/temp')")
    parser.add_argument("value", help="Value to apply (i.e. '5'). 'NONE' is reserved for no value.")
    parser.set_defaults(main=_main)


async def _main(args):
    disable_stdout_buffering()
    e = create_ebus(args)
    await load_msgdefs(e, args)
    for msgdef in e.msgdefs.resolve([args.field]):
        value = args.value if args.value != "NONE" else None
        await e.write(msgdef, value)
