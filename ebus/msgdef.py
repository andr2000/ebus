import collections

from .util import repr_

_MsgDef = collections.namedtuple("_MsgDef", "circuit name fields read prio write update")


class MsgDef(_MsgDef):

    __slots__ = tuple()

    def __new__(cls, circuit, name, fields, read=False, prio=None, write=False, update=False):
        """
        Message Definition.

        Args:
            circuit (str): Circuit Name
            name (str): Message Name
            fields (tuple): Fields

        Keyword Args:
            read (bool): Message intend to be read
            prio (int): Message Polling Priority
            write (bool): Message intend to be written
            updated (bool): Message intent to be seen automatically on every value change
        """
        return _MsgDef.__new__(cls, circuit, name, fields, read, prio, write, update)

    def __repr__(self):
        args = (self.circuit, self.name, self.fields)
        kwargs = [
            ("read", self.read, False),
            ("prio", self.prio, None),
            ("write", self.write, False),
            ("update", self.update, False),
        ]
        return repr_(self, args, kwargs)

    @property
    def type_(self):
        """Message Type."""
        r = "r" if self.read else "-"
        p = f"{self.prio}" if self.prio else "-"
        w = "w" if self.write else "-"
        u = "u" if self.update else "-"
        return "".join((r, p, w, u))


_FieldDef = collections.namedtuple("_FieldDef", "uname name types dividervalues unit")


class FieldDef(_FieldDef):

    __slots__ = tuple()

    def __new__(cls, uname, name, types, dividervalues=None, unit=None):
        """
        Field Definition.

        Args:
            uname (str): Unique name (as `name` may be used multiple times by ebus)
            name (str): Name
            types (tuple): Tuple of type idenfifier

        Keywords Args:
            dividervalues (str): EBUS Divider or value specification
            unit (str): Unit of the field value
        """
        return _FieldDef.__new__(cls, uname, name, types, dividervalues, unit)

    def __repr__(self):
        args = (self.uname, self.name, self.types)
        kwargs = [
            ("dividervalues", self.dividervalues, None),
            ("unit", self.unit, None),
        ]
        return repr_(self, args, kwargs)

    @property
    def divider(self):
        """Divider if given."""
        dividervalues = self.dividervalues
        if dividervalues and "=" not in dividervalues:
            divider = float(self.dividervalues)
            if divider < 0:
                divider = 1 / -divider
            return divider

    @property
    def values(self):
        """Return valuemap."""
        dividervalues = self.dividervalues
        if dividervalues and "=" in dividervalues:
            return dict([pair.split("=", 1) for pair in dividervalues.split(";")])
