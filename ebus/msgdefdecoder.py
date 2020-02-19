import collections
import re

from .msgdef import FieldDef
from .msgdef import MsgDef

# https://github.com/john30/ebusd/wiki/4.1.-Message-definition#message-definition


def decode_msgdef(line):
    """
    Decode Message and Field Definition retrieved from ebusd.

    The EBUSD command `find -a -F type,circuit,name,fields` retrieves
    all message and field definitions of all known and connected devices.
    The resulting lines are decoded by this method and retrieve a proper
    :any:`MsgDef` instance per `str`.

    >>> m = decode_msgdef('r,mc.4,OtShutdownLimit,temp,s,UCH,,°C,"text, text"')
    >>> m.circuit, m.name, m.read, m.prio, m.write, m.update
    ('mc.4', 'OtShutdownLimit', True, None, False, False)
    >>> m.fields
    (FieldDef('temp', 'temp', ('UCH',), unit='°C', comment='text, text'),)

    >>> m = decode_msgdef('w,ui,TempIncrease,temp,m,D2C,,°C,Temperatur')
    >>> m.circuit, m.name, m.read, m.prio, m.write, m.update
    ('ui', 'TempIncrease', False, None, True, False)
    >>> m.fields
    (FieldDef('temp', 'temp', ('D2C',), unit='°C'),)
    """
    try:
        values = _split(line)
        type_, circuit, name = values[:3]
        read, prio, write, update = _decodetype(type_)
        fields = _decodefields(values[3:])
    except ValueError:
        raise ValueError(f"Invalid message definition {line!r}") from None
    return MsgDef(circuit, name, fields, read, prio, write, update)


def _split(line):
    values = []
    r = re.compile(r'("([^"]+)")|([^\,]*),')
    for idx, m in enumerate(r.finditer(line)):
        groups = m.groups()
        values.append(groups[1] or groups[2])
    return values


def _decodetype(type_):
    r = re.compile(r"\A(r)([1-9]?)\Z")
    m = r.match(type_)
    if m:
        read = m.group(1) is not None
        prio = int(m.group(2)) if m.group(2) else None
    else:
        read, prio = False, None
    write = "w" in type_
    update = not read and len(type_) > (1 if write else 0)
    return read, prio, write, update


def _decodefields(values):
    if len(values) % 6 in (0, 3, 4, 5):
        chunks = _chunks(values, 6)
        return tuple(_createfields(chunks))
    else:
        raise ValueError()


def _createfields(chunks):
    if chunks:
        # determine duplicate names
        dups = collections.defaultdict(lambda: -1)
        for name in tuple(zip(*chunks))[0]:
            dups[name] += 1
        # create fields
        cnts = collections.defaultdict(lambda: 0)
        for chunk in chunks:
            name = chunk[0]
            if dups[name]:
                cnt = cnts[name]
                cnts[name] = cnt + 1
                name = f"{name}.{cnt}"
            else:
                name = name
            yield _createfield(name, *chunk)


def _createfield(name, ename, part, datatype, dividervalues=None, unit=None, comment=None):
    types = tuple(datatype.split(","))
    return FieldDef(name, ename, types, dividervalues, unit, comment)


def _chunks(list_or_tuple, maxsize):
    return [list_or_tuple[i : i + maxsize] for i in range(0, len(list_or_tuple), maxsize)]
