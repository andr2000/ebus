import asyncio

from nose.tools import assert_raises
from nose.tools import eq_

import ebus

from .util import DummyServer
from .util import run

UNUSED_PORT = 4445


def test_connection():
    """Connection Class Properties."""
    c = ebus.Connection()
    eq_(c.host, "127.0.0.1")
    eq_(c.port, 8888)
    eq_(c.autoconnect, False)

    c = ebus.Connection(host="foo", port=4444, autoconnect=True)
    eq_(c.host, "foo")
    eq_(c.port, 4444)
    eq_(c.autoconnect, True)


def test_connect_fails():
    """Connection failed."""
    c = ebus.Connection(port=UNUSED_PORT)

    async def test():
        eq_(c.is_connected(), False)
        with assert_raises(ConnectionRefusedError):
            await c.connect()
        eq_(c.is_connected(), False)

    run(test)


def test_connect():
    """Connection succeed."""
    s = DummyServer()
    c = ebus.Connection(port=s.port)

    async def test():
        await s.start()
        eq_(c.is_connected(), False)
        await c.connect()
        eq_(c.is_connected(), True)
        await c.disconnect()
        eq_(c.is_connected(), False)
        await c.disconnect()
        eq_(c.is_connected(), False)

    run(test, server=s)


def test_notconnected():
    """Not Connected."""
    # s = DummyServer()
    c = ebus.Connection(port=UNUSED_PORT)

    async def test():
        with assert_raises(ConnectionError):
            await c.write("rx0\n")

    run(test)


def test_read_write():
    """Read Write Through Connection."""
    s = DummyServer()
    c = ebus.Connection(port=s.port, autoconnect=True)

    s.add_rx("rx0\n")
    s.add_tx("tx0\n")

    async def test():
        await s.start()
        await c.write("rx0\n")
        line = await c.readline()
        eq_(line, "tx0")
        await asyncio.sleep(0.001)

    run(test, server=s)


def test_readlines():
    """Read Multiple lines."""
    s = DummyServer()
    c = ebus.Connection(port=s.port, autoconnect=True)
    s.add_tx("tx0\ntx1\ntx2\n\n")

    async def test():
        await s.start()
        await c.write("rx0\n")
        lines = tuple([line async for line in c.readlines()])
        eq_(lines, ("tx0", "tx1", "tx2", ""))
        await asyncio.sleep(0.001)

    run(test, server=s)


def test_command_error():
    """Command Error."""
    s = DummyServer()
    c = ebus.Connection(port=s.port, autoconnect=True)

    s.add_tx("ERR: msg\n")
    s.add_tx("\n")

    async def test():
        await s.start()
        with assert_raises(ebus.CommandError):
            await c.readline()

    run(test, server=s)
