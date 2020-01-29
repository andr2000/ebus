"""EBUSD Message Definition Decoder."""
import re

from .messagedefs import FieldDef
from .messagedefs import MessageDef

# https://github.com/john30/ebusd/wiki/4.1.-Message-definition#message-definition


def decode(line):
    """
    Decode Message and Field Definition retrieved from ebusd.

    The EBUSD command `find -F type,circuit,name,fields` retrieves
    all message and field definitions of all known and connected devices.
    The resulting lines are decoded by this method and retrieve a proper
    :any:`MessageDef` instance per `str`.

    >>> m = decode('r,mc.4,OtShutdownLimit,temp,s,UCH,,°C,"text, text"')
    >>> m.circuit, m.name, m.read, m.prio, m.write, m.update
    ('mc.4', 'OtShutdownLimit', True, None, False, False)
    >>> m.fields  # doctest: +ELLIPSIS
    (FieldDef(name='temp', types=('UCH',), dividervalues='', unit='°C'...

    >>> m = decode('w,ui,TempIncrease,temp,m,D2C,,°C,Temperatur')
    >>> m.circuit, m.name, m.read, m.prio, m.write, m.update
    ('ui', 'TempIncrease', False, None, True, False)
    >>> m.fields  # doctest: +ELLIPSIS
    (FieldDef(name='temp', types=('D2C',), dividervalues='', unit='°C'...
    """
    values = _split(line)
    type_, circuit, name = values[:3]
    read, prio, write, update = _decodetype(type_)
    fields = _decodefields(values[3:])
    return MessageDef(circuit, name, read, prio, write, update, fields)


def _split(line):
    values = []
    r = re.compile(r'("([^"]+)")|([^\,]*),')
    for idx, m in enumerate(r.finditer(line)):
        groups = m.groups()
        values.append(groups[1] or groups[2])
    return values


def _decodetype(type_):
    r = re.compile(r'\A(r)([1-9]?)\Z')
    m = r.match(type_)
    if m:
        read = m.group(1) is not None
        prio = int(m.group(2)) if m.group(2) else None
    else:
        read, prio = False, None
    write = 'w' in type_
    update = not read and len(type_) > (1 if write else 0)
    return read, prio, write, update


def _decodefields(values):
    if len(values) % 6 in (0, 3, 4, 5):
        fields = []
        while values:
            fields.append(_decodefield(*values[:6]))
            values = values[6:]
        return tuple(fields)
    else:
        raise ValueError(values)


def _decodefield(name, part, datatype, dividervalues=None, unit=None, *args):
    types = tuple(datatype.split(";"))
    return FieldDef(name, types, dividervalues, unit)
