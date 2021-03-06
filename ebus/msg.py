import collections

from .na import NA
from .util import repr_

Error = collections.namedtuple("Error", "msg")


class Msg(collections.namedtuple("_Msg", "msgdef fields")):
    __slots__ = tuple()

    def __repr__(self):
        args = (self.msgdef.name, self.fields)
        return repr_(self, args)

    @property
    def ident(self):
        """Identifier."""
        return self.msgdef.ident


class Field(collections.namedtuple("_Field", "fielddef value")):
    __slots__ = tuple()

    def __repr__(self):
        args = (self.fielddef.name, self.value)
        return repr_(self, args)

    @property
    def ident(self):
        """Identifier."""
        return self.fielddef.ident

    @property
    def unitvalue(self):
        """Unitized Value."""
        value = self.value
        if value is not None and value is not NA:
            if not isinstance(value, str) and self.fielddef.unit:
                return f"{value}{self.fielddef.unit}"
            else:
                return value
        else:
            return None


def filter_msg(msg, msgdefs):
    """Strip Down Message."""
    ident = msg.msgdef.ident
    for msgdef in msgdefs:
        if ident == msgdef.ident:
            if msg.msgdef == msgdef:
                return msg
            else:
                fields = tuple(
                    Field(field.fielddef, field.value) for field in msg.fields if field.fielddef in msgdef.fields
                )
                return Msg(msgdef, fields)
