from .common import add_msgdef_args
from .common import add_patterns_arg
from .common import add_read_args
from .common import create_ebus
from .common import disable_stdout_buffering
from .common import load_msgdefs
from .common import print_msg


def parse_args(subparsers):
    """Parse Arguments."""
    parser = subparsers.add_parser("read", help="Read values from the bus, decode and print")
    add_msgdef_args(parser)
    add_read_args(parser, ttl=0)
    add_patterns_arg(parser, opt=True)
    parser.set_defaults(main=_main)


async def _main(args):
    disable_stdout_buffering()
    e = create_ebus(args)
    await load_msgdefs(e, args)
    msgdefs = e.msgdefs.resolve(args.patterns.split(";"), filter_=lambda msgdef: msgdef.read or msgdef.update)
    print(f"Reading to {msgdefs.summary()}")
    for msgdef in msgdefs:
        if msgdef.read:
            msg = await e.read(msgdef, prio=args.prio, ttl=args.ttl)
            print_msg(msg)
