from nose.tools import eq_, assert_raises
import asyncio
from ebus import Connection
from tests.util import run, DummyServer


def test_connection():
    """Connection Class Properties."""
    c = Connection()
    eq_(c.host, '127.0.0.1')
    eq_(c.port, 8888)
    eq_(c.autoconnect, False)

    c = Connection(host='foo', port=DummyServer.PORT, autoconnect=True)
    eq_(c.host, 'foo')
    eq_(c.port, DummyServer.PORT)
    eq_(c.autoconnect, True)


def test_connect_fails():
    """Connection failed."""
    c = Connection(port=DummyServer.PORT)

    async def test():
        eq_(c.is_connected(), False)
        with assert_raises(ConnectionRefusedError):
            await c.connect()
        eq_(c.is_connected(), False)
    run(test)


def test_connect():
    """Connection succeed."""
    s = DummyServer()
    c = Connection(port=DummyServer.PORT)

    async def test():
        await s.start()
        eq_(c.is_connected(), False)
        await c.connect()
        eq_(c.is_connected(), True)
        await c.disconnect()
        eq_(c.is_connected(), False)
        await c.disconnect()
        eq_(c.is_connected(), False)
    run(test)
    s.kill()


# def test_read_write():
#     """Read Write Through Connection."""
#     s = DummyServer()
#     c = Connection(port=DummyServer.PORT, autoconnect=True)

#     async def test():
#         await s.start()
#         s.add_tx('tx0')
#         s.add_rx('rx0')
#         await asyncio.sleep(.001)
#         await c.write('foo')
#         # eq_((await c.readline()), 'rx0')
#     run(test)
#     s.kill()
#     assert False
