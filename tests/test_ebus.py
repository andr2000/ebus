import asyncio

from nose.tools import eq_

import ebus

from .util import DummyServer
from .util import run


def test_defaults():
    """Defaults."""
    e = ebus.Ebus("host", 4444)
    eq_(e.host, "host")
    eq_(e.port, 4444)
    eq_(e.scanwaitinterval, 3)

    eq_(repr(e), "Ebus('host', 4444)")


def test_params():
    """Params."""
    e = ebus.Ebus("host1", 4445, scanwaitinterval=5)
    eq_(e.host, "host1")
    eq_(e.port, 4445)
    eq_(e.scanwaitinterval, 5)

    eq_(repr(e), "Ebus('host1', 4445, scanwaitinterval=5)")


def test_cmd():
    """Cmd."""
    s = DummyServer()

    async def test():
        await s.start()
        s.add_rx("read -c bai Status\n")
        s.add_tx("line0\n")
        s.add_tx("line1\n")

        e = ebus.Ebus(s.LOCALHOST, s.port)
        lines = tuple([line async for line in e.cmd("read -c bai Status\n")])
        eq_(lines, ("line0", "line1", ""))

    run(test, server=s)
