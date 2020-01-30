import asyncio


class Connection:
    def __init__(self, host="127.0.0.1", port=8888, autoconnect=False):
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
        self._reader, self._writer = None, None

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

    async def connect(self):
        """
        Establish connection (required before first communication).

        Raises:
            IOError: If connection cannot be established
        """
        self._reader, self._writer = await asyncio.open_connection(
            self._host, self._port
        )

    async def disconnect(self):
        """Disconnect if not already done."""
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
        await self._ensure_connection()
        self._writer.write(f"{message}\n".encode())
        await self._writer.drain()

    async def readline(self):
        """
        Receive one line.

        Raises:
            IOError: If connection is broken or cannot be established (`autoconnect==True`)
            ConnectionError: If not connected (`autoconnect==False`)
        """
        await self._ensure_connection()
        line = await self._reader.readline()
        line = line.decode("utf-8").rstrip()
        await self._checkline(line)
        return line

    async def readlines(self):
        """
        Receive lines until an empty one.

        Raises:
            IOError: If connection is broken or cannot be established (`autoconnect==True`)
            ConnectionError: If not connected (`autoconnect==False`)
        """
        await self._ensure_connection()
        while True:
            line = await self._reader.readline()
            line = line.decode("utf-8").rstrip()
            await self._checkline(line)
            if line:
                yield line
            else:
                break

    async def _ensure_connection(self):
        if not self._writer or self._writer.is_closing():
            if self._autoconnect:
                await self.connect()
            else:
                raise ConnectionError("Not connected")

    async def _checkline(self, line):
        if line.startswith("ERR: "):
            detail = line.lstrip("ERR: ")
            await self.disconnect()
            raise CommandError(detail)


class CommandError(RuntimeError):
    pass
