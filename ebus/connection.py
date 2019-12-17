import asyncio


class Connection:
    """
    Ebus Connection.

    Keyword Args:
        host (str): Hostname or IP
        port (int): Port

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

    def __init__(self, host='127.0.0.1', port=8888):
        self._host = host
        self._port = port
        self._reader, self._writer = None, None

    async def connect(self):
        """Establish connection (required before first communication)."""
        self._reader, self._writer = await asyncio.open_connection(self._host, self._port)

    async def send(self, message):
        """Send `message`."""
        self._writer.write(f"{message}\n".encode())
        await self._writer.drain()

    async def receive(self):
        """Receive one line."""
        line = await self._reader.readline()
        return line.decode('utf-8').rstrip()

    async def read(self, name, field=None, circuit=None, ttl=None):
        """Read `name` extracting `field` from `circuit` not older than `ttl` seconds."""
        response = await self._request('read', [
            ('-m ', ttl),
            ('-c ', circuit),
            ('', name),
            ('', field),
        ])
        return response

    async def write(self, name, circuit, value):
        """Write `value` to `name` in `circuit`."""
        await self._request('write', [
            ('-c ', circuit),
            ('', name),
            ('', value),
        ])

    async def start_listening(self, verbose=False):
        """Start Listening."""
        command = 'listen -v' if verbose else 'listen'
        await self.send(command)
        # consume 'listen started'
        await self.receive()
        await self.receive()
        await self.receive()

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


class Error(RuntimeError):

    """Exception raised in case of an error."""
