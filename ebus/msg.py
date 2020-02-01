import collections

from .util import repr_

Error = collections.namedtuple("Error", "msg")


class Msg(collections.namedtuple("_Msg", "circuit msgdef fields")):
    __slots__ = tuple()

    def __repr__(self):
        args = (self.circuit, self.msgdef.name, self.fields)
        return repr_(self, args)


class Field(collections.namedtuple("_Field", "fielddef value")):
    __slots__ = tuple()

    def __repr__(self):
        args = (self.fielddef.uname, self.value)
        return repr_(self, args)
