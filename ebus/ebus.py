import asyncio
import collections
import logging

from .connection import CommandError
from .connection import Connection
from .msg import Msg
from .msg import filter_msg
from .msgdecoder import MsgDecoder
from .msgdecoder import UnknownMsgError
from .msgdefdecoder import decode_msgdef
from .msgdefs import MsgDefs
from .util import repr_

_LOGGER = logging.getLogger(__name__)
_CMD_FINDMSGDEFS = "find -a -F type,circuit,name,fields"


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
            cnt = sum([1 async for line in self.request(_CMD_FINDMSGDEFS)])
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
        msgdefs = []
        async for line in self.request(_CMD_FINDMSGDEFS):
            if line:
                try:
                    msgdef = decode_msgdef(line)
                    if not msgdef.circuit.startswith("scan"):
                        msgdefs.append(msgdef)
                except ValueError as e:
                    _LOGGER.warn(f"Cannot decode message definition ({e})")
        for msgdef in sorted(msgdefs, key=lambda msgdef: (msgdef.circuit, msgdef.name)):
            self.msgdefs.add(msgdef)

    async def read(self, msgdef, prio=False, ttl=None):
        """
        Read Message.

        Raises:
            ValueError: on decoder error
        """
        p = msgdef.prio if prio else None
        try:
            lines = tuple([line async for line in self.request("read", msgdef.name, c=msgdef.circuit, p=p, m=ttl)])
        except CommandError as e:
            _LOGGER.warn(f"{msgdef.ident}: {e!r}")
        else:
            return self.msgdecoder.decode_value(msgdef, lines[0])

    async def write(self, msgdef, value, ttl=None):
        """Write Message."""
        if not msgdef.write:
            raise ValueError(f"Message is not writeable '{msgdef}'")
        fullmsgdef = self.msgdefs.get(msgdef.circuit, msgdef.name)
        if fullmsgdef != msgdef:
            if not msgdef.read:
                raise ValueError(f"Message is not read-modify-writable '{msgdef}'")
            # read actual values
            readline = tuple([line async for line in self.request("read", msgdef.name, c=msgdef.circuit, m=ttl)])[0]
            values = readline.split(";")
            for fielddef in msgdef.fields:
                values[fielddef.idx] = value
            value = ";".join(values)
        async for line in self.request("write", msgdef.name, value, c=msgdef.circuit, check=True):
            pass

    async def listen(self, msgdefs=None):
        """Listen to EBUSD, decode and yield."""
        async for line in self.request("listen", infinite=True):
            if line == "listen started":
                continue
            msg = self._decode_line(line)
            if msg is not None and msgdefs is not None:
                msg = filter_msg(msg, msgdefs)
            if msg:
                yield msg

    async def observe(self, msgdefs=None, prio=False, ttl=None):
        """
        Observe.

        Read all known messages.
        Use `find` to get the latest data, if me missed any updates in the
        meantime and start listening
        """
        msgdefs = msgdefs or self.msgdefs
        data = collections.defaultdict(lambda: None)

        # read all
        for msgdef in msgdefs:
            if msgdef.read:
                msg = await self.read(msgdef, prio=prio, ttl=ttl)
                if msg:
                    msg = filter_msg(msg, msgdefs)
                if msg:
                    yield msg
                    data[msgdef] = msg
            elif msgdef.update:
                data[msgdef] = None

        # find new values (which got updated while we where reading)
        async for line in self.request("find -d"):
            msg = self._decode_line(line)
            if msg:
                msg = filter_msg(msg, msgdefs)
            if msg and msg != data[msg.msgdef]:
                yield msg
                data[msg.msgdef] = msg

        # listen
        async for msg in self.listen(msgdefs=msgdefs):
            yield msg

    async def request(self, cmd, *args, infinite=False, check=False, **kwargs):
        """Assemble request, send and readlines."""
        parts = [cmd]
        parts += [f"-{option} {value}" for option, value in kwargs.items() if value is not None]
        parts += [str(arg) for arg in args]
        await self.connection.write(" ".join(parts))
        async for line in self.connection.readlines(infinite=infinite, check=check):
            yield line

    async def cmd(self, cmd, infinite=False, check=False):
        """Send `cmd` to EBUSD and Receive Response."""
        await self.connection.write(cmd)
        async for line in self.connection.readlines(infinite=infinite, check=check):
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
