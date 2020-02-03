import sys


def repr_(obj, args=None, kwargs=None):
    """
    Return Python Representation String.

    Keyword Args:
        args (tuple): Tuple with all arg values
        kwargs (tuple): Tuple of (key, value, default) tuples.
    """
    classname = obj.__class__.__qualname__
    args = [repr(arg) for arg in args or []]
    if kwargs:
        for key, value, default in kwargs:
            if value != default:
                args.append("%s=%r" % (key, value))
    return "%s(%s)" % (classname, ", ".join(args))


class UnbufferedStream:
    def __init__(self, stream):
        """Write unbuffered to `stream`."""
        self.stream = stream

    def write(self, *args, **kwargs):
        """Write."""
        self.stream.write(*args, **kwargs)
        self.stream.flush()

    def writelines(self, *args, **kwargs):
        """Write multiple lines."""
        self.stream.writelines(*args, **kwargs)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)
