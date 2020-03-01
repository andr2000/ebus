import sys

import ebus


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
    return ebus.Ebus(host=args.host, port=args.port, timeout=args.timeout)


async def load_msgdefs(e, args):
    """Load Message Definitions."""
    if args.scanwait:
        print("Waiting for EBUSD scan to complete ", end="")
        async for line in e.wait_scancompleted():
            print(".", end="")
        print(" DONE.")

    print("Loading Message Definitions ... ", end="")
    await e.load_msgdefs()
    print(f"{e.msgdefs.summary()} DONE.")


def print_msg(msg):
    """Formatted output."""
    if isinstance(msg, ebus.Msg):
        for field in msg.fields:
            comment = field.fielddef.comment
            details = f" [{comment}]" if comment else ""
            print(f"{field.ident:<40s} {field.fielddef.msgdef.type_} {field.unitvalue}{details}")
    else:
        print(f"{msg.msgdef.ident:<40s}      {msg.error}")
