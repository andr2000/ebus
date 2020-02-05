import asyncio
import collections
import logging

from .connection import CommandError
from .connection import Connection
from .const import CMD_FINDMSGDEFS
from .msgdecoder import MsgDecoder
from .msgdecoder import UnknownMsgError
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
        return repr_(
            self,
            args=(self.connection.host, self.connection.port),
            kwargs=(("scanwaitinterval", self.scanwaitinterval, 3),),
        )

    @property
    def host(self):
        """Host Name or IP."""
        return self.connection.host

    @property
    def port(self):
        """Port."""
        return self.connection.port

    async def wait_scancompleted(self):
        """Wait until scan is completed."""
        cnts = []
        while True:
            cnt = sum([1 async for line in self.request(CMD_FINDMSGDEFS)])
            cnts.append(cnt)
            if len(cnts) < 4 or cnts[-4] != cnts[-3] or cnts[-3] != cnts[-2] or cnts[-2] != cnts[-1]:
                yield cnt
                await asyncio.sleep(self.scanwaitinterval)
            else:
                break

    async def load_msgdefs(self):
        """
        Load Message Definitions from EBUSD.

        Keyword Args:
            scanwait (bool): Wait for EBUSD scan to complete
        """
        self.msgdefs.clear()
        async for line in self.request(CMD_FINDMSGDEFS):
            if line:
                try:
                    msgdef = decode_msgdef(line)
                    if not msgdef.circuit.startswith("scan"):
                        self.msgdefs.add(msgdef)
                except ValueError as e:
                    _LOGGER.warn(f"Cannot decode message definition ({e})")

    async def read(self, msgdef, prio=None, ttl=None):
        """
        Read Message.

        Raises:
            ValueError: on decoder error
        """
        if msgdef.read:
            try:
                lines = tuple(
                    [line async for line in self.request("read", msgdef.name, c=msgdef.circuit, p=prio, m=ttl)]
                )
            except CommandError as e:
                _LOGGER.warn(f"{e!r}: {msgdef}")
            else:
                return self.msgdecoder.decode_value(msgdef, lines[0])

    async def readall(self, prio=None, ttl=None):
        """Iterate over a all known messages, read from EBUSD, decode and yield."""
        for msgdef in self.msgdefs:
            if not msgdef.read:
                continue
            yield await self.read(msgdef, prio=prio, ttl=ttl)

    async def write(self, msgdef, value):
        """Write Message."""
        if not msgdef.write:
            raise ValueError(f"Message is not writeable '{msgdef}'")
        try:
            async for line in self.request("write", msgdef.name, value, c=msgdef.circuit):
                pass
        except CommandError as e:
            _LOGGER.warn(f"{e!r}: {msgdef}")

    async def listen(self):
        """Listen to EBUSD, decode and yield."""
        async for line in self.request("listen", infinite=True):
            if line == "listen started":
                continue
            msg = self._decode_line(line)
            if msg:
                yield msg

    async def observe(self, patterns=None, prio=None, ttl=None):
        """
        Observe.

        Read all known messages.
        Use `find` to get the latest data, if me missed any updates in the
        meantime and start listening
        """
        if patterns:
            msgdefs = [msgdef for msgdef, _ in self.msgdefs.resolve(patterns)]
        else:
            msgdefs = tuple(self.msgdefs)
        data = collections.defaultdict(lambda: None)

        # read all
        for msgdef in msgdefs:
            if not msgdef.read:
                continue
            msg = await self.read(msgdef, prio=prio, ttl=ttl)
            if msg:
                data[msgdef] = msg
                yield msg

        # find
        async for line in self.request("find -d"):
            msg = self._decode_line(line)
            if msg and msg in msgdefs:
                if msg != data[msg.msgdef]:
                    yield msg
                data[msg.msgdef] = msg

        # listen
        async for msg in self.listen():
            if msg and msg.msgdef in msgdefs:
                yield msg

    async def request(self, cmd, *args, infinite=False, **kwargs):
        """Assemble request, send and readlines."""
        parts = [cmd]
        parts += [f"-{option} {value}" for option, value in kwargs.items() if value is not None]
        parts += [str(arg) for arg in args]
        await self.connection.write(" ".join(parts))
        async for line in self.connection.readlines(infinite=infinite):
            yield line

    async def cmd(self, cmd, infinite=False):
        """Send `cmd` to EBUSD and Receive Response."""
        await self.connection.write(cmd)
        async for line in self.connection.readlines(infinite=infinite):
            yield line

    def _decode_line(self, line):
        if line:
            try:
                return self.msgdecoder.decode_line(line)
            except UnknownMsgError:
                return None
            except ValueError as e:
                _LOGGER.warn(f"Cannot decode message in {line!r}: {e}")
        else:
            return None
