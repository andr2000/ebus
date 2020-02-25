import datetime

from . import types

_PYTYPEMAP = {
    "bda": "date",
    "hda": "date",
    "day": "date",
    "bti": "hhmmss",
    "hti": "hhmmss",
    "vti": "hhmmss",
    "btm": "hhmm",
    "htm": "hhmm",
    "vtm": "hhmm",
    "min": "hhmm",
    "ttm": "hhmm",
    "tth": "hhmm",
    "ttq": "hhmm",
    "bcd": "int",
    "uch": "int",
    "sch": "int",
    "d1b": "int",
    "d1c": "float",
    "d2b": "float",
    "d2c": "float",
    "flt": "float",
    "flr": "float",
    "exp": "float",
    "exr": "float",
    "uin": "int",
    "uir": "int",
    "sin": "int",
    "sir": "int",
    "u3n": "int",
    "u3r": "int",
    "s3n": "int",
    "s3r": "int",
    "ulg": "int",
    "ulr": "int",
    "slg": "int",
    "slr": "int",
    "bi0": "bool",
}


def get_typename(type_):
    """
    Get our name for EBUSD `type`.

    >>> get_typename('hda')
    'date'
    >>> get_typename('hti')
    'hhmmss'
    >>> get_typename('flt')
    'float'
    >>> get_typename('uin')
    'int'
    """
    if type_:
        name = type_.split(":")[0].lower()
        return _PYTYPEMAP.get(name, None)


class TypeDecoder:
    """
    Convert EBUSD strings to python types.

    See https://github.com/john30/ebusd/wiki/4.3.-Builtin-data-types

    String types are just kept as is. Simple casts are stored in `_casts`

    >>> import ebus
    >>> typedecoder = ebus.TypeDecoder()
    >>> fielddef = ebus.FieldDef(0, "uname", "name", ("uin",))
    >>> typedecoder(fielddef, '7')
    7

    >>> fielddef = ebus.FieldDef(0, "uname", "name", ("hda",))
    >>> v = typedecoder(fielddef, '21.1.2019')
    >>> v
    Date(2019, 1, 21)
    >>> str(v)
    '2019-01-21'

    >>> fielddef = ebus.FieldDef(0, "uname", "name", ("hti",))
    >>> v = typedecoder(fielddef, '22:55:03')
    >>> v
    HourMinuteSecond(22, 55, 3)
    >>> str(v)
    '22:55:03'

    Unknown types are just handled as strings:

    >>> fielddef = ebus.FieldDef(0, "uname", "name", ("foo",))
    >>> typedecoder(fielddef, '7')
    '7'

    Unknown values become `None`:

    >>> fielddef = ebus.FieldDef(0, "uname", "name", ("bi0",))
    >>> typedecoder(fielddef, '-')
    """

    def __call__(self, fielddef, value):
        """Convert `value` to python value."""
        if fielddef.values is None:
            pytype = get_typename(fielddef.types[0])
            if pytype:
                method = getattr(self, "_" + pytype)
                value = method(fielddef, value)
        return value

    @staticmethod
    def _date(fielddef, value):
        if value != "-.-.-":
            dt = datetime.datetime.strptime(value, "%d.%m.%Y")
            return types.Date(dt.year, dt.month, dt.day)

    @staticmethod
    def _hhmm(fielddef, value):
        if value != "-:-":
            dt = datetime.datetime.strptime(value, "%H:%M")
            return types.HourMinute(dt.hour, dt.minute)

    @staticmethod
    def _hhmmss(fielddef, value):
        if value != "-:-:-":
            dt = datetime.datetime.strptime(value, "%H:%M:%S").time()
            return types.HourMinuteSecond(dt.hour, dt.minute, dt.second)

    @staticmethod
    def _int(fielddef, value):
        if value != "-":
            if fielddef.dividervalues:
                return float(value)
            else:
                return int(value)

    @staticmethod
    def _float(fielddef, value):
        if value != "-":
            return float(value)

    @staticmethod
    def _bool(fielddef, value):
        if value != "-":
            return bool(int(value))
