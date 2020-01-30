# """Home-Assistant Friendly Decoder."""
import collections
import re

from .typehandler import TypeHandler

Msg = collections.namedtuple('Msg', 'circuit msgdef fields')
Field = collections.namedtuple('Field', 'fielddef value')


class MsgDecoder:

    """Message Decoder."""

    _re_decode = re.compile(r'(([A-z0-9]+)(\.[A-z0-9]+)?) ([^\s]*) (= )?(.*)')

    def __init__(self, msgdefs):
        """
        Message Decoder.

        Args:
            msgdefs (MsgDefs): Message Definitions
        """
        self.msgdefs = msgdefs
        self.typehandler = TypeHandler()

    def decode(self, line):
        """
        Decode `line` and yield :any:`Msg` instances.

        Raises:
            FormatError: if `line` does not match expected format.
            UnknownError: if `line` is not covered by fields.
        """
        match = self._re_decode.match(line)
        if not match:
            raise ValueError(line)
        circuit, circuitbasename, _, name, _, valuestr = match.groups()
        msgdef = self.msgdefs.get(circuitbasename, name)
        if not msgdef:
            raise UnknownMsgError(f'circuit={circuit}, name={name}')
        fields = tuple(self._decodefields(msgdef.fields, valuestr.split(";")))
        return Msg(circuit, msgdef, fields)

    def _decodefields(self, fielddefs, values):
        typehandler = self.typehandler
        for fielddef, value in zip(fielddefs, values):
            yield Field(fielddef, typehandler(fielddef, value.strip()))


class UnknownMsgError(RuntimeError):

    """Exception raised in case of unknown Message."""
