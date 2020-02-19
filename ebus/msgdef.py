import collections

from anytree import NodeMixin

from .util import repr_

_MsgDef = collections.namedtuple("_MsgDef", "circuit name read prio write update")


class MsgDef(_MsgDef, NodeMixin):

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
        if not read:
            prio = None
        msgdef = _MsgDef.__new__(cls, circuit, name, read, prio, write, update)
        if fields:
            msgdef.children = fields
        return msgdef

    def __repr__(self):
        args = (self.circuit, self.name, self.fields)
        kwargs = [
            ("read", self.read, False),
            ("prio", self.prio, None),
            ("write", self.write, False),
            ("update", self.update, False),
        ]
        return repr_(self, args, kwargs)

    def __ident(self):
        return (self.circuit, self.name, self.fields, self.read, self.prio, self.write, self.update)

    def __hash__(self):
        return hash(self.__ident())

    def __eq__(self, other):
        if isinstance(other, MsgDef):
            return self.__ident() == other.__ident()
        else:
            return False

    @property
    def fields(self):
        """Fields."""
        return self.children

    @property
    def ident(self):
        """Identifier."""
        return f"{self.circuit}/{self.name}"

    @property
    def type_(self):
        """Message Type."""
        r = "r" if self.read else "-"
        p = f"{self.prio}" if self.prio else "-"
        w = "w" if self.write else "-"
        u = "u" if self.update else "-"
        return "".join((r, p, w, u))


_FieldDef = collections.namedtuple("_FieldDef", "idx name ename types dividervalues unit comment")


class FieldDef(_FieldDef, NodeMixin):

    __slots__ = tuple()

    def __new__(cls, idx, name, ename, types, dividervalues=None, unit=None, comment=None):
        """
        Field Definition.

        Args:
            idx (str): Index within Message
            name (str): Unique name (as `name` may be used multiple times by ebus)
            ename (str): Ebus Name
            types (tuple): Tuple of type idenfifier

        Keywords Args:
            dividervalues (str): EBUS Divider or value specification
            unit (str): Unit of the field value
            comment (str): Comment.
        """
        return _FieldDef.__new__(cls, idx, name, ename, types, dividervalues or None, unit or None, comment or None)

    def __repr__(self):
        args = (self.idx, self.name, self.ename, self.types)
        kwargs = [
            ("dividervalues", self.dividervalues, None),
            ("unit", self.unit, None),
            ("comment", self.comment, None),
        ]
        return repr_(self, args, kwargs)

    def _pre_detach(self, parent):
        # it is forbidden to remove fields from their message - create new one
        assert False, f"{self!r} is already used by {parent!r}"  # pragma: no cover

    @property
    def ident(self):
        """Identifier."""
        return f"{self.parent.ident}/{self.name}" if self.parent else None

    def __copy__(self):
        return FieldDef(
            idx=self.idx,
            name=self.name,
            ename=self.ename,
            types=self.types,
            dividervalues=self.dividervalues,
            unit=self.unit,
        )

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
