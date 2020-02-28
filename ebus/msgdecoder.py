import re

from .msg import Field
from .msg import Msg
from .na import NA
from .na import NotAvailable
from .util import repr_


class MsgDecoder:

    _re_decode = re.compile(r"([A-z0-9]+(\.[A-z0-9]+)?) ([^\s]*) (= )?(.*)")

    def __init__(self, msgdefs):
        """
        Message Decoder.

        Args:
            msgdefs (MsgDefs): Message Definitions
        """
        self.msgdefs = msgdefs

    def decode_line(self, line):
        """
        Decode `line` and return :any:`Msg` instance.

        Raises:
            ValueError: if `line` does not match expected format.
            UnknownMsgError: if `line` is not covered by fields.
        """
        match = self._re_decode.match(line)
        if not match:
            raise ValueError(line)
        circuit, _, name, _, valuestr = match.groups()
        msgdef = self.msgdefs.get(circuit, name)
        if not msgdef:
            raise UnknownMsgError(f"circuit={circuit}, name={name}")
        return self.decode_value(msgdef, valuestr.strip(), circuit=circuit)

    def decode_value(self, msgdef, valuestr, circuit=None):
        """Decode message `msgdef` valuestr `valuestr`."""
        values = valuestr.split(";")
        if (valuestr or len(values) == len(msgdef.fields)) and valuestr != "no data stored" and "ERR: " not in valuestr:
            fields = tuple(self._decodefields(msgdef, values))
            return Msg(msgdef, fields)
        else:
            return BrokenMsg(msgdef, valuestr.strip())

    def _decodefields(self, msgdef, values):
        fields = []
        for fielddef in msgdef.fields:
            if fielddef.idx is None:
                continue
            try:
                value = values[fielddef.idx].strip()
            except IndexError:
                fieldvalue = NA
            else:
                fieldvalue = fielddef.type_.decode(value)
            fields.append(Field(fielddef, fieldvalue))
        for virtfielddef in msgdef.virtfields:
            virtfieldvalue = virtfielddef.func(fields)
            fields.append(Field(virtfielddef, virtfieldvalue))
        return fields


class UnknownMsgError(RuntimeError):

    """Exception raised in case of unknown Message."""


class BrokenMsg:
    def __init__(self, msgdef, error):
        """
        Broken Message.

        .. note: In a boolean context this instance evaluates to `False`.
        """
        self.msgdef = msgdef
        self.error = error

    def __repr__(self):
        return repr_(self, (self.msgdef.ident, self.error))
