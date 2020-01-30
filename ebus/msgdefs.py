"""MsgDefs."""
import collections

MsgDef = collections.namedtuple("MsgDef", "circuit name read prio write update fields")
FieldDef = collections.namedtuple("FieldDef", "uname name types dividervalues unit")


class MsgDefs:

    """Message Defs Container."""

    def __init__(self):
        """Message Defs Container."""
        # {
        #     circuit: {
        #         name: message
        #     }
        # }
        self._msgdefs = collections.defaultdict(lambda: collections.defaultdict(lambda: None))

    def add(self, msgdef):
        """Add Message Definition."""
        self._msgdefs[msgdef.circuit][msgdef.name] = msgdef

    def __iter__(self):
        for circuitmsgdefs in self._msgdefs.values():
            yield from circuitmsgdefs.values()
