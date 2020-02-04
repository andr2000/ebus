import collections
from fnmatch import fnmatchcase


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

    def find(self, circuit, name):
        """Find Message Definitions."""
        for msgdef in self:
            if fnmatchcase(msgdef.circuit, circuit) and fnmatchcase(msgdef.name, name):
                yield msgdef

    def resolve(self, path, nomsg=False, nofield=False):
        """Resolve path."""
        parts = path.split("/")
        if len(parts) == 2 and not nomsg:
            circuit, name = parts
            for msgdef in self.find(circuit, name):
                yield msgdef, None
        elif len(parts) == 3 and not nofield:
            circuit, name, fieldname = parts
            for msgdef in self.find(circuit, name):
                for fielddef in msgdef.fields:
                    if fnmatchcase(fielddef.name, fieldname):
                        yield msgdef, fielddef
        else:
            raise ValueError(f"Invalid path {path!r}")

    def get_info(self):
        """Human Information."""
        total = len(self)
        read = sum([1 for msgdef in self if msgdef.read])
        update = sum([1 for msgdef in self if msgdef.update])
        write = sum([1 for msgdef in self if msgdef.write])
        return f"{total} message definitions found ({read} read, {update} update, {write} write)"

    def __iter__(self):
        for circuitmsgdefs in self._msgdefs.values():
            yield from circuitmsgdefs.values()

    def __len__(self):
        return sum(len(defs) for defs in self._msgdefs.values())
