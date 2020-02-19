import collections
import copy
import re
from fnmatch import fnmatchcase

from .msgdef import MsgDef


class MsgDefs:

    """Message Defs Container."""

    _re_resolve = re.compile(r"\A([^/#]+)/([^/#]+)(#(\d))?(/([^/#]*))?\Z")

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
        self._msgdefs = collections.defaultdict(lambda: collections.defaultdict(list))

    def add(self, msgdef):
        """Add Message Definition."""
        self._msgdefs[msgdef.circuit][msgdef.name].append(msgdef)

    def get(self, circuit, name):
        """Retrieve circuit message."""
        msgdefs = self._msgdefs
        if circuit in msgdefs:
            circuitmsgdefs = msgdefs[circuit]
            if name in circuitmsgdefs:
                return circuitmsgdefs[name][0]

    def find(self, circuit, name="*"):
        """Find Message Definitions."""
        msgdefs = MsgDefs()
        for msgdef in self:
            if fnmatchcase(msgdef.circuit, circuit) and fnmatchcase(msgdef.name, name):
                msgdefs.add(msgdef)
        return msgdefs

    def resolve(self, patterns):
        """Resolve patterns."""
        msgdefs = MsgDefs()
        for pattern in patterns.split(";"):
            for msgdef in self._resolve(pattern.strip()):
                if msgdef not in msgdefs:
                    msgdefs.add(msgdef)
        return msgdefs

    def _resolve(self, pattern):
        m = self._re_resolve.fullmatch(pattern)
        if m:
            circuit, name, _, prio, _, fieldname = m.groups()
            for msgdef in self.find(circuit, name):
                if fieldname is None:
                    fields = msgdef.fields
                else:
                    fields = tuple(fielddef for fielddef in msgdef.fields if fnmatchcase(fielddef.name, fieldname))
                if not fields:
                    continue
                if fields == msgdef.fields and (prio is None or not msgdef.read):
                    yield msgdef
                else:
                    if prio is None:
                        prio = msgdef.prio
                    yield MsgDef(
                        msgdef.circuit,
                        msgdef.name,
                        tuple(copy.copy(fielddef) for fielddef in fields),
                        read=msgdef.read,
                        prio=prio,
                        write=msgdef.write,
                        update=msgdef.update,
                    )
        else:
            raise ValueError(f"Invalid pattern {pattern!r}")

    def get_info(self):
        """Human Information."""
        total = len(self)
        read = sum([1 for msgdef in self if msgdef.read])
        update = sum([1 for msgdef in self if msgdef.update])
        write = sum([1 for msgdef in self if msgdef.write])
        return f"{total} messages ({read} read, {update} update, {write} write)"

    def __iter__(self):
        for circuitmsgdefs in self._msgdefs.values():
            for msgdefs in circuitmsgdefs.values():
                yield from msgdefs

    def __len__(self):
        return sum(len(defs) for defs in self._msgdefs.values())
