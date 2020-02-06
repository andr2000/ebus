import collections

from .util import repr_

Error = collections.namedtuple("Error", "msg")


class Msg(collections.namedtuple("_Msg", "msgdef fields")):
    __slots__ = tuple()

    def __repr__(self):
        args = (self.msgdef.name, self.fields)
        return repr_(self, args)


class Field(collections.namedtuple("_Field", "msgdef fielddef value")):
    __slots__ = tuple()

    def __str__(self):
        fielddef = self.fielddef
        unit = fielddef.unit if self.value is not None and fielddef.unit else ""
        return f"{self.msgdef}/{fielddef.uname} {self.value}{unit}"

    def __repr__(self):
        args = (self.fielddef.uname, self.value)
        return repr_(self, args)


def filter_msg(msg, msgdefs):
    """Strip Down Message."""
    return msg
