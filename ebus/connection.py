import asyncio
import logging

from .util import repr_

_LOGGER = logging.getLogger(__name__)


class Connection:
    def __init__(self, host="127.0.0.1", port=8888, autoconnect=False, timeout=None):
        """
        Ebus Connection.

        Keyword Args:
            host (str): Hostname or IP
            port (int): Port
            autoconnect (bool): Automatically connect and re-connect
        """
        self._host = host
        self._port = port
        self._autoconnect = autoconnect
        self._timeout = timeout
        self._reader, self._writer = None, None

    def __repr__(self):
        return repr_(
            self,
            kwargs=(
                ("host", self.host, "127.0.0.1"),
                ("port", self.port, 8888),
                ("autoconnect", self.autoconnect, False),
                ("timeout", self.timeout, None),
            ),
        )

    @property
    def host(self):
        """Host."""
        return self._host

    @property
    def port(self):
        """Port."""
        return self._port

    @property
    def autoconnect(self):
        """Automatically connect and re-connect."""
        return self._autoconnect

    @property
    def timeout(self):
        """Connection Timeout."""
        return self._timeout

    async def connect(self):
        """
        Establish connection (required before first communication).

        Raises:
            IOError: If connection cannot be established
        """
        _LOGGER.debug(f"connect()")
        self._reader, self._writer = await self._timedout(asyncio.open_connection(self._host, self._port))

    async def disconnect(self):
        """Disconnect if not already done."""
        _LOGGER.debug(f"disconnect()")
        if self._writer:
            try:
                self._writer.close()
                await self._writer.wait_closed()
            except BrokenPipeError:  # pragma: no cover
                pass
            finally:
                self._reader, self._writer = None, None

    def is_connected(self):
        """
        Return `True` if connection is established.

        This does not check if the connection is still usable.
        """
        return self._writer is not None and not self._writer.is_closing()

    async def write(self, message):
        """
        Send `message`.

        Raises:
            IOError: If connection is broken or cannot be established (`autoconnect==True`)
            ConnectionError: If not connected (`autoconnect==False`)
        """
        _LOGGER.debug(f"write({message!r})")
        await self._ensure_connection()
        self._writer.write(f"{message}\n".encode())
        await self._timedout(self._writer.drain())

    async def readline(self):
        """
        Receive one line.

        Raises:
            IOError: If connection is broken or cannot be established (`autoconnect==True`)
            ConnectionError: If not connected (`autoconnect==False`)
        """
        await self._ensure_connection()
        line = await self._readline()
        await self._checkline(line)
        _LOGGER.debug(f"readline() = {line!r}")
        return line

    async def readlines(self, infinite=False, check=False):
        """
        Receive lines until an empty one.

        Raises:
            IOError: If connection is broken or cannot be established (`autoconnect==True`)
            ConnectionError: If not connected (`autoconnect==False`)
        """
        await self._ensure_connection()
        while True:
            line = await self._readline()
            if check:
                await self._checkline(line)
            _LOGGER.debug(f"readlines() = {line!r}")
            yield line
            if not line and not infinite:
                break

    async def _readline(self):
        line = await self._reader.readline()
        return line.decode("utf-8").rstrip()

    async def _ensure_connection(self):
        if not self._writer or self._writer.is_closing():
            if self._autoconnect:
                await self.connect()
            else:
                raise ConnectionError("Not connected")

    async def _timedout(self, task):
        if self._timeout:
            try:
                result = await asyncio.wait_for(task, timeout=self._timeout)
            except asyncio.TimeoutError:
                raise ConnectionTimeout(f"{self.host}:{self.port}")
        else:
            result = await task
        return result

    async def _checkline(self, line):
        if line.startswith("ERR: "):
            # consume everything until newline
            while await self._readline():
                pass
            raise CommandError(line.lstrip("ERR: "))


class CommandError(RuntimeError):
    pass


class ConnectionTimeout(RuntimeError):

    pass
