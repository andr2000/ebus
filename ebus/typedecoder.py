import datetime


class TypeDecoder:
    """
    Convert EBUSD strings to python types.

    See https://github.com/john30/ebusd/wiki/4.3.-Builtin-data-types

    String types are just kept as is. Simple casts are stored in `_casts`
    """

    _remap = {
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

    def __call__(self, fielddef, value):
        """Convert `value` to python value."""
        name = fielddef.types[0].split(":")[0].lower()
        if fielddef.values is None:
            methodname = self._remap.get(name, name)
            method = getattr(self, "_" + methodname, None)
            if method:
                value = method(fielddef, value)
        return value

    @staticmethod
    def _date(fielddef, value):
        if value != "-.-.-":
            return datetime.datetime.strptime(value, "%d.%m.%Y")

    @staticmethod
    def _hhmm(fielddef, value):
        if value != "-:-":
            return datetime.datetime.strptime(value, "%H:%M")

    @staticmethod
    def _hhmmss(fielddef, value):
        if value != "-:-:-":
            return datetime.datetime.strptime(value, "%H:%M:%S")

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
