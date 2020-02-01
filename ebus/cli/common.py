def add_connection_args(parser):
    """Add Connection arguments to parser."""
    parser.add_argument("--host", "-H", default="127.0.0.1", help="EBUSD address. Default is '172.0.0.1'.")
    parser.add_argument("--port", "-p", default=8888, type=int, help="EBUSD port. Default is 8888.")
