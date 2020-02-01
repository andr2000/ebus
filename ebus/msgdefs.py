import collections


class MsgDefs:

    """Message Defs Container."""

    def __init__(self):
        """
        Message Defs Container.

        >>> from .msgdef import MsgDef, FieldDef
        >>> msgdefs = MsgDefs()
        >>> msgdefs.add(MsgDef('mc', 'Status0a', (
        ...     FieldDef('temp', 'temp', ('D2C',), None, '°C'),
        ...     FieldDef('mixer', 'mixer', ('UCH',), None, None),
        ...     FieldDef('onoff-0', 'onoff', ('UCH',), None, None),
        ...     FieldDef('onoff-1', 'onoff', ('UCH',), None, None),
        ...     FieldDef('temp0', 'temp0', ('UCH',), None, '°C'),
        ... ), read=True))
        >>> msgdefs.add(MsgDef('hc', 'Status0', (
        ...     FieldDef('temp', 'temp', ('D2C',), None, '°C'),
        ...     FieldDef('temp0', 'temp0', ('UCH',), None, '°C'),
        ... ), read=True))
        >>> msgdefs.get('mc', 'Status0a')
        MsgDef('mc', 'Status0a', (FieldDef('temp', ...'°C'), FieldDef('mixer', ..., ('UCH',), unit='°C')), read=True)
        >>> list(msgdefs)
        [MsgDef('mc', 'Status0a', (FieldDef('temp', ...'°C'), FieldDef('mixer', ..., ('UCH',), unit='°C')), read=True)]
        """
        self.clear()

    def clear(self):
        """Clear."""
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

    def __len__(self):
        return sum(len(defs) for defs in self._msgdefs)
