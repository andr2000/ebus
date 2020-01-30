"""MsgDefs."""
import collections

MsgDef = collections.namedtuple("MsgDef", "circuit name read prio write update fields")
FieldDef = collections.namedtuple("FieldDef", "uname name types unit")


class MsgDefs:

    """Message Defs Container."""

    def __init__(self):
        """
        Message Defs Container.

        >>> msgdefs = MsgDefs()
        >>> msgdef = MsgDef('mc', 'Status0a', True, None, False, False, (
        ...     FieldDef('temp', 'temp', ('D2C',), '°C'),
        ...     FieldDef('mixer', 'mixer', ('UCH',), None),
        ...     FieldDef('onoff-0', 'onoff', ('UCH',), None),
        ...     FieldDef('onoff-1', 'onoff', ('UCH',), None),
        ...     FieldDef('temp0', 'temp0', ('UCH',), '°C'),
        ... ))
        >>> msgdefs.add(msgdef)
        >>> msgdefs.get('mc', 'Status0a')
        MsgDef(circuit='mc', name='Status0a', ..., unit='°C')))
        """
        self._msgdefs = collections.defaultdict(lambda: collections.defaultdict(lambda: None))

    def add(self, msgdef):
        """Add Message Definition."""
        self._msgdefs[msgdef.circuit][msgdef.name] = msgdef

    def get(self, circuit, name):
        """Retrieve circuit message."""
        msgdefs = self._msgdefs
        if circuit in msgdefs:
            circuitmsgdefs = msgdefs[circuit]
            if name in circuitmsgdefs:
                return circuitmsgdefs[name]

    def __iter__(self):
        for circuitmsgdefs in self._msgdefs.values():
            yield from circuitmsgdefs.values()
