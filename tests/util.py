import asyncio
import collections
import filecmp
import os
import shutil

from nose.tools import eq_

_LEARN = False


def cmp_(out, ref):
    """Compare files."""
    if _LEARN:
        shutil.copyfile(out, ref)
    else:
        assert filecmp.cmp(out, ref), out
    os.remove(out)


class DummyServer:

    LOCALHOST = "127.0.0.1"
    _port = 12345

    @classmethod
    def _get_port(cls):
        port = cls._port
        cls._port += 1
        return port

    def __init__(self):
        self.queue = collections.deque()
        self.server = None
        self.port = DummyServer._get_port()

    def add_rx(self, line):
        self.queue.append((False, line))

    def add_tx(self, line):
        self.queue.append((True, line))

    async def start(self):
        async def _server():
            server = await asyncio.start_server(self, DummyServer.LOCALHOST, self.port)
            await server.serve_forever()

        self.server = asyncio.ensure_future(_server())
        await asyncio.sleep(0.001)

    async def __call__(self, reader, writer):
        print(f"DummyServer: started at port {self.port}")
        while self.queue:
            tx, line = self.queue.popleft()
            if tx:
                print(f"DummyServer: send {line}")
                writer.write(f"{line}".encode("utf-8"))
                await writer.drain()
            else:
                print(f"DummyServer: expect {line}")
                rxline = await reader.readline()
                rxline = rxline.decode("utf-8")
                print(f"DummyServer: got {rxline}")
                eq_(rxline, line)
        writer.close()
        print("DummyServer: closed")

    async def terminate(self):
        await asyncio.sleep(0.001)
        eq_(self.queue, collections.deque())
        self.server.cancel()


def run(coroutine, server=None):
    """Run `coroutine`."""

    async def _run():
        await coroutine()
        if server:
            await server.terminate()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(coroutine())
