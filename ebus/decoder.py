"""Home-Assistant Friendly Decoder."""
import collections
import re

Value = collections.namedtuple('Value', 'field circuit value')


class Decoder:

    """Home-Assistant Friendly Decoder."""

    def __init__(self, fields, units):
        """
        Home-Assistant Friendly Decoder.

        Args:
            fields (Fields): Field container instance
            units (Fields): Unit container instance
        """
        self.fields = fields
        self.units = units
        self._re_decode = re.compile(r'([A-z0-9]+(\.[A-z0-9]+)?) ([A-z0-9]+) = (.*)')
        self._re_ignores = []
        self._unknowns = []

    def add_ignore(self, regex):
        """Ignore what matches to `regex` instead of complaining."""
        self._re_ignores.append(re.compile(regex))

    def decode(self, line):
        """
        Decode `line` and return :any:`Value`.

        Raises:
            FormatError: if `line` does not match expected format.
            UnknownError: if `line` is not covered by fields.
        """
        match = self._re_decode.match(line)
        if match:
            circuit, _, name, valuestr = match.groups()
            fields = self.fields.get(circuit, name)
            if fields:
                # create values dict
                values = {}
                for idx, pair in enumerate(valuestr.split(';')):
                    sub, value = pair.split('=', 1)
                    values.setdefault(sub, value)  # first wins
                    values[str(idx)] = value
                # sub handling
                for field in fields:
                    if field.sub is None:
                        value = self.units.decode(field.unitname, valuestr)
                        yield Value(field, circuit, value)
                    else:
                        try:
                            value = values[field.sub]
                        except KeyError:
                            yield Value(field, circuit, None)
                        else:
                            value = self.units.decode(field.unitname, value)
                            yield Value(field, circuit, value)
            else:
                for re_ignore in self._re_ignores:
                    if re_ignore.match(line):
                        break
                else:
                    if (circuit, name) not in self._unknowns:
                        self._unknowns.append((circuit, name))
                        raise UnknownError(line)
        else:
            raise FormatError(line)


class FormatError(RuntimeError):

    """Exception raised in case of a format error."""


class UnknownError(RuntimeError):

    """Exception raised in case of unknown values."""
