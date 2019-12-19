import asyncio


class Connection:
    """
    Ebus Connection.

    Keyword Args:
        host (str): Hostname or IP
        port (int): Port
        autoconnect (bool): Automatically connect and re-connect

    >>> async def app():
    ...    c = Connection()
    ...    await c.connect()
    ...    line = await c.read('WaterPressure press', circuit='bai')
    ...    print(line)
    ...
    ...    await c.start_listening()
    ...    while True:
    ...        line = await c.receive()
    ...        print(line)
    """

    def __init__(self, host='127.0.0.1', port=8888, autoconnect=False):
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
        self._reader, self._writer = await asyncio.open_connection(self._host, self._port)

    async def disconnect(self):
        """Disconnect if not already done."""
        if self._writer:
            self._writer.close()
            await self._writer.wait_closed()
            self._reader, self._writer = None, None

    def is_connected(self):
        """
        Return `True` if connection is established.

        This does not check if the connection is still usable.
        """
        return self._writer and not self._writer.is_closing()

    async def send(self, message):
        """
        Send `message`.

        Raises:
            IOError: If connection is broken or cannot be established (`autoconnect==True`)
            NotConnectedError: If not connected (`autoconnect==False`)
        """
        await self._ensure_connection()
        self._writer.write(f"{message}\n".encode())
        await self._writer.drain()

    async def receive(self):
        """
        Receive one line.

        Raises:
            IOError: If connection is broken or cannot be established (`autoconnect==True`)
            NotConnectedError: If not connected (`autoconnect==False`)
        """
        await self._ensure_connection()
        line = await self._reader.readline()
        line = line.decode('utf-8').rstrip()
        if line == "ERR: shutdown":
            await self.disconnect()
            raise Error('disconnect')
        return line

    async def read(self, name, field=None, circuit=None, ttl=None, verbose=False):
        """
        Read `name` extracting `field` from `circuit` not older than `ttl` seconds.

        Raises:
            Error: In case of an unknown command or command argument (response contains `ERR`)
            IOError: If connection is broken or cannot be established (`autoconnect==True`)
            NotConnectedError: If not connected (`autoconnect==False`)
        """
        await self._ensure_connection()
        response = await self._request('read', [
            ('-m ', ttl),
            ('-c ', circuit),
            ('', name),
            ('', field),
            ('-v ' if verbose else '', ''),
        ])
        return response

    async def write(self, name, circuit, value):
        """
        Write `value` to `name` in `circuit`.

        Raises:
            Error: In case of an unknown command or command argument (response contains `ERR`)
            IOError: If connection is broken or cannot be established (`autoconnect==True`)
            NotConnectedError: If not connected (`autoconnect==False`)
        """
        await self._ensure_connection()
        await self._request('write', [
            ('-c ', circuit),
            ('', name),
            ('', value),
        ])

    async def start_listening(self, verbose=False):
        """Start Listening."""
        await self._ensure_connection()
        command = 'listen -v' if verbose else 'listen'
        await self.send(command)
        # consume 'listen started'
        await self.receive()
        await self.receive()
        await self.receive()

    async def _ensure_connection(self):
        if not self._writer or self._writer.is_closing():
            if self._autoconnect:
                await self.connect()
            else:
                raise NotConnectedError()

    async def _request(self, command, options):
        args = ''.join([f'{option} {value} '
                        for option, value in options
                        if value is not None])
        await self.send(f'{command} {args}')
        line = await self.receive()
        self._checkresponse(line)
        return line

    @staticmethod
    def _checkresponse(line):
        if "ERR:" in line:
            raise CommandError(line)


class NotConnectedError(OSError):
    """Connection is not established."""


class Error(RuntimeError):
    """Exception raised in case of an error."""
