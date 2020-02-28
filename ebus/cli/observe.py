from .common import add_ebus_args
from .common import add_msgdef_args
from .common import add_patterns_arg
from .common import add_read_args
from .common import create_ebus
from .common import disable_stdout_buffering
from .common import load_msgdefs
from .common import print_msg


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
    add_patterns_arg(parser, opt=True)
    parser.set_defaults(main=_main)


async def _main(args):
    disable_stdout_buffering()
    e = create_ebus(args)
    await load_msgdefs(e, args)
    msgdefs = e.msgdefs.resolve(args.patterns.split(";"))
    print(f"Observing {msgdefs.summary()}")
    async for msg in e.observe(msgdefs=msgdefs, prio=args.prio, ttl=args.ttl):
        print_msg(msg)
