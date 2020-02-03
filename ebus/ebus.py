import asyncio
import logging

from .connection import CommandError
from .connection import Connection
from .msgdecoder import MsgDecoder
from .msgdefdecoder import decode_msgdef
from .msgdefs import MsgDefs
from .util import repr_

_LOGGER = logging.getLogger(__name__)


class Ebus:
    def __init__(self, host, port, scanwaitinterval=3):
        """
        Pythonic EBUS Representation.

        This instance connects to an EBUSD instance and allows to read, write or monitor.
        """
        self.connection = Connection(host=host, port=port, autoconnect=True)
        self.scanwaitinterval = scanwaitinterval
        self.msgdefs = MsgDefs()
        self.msgdecoder = MsgDecoder(self.msgdefs)

    def __repr__(self):
        return repr_(self, args=(self.connection.host, self.connection.port))

    async def wait_scancompleted(self):
        """Wait until scan is completed."""
        cnts = []
        while True:
            cnt = sum([1 async for line in self.request("find -a -F type,circuit,name,fields")])
            cnts.append(cnt)
            if len(cnts) < 3 or cnts[-4] != cnts[-3] or cnts[-3] != cnts[-2] or cnts[-2] != cnts[-1]:
                yield cnt
            else:
                break
            await asyncio.sleep(self.scanwaitinterval)

    async def load_msgdefs(self):
        """
        Load Message Definitions from EBUSD.

        Keyword Args:
            scanwait (bool): Wait for EBUSD scan to complete
        """
        self.msgdefs.clear()
        async for line in self.request("find -a -F type,circuit,name,fields"):
            if line:
                try:
                    msgdef = decode_msgdef(line)
                    if not msgdef.circuit.startswith("scan"):
                        self.msgdefs.add(msgdef)
                except ValueError as e:
                    _LOGGER.warn(f"Cannot decode message definition ({e})")

    async def read(self, msgdef):
        """
        Read Message.

        Raises:
            ValueError: on decoder error
        """
        cmd = f"read -c {msgdef.circuit} {msgdef.name}"
        lines = tuple([line async for line in self.request(cmd)])
        return self.msgdecoder.decode_value(msgdef, lines[0])

    async def readall(self):
        """Read all Messages."""
        for msgdef in self.msgdefs:
            if not msgdef.read:
                continue
            try:
                yield await self.read(msgdef)
            except CommandError as e:
                _LOGGER.warn(f"{msgdef}: {e!r}")

    async def listen(self):
        """Listen."""
        decode_line = self.msgdecoder.decode_line
        async for line in self.request("listen", infinite=True):
            if line and line != "listen started":
                yield decode_line(line)

    async def request(self, *args, infinite=False, **kwargs):
        """Assemble request, send and readlines."""
        args = [str(arg) for arg in args]
        args += [f"{option} {value}" for option, value in kwargs.items() if value is not None]
        cmd = " ".join(args)
        await self.connection.write(cmd)
        async for line in self.connection.readlines(infinite=infinite):
            yield line

    async def cmd(self, cmd, infinite=False):
        """Send `cmd` to EBUSD and Receive Response."""
        await self.connection.write(cmd)
        async for line in self.connection.readlines(infinite=infinite):
            yield line
