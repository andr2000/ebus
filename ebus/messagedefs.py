"""MessageDefs."""
import collections

MessageDef = collections.namedtuple("MessageDef", "circuit name read prio write update fields")
FieldDef = collections.namedtuple("FieldDef", "name types dividervalues unit")


class MessageDefs:

    """Message Defs Container."""

    def __init__(self):
        """Message Defs Container."""
        # {
        #     circuit: {
        #         name: message
        #     }
        # }
        self._messagedefs = collections.defaultdict(lambda: collections.defaultdict(lambda: None))

    def add(self, messagedef):
        """Add Message Definition."""
        self._messagedefs[messagedef.circuit][messagedef.name] = messagedef

    def __iter__(self):
        for circuitmessagedefs in self._messagedefs.values():
            yield from circuitmessagedefs.values()
