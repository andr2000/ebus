import logging

from .connection import Connection
from .msgdecoder import MsgDecoder
from .msgdefdecoder import decode_msgdef
from .msgdefs import MsgDefs
from .util import repr_

_LOGGER = logging.getLogger(__name__)


class Ebus:
    def __init__(self, host, port):
        """
        Pythonic EBUS Representation.

        This instance connects to an EBUSD instance and allows to read, write or monitor.
        """
        self.connection = Connection(host=host, port=port, autoconnect=True)
        self.msgdefs = MsgDefs()
        self.msgdecoder = MsgDecoder(self.msgdefs)

    def __repr__(self):
        return repr_(self, args=(self.connection.host, self.connection.port))

    async def load_msgdefs(self):
        """Load Message Definitions from EBUSD."""
        self.msgdefs.clear()
        async for line in self.request("find -a -F type,circuit,name,fields"):
            if line:
                try:
                    self.msgdefs.add(decode_msgdef(line))
                except ValueError as e:
                    _LOGGER.warn(f"Cannot decode Message Definition ({e})")

    async def listen(self):
        """Listen."""
        decode = self.msgdecoder.decode
        async for line in self.request("listen", infinite=True):
            if line and line != "listen started":
                try:
                    yield decode(line)
                except ValueError as e:
                    _LOGGER.warn(f"Cannot decode Message ({e})")

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
        connection = self.connection
        await connection.write(cmd)
        async for line in connection.readlines(infinite=infinite):
            yield line
