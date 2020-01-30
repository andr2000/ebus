import datetime


class TypeHandler:
    """
    Convert valuestr to python value.

    See https://github.com/john30/ebusd/wiki/4.3.-Builtin-data-types

    String types are just kept as is. Simple casts are stored in `_casts`
    """

    _casts = {
        'BDA': lambda value: datetime.datetime.strptime(value, '%d.%m.%Y')
        # 'BDA': lambda value: datetime.datetime.strptime(value, '%d.%m.%Y')
    }

    def __call__(self, fielddef, valuestr):
        typename = fielddef.types[0]
        basename = typename.split(":")[0]
        cast = self._casts.get(basename, None)
        if cast:
            return cast(valuestr)
        return valuestr
