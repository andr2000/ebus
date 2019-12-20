import asyncio
import collections
import filecmp
import os
import shutil

from nose.tools import eq_

_LEARN = True


def cmp_(out, ref):
    """Compare files."""
    if _LEARN:
        shutil.copyfile(out, ref)
    else:
        assert filecmp.cmp(out, ref)
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


def run(coroutine):
    """Run `coroutine`."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(coroutine())
