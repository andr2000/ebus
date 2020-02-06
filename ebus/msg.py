import collections

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
        args = (self.fielddef.uname, self.value)
        return repr_(self, args)

    @property
    def ident(self):
        """Identifier."""
        return self.fielddef.ident

    @property
    def unitvalue(self):
        """Unitized Value."""
        if self.value is not None:
            if self.fielddef.unit:
                return f"{self.value}{self.fielddef.unit}"
            else:
                return self.value
        else:
            return None


def filter_msg(msg, msgdefs):
    """Strip Down Message."""
    k = (msg.msgdef.circuit, msg.msgdef.name)
    for msgdef in msgdefs:
        if k == (msgdef.circuit, msgdef.name):
            if msg.msgdef == msgdef:
                return msg
            else:
                fields = tuple(
                    Field(field.fielddef, field.value) for field in msg.fields if field.fielddef in msgdef.fields
                )
                return Msg(msgdef, fields)
