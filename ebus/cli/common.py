import sys

import ebus


def add_ebus_args(parser):
    """Load arguments related to :any:`create_ebus`."""
    parser.add_argument("--host", "-H", default="127.0.0.1", help="EBUSD address. Default is '172.0.0.1'.")
    parser.add_argument("--port", "-P", default=8888, type=int, help="EBUSD port. Default is 8888.")


def add_msgdef_args(parser):
    """Load arguments related to :any:`load_msgdef`."""
    parser.add_argument(
        "--scanwait",
        "-w",
        default=False,
        action="store_true",
        help=(
            "EBUSD scans the bus for available devices. "
            "Wait until this scan does not find any new messages. "
            "Specify this option, if EBUSD was started within the last minutes."
        ),
    )


def add_read_args(parser, ttl=None):
    """Read Arguments."""
    parser.add_argument("--prio", "-p", default=False, action="store_true", help="Set poll priority")
    parser.add_argument("--ttl", "-t", default=ttl, type=int, help="Maximum age of value in seconds")


def add_patterns_arg(parser, opt=False):
    """Add patterns option."""
    if not opt:
        parser.add_argument("patterns", help="Message patterns separated by ';' (i.e. 'ui/OutsideTemp')")
    else:
        parser.add_argument(
            "patterns",
            nargs="?",
            default="*/*",
            help="Message patterns separated by ';' (i.e. 'ui/OutsideTemp'). Default is '*/*' for all.",
        )


def disable_stdout_buffering():
    """Disable STDOUT buffering."""
    sys.stdout = ebus.util.UnbufferedStream(sys.stdout)


def create_ebus(args):
    """Create :any:`Ebus` instance with parameters from `args`."""
    return ebus.Ebus(host=args.host, port=args.port)


async def load_msgdefs(e, args):
    """Load Message Definitions."""
    if args.scanwait:
        print("Waiting for EBUSD scan to complete ", end="")
        async for line in e.wait_scancompleted():
            print(".", end="")
        print(" DONE.")

    print("Loading Message Definitions ... ", end="")
    await e.load_msgdefs()
    print(f"{e.msgdefs.get_info()} DONE.")


def format_field(field):
    """Format Field Value."""
    comment = field.fielddef.comment
    details = f" [{comment}]" if comment else ""
    return f"{field.ident:<40s} {field.unitvalue}{details}"
