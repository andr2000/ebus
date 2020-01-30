# """Home-Assistant Friendly Decoder."""
import collections
import re

from .typedecoder import TypeDecoder

Msg = collections.namedtuple('Msg', 'circuit msgdef fields')
Field = collections.namedtuple('Field', 'fielddef value')
Error = collections.namedtuple('Error', 'msg')


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
        self.typedecoder = TypeDecoder()

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
        typedecoder = self.typedecoder
        for fielddef, value in zip(fielddefs, values):
            if not value.startswith("ERR: "):
                yield Field(fielddef, typedecoder(fielddef, value.strip()))
            else:
                yield Field(fielddef, Error(value.lstrip("ERR: ")))


class UnknownMsgError(RuntimeError):

    """Exception raised in case of unknown Message."""
