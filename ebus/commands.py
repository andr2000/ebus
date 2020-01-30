async def read(connection, name, field=None, circuit=None, ttl=None, verbose=False):
    """
    Read `name` extracting `field` from `circuit` not older than `ttl` seconds.

    Raises:
        CommandError: In case of an unknown command or command argument (response contains `ERR`)
        IOError: If connection is broken or cannot be established (`autoconnect==True`)
        ConnectionError: If not connected (`autoconnect==False`)
    """
    lines = tuple(
        await request(
            connection,
            "read",
            [
                ("-v" if verbose else "", ""),
                ("-m", ttl),
                ("-c", circuit),
                ("", name),
                ("", field),
            ],
        )
    )
    return lines[0]


async def write(connection, name, circuit, value):
    """
    Write `value` to `name` in `circuit`.

    Raises:
        CommandError: In case of an unknown command or command argument (response contains `ERR`)
        IOError: If connection is broken or cannot be established (`autoconnect==True`)
        ConnectionError: If not connected (`autoconnect==False`)
    """
    await request(connection, "write", [("-c ", circuit), ("", name), ("", value),])


async def request(connection, command, options=None):
    """Assemble request, send and readlines."""
    args = "".join(
        [f"{option} {value} " for option, value in (options or []) if value is not None]
    )
    await connection.write(f"{command} {args}")
    return await connection.readlines()


async def start_listening(connection, verbose=False):
    """Start Listening."""
    await request(connection, "listen -v")


async def info(connection):
    """Retrieve Information."""
    lines = await request(connection, "info")
    addresses = {}
    data = {"addresses": addresses}
    for line in lines:
        name, value = line.split(": ", 1)
        if name.startswith("address "):
            address = int(name[len("address ") :], 16)
            parts = value.split(", ")
            addresses[address] = parts
        else:
            data[name] = value.strip()
    return data
