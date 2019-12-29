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


class DummyConnection:

    def __init__(self, rxlines=None, txlines=None):
        self.rxlines = collections.deque(rxlines or [])
        self.txlines = collections.deque(txlines or [])

    async def readlines(self):
        lines = []
        while True:
            line = self.rxlines.popleft()
            if line:
                lines.append(line)
            else:
                break
        await asyncio.sleep(0.001)  # dummy
        return lines

    async def readline(self):
        await asyncio.sleep(0.001)  # dummy
        return self.rxlines.popleft()

    async def write(self, line):
        await asyncio.sleep(0.001)  # dummy
        eq_(line, self.txlines.popleft())


class DummyServer:

    LOCALHOST = '127.0.0.1'
    PORT = 12344

    def __init__(self):
        self.queue = collections.deque()
        self.server = None

    def add_rx(self, line):
        self.queue.append((False, line))

    def add_tx(self, line):
        self.queue.append((True, line))

    async def start(self):
        async def _server():
            server = await asyncio.start_server(self, DummyServer.LOCALHOST, DummyServer.PORT)
            await server.serve_forever()
        self.server = asyncio.ensure_future(_server())
        await asyncio.sleep(.001)

    # async def __call__(self, reader, writer):
    #     while self.queue:
    #         tx, line = self.queue.popleft()
    #         print((tx, line))
    #         if tx:
    #             print("RX started")
    #             rxline = await reader.readline()
    #             print("RX", line, rxline)
    #             eq_(line, rxline.decode('utf-8'))
    #         else:
    #             print("TX", line)
    #             writer.write(f"{line}\n".encode('utf-8'))
    #             await writer.drain()
    #     writer.close()

    def kill(self):
        eq_(self.queue, collections.deque())
        self.server.cancel()


def run(coroutine):
    """Run `coroutine`."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(coroutine())
