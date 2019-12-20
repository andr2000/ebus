"""Unit Handling."""
import datetime


class Unit:

    def __init__(self, name, decode=None, icon=None, uom=None):
        """
        Unit Description.

        Args:
            name (str): Unique Identifier
            decode (callable): Function for decoding

        Keyword Args:
            icon (str): icon to use in hass.
            uom (str): unit of measurement in hass
        """
        self._name = name
        self._decode = decode
        self._icon = icon
        self._uom = uom

    @property
    def name(self):
        """Name."""
        return self._name

    @property
    def decode(self):
        """Decode Function."""
        return self._decode

    @property
    def icon(self):
        """Icon in HASS."""
        return self._icon

    @property
    def uom(self):
        """Unit of Measurement in HASS."""
        return self._uom

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self.name!r}, icon={self.icon!r}), uom={self.uom!r})"


class Units:

    def __init__(self):
        """Container for Units."""
        self._units = {}

    def add(self, unit):
        """Add :any:`Unit`."""
        self._units[unit.name] = unit

    def get(self, unitname):
        """Retrieve unit name `unitname` if available."""
        return self._units.get(unitname, None)

    def decode(self, unitname, valuestr, value=None):
        """
        Use unit with `unitname` to decode

        >>> u = Units()
        >>> u.load()
        >>> u.decode('tempsensor', 'temp=45.95;sensor=ok', None)
        (46.0, {'status': 'ok'})
        >>> u.decode('tempsensor', 'temp=45.9;sensor=error', None)
        (None, {'status': 'error'})
        >>> u.decode('date+time', 'time=20:47:01;date=14.12.2019', None)
        (datetime.datetime(2019, 12, 14, 20, 47, 1), None)

        """
        unit = self.get(unitname)
        attrs = None
        if unit and unit.decode:
            value, attrs = unit.decode(valuestr, value)
        return value, attrs

    def load(self):
        """
        Load all predefined units.

        >>> u = Units()
        >>> u.load()
        >>> for unit in u:
        ...     print(unit)
        Unit('temp', icon='mdi:thermometer'), uom='°C')
        Unit('tempsensor', icon='mdi:thermometer'), uom='°C')
        Unit('onoff', icon='mdi:toggle-switch'), uom=None)
        Unit('seconds', icon='mdi:av-timer'), uom='seconds')
        Unit('pressuresensor', icon='mdi:pipe'), uom='bar')
        Unit('date+time', icon=None), uom=None)
        Unit('modes', icon=None), uom=None)
        """
        self.add(Unit('temp', _float1, 'mdi:thermometer', '°C'))
        self.add(Unit('tempsensor', _sensorfab('temp'), 'mdi:thermometer', '°C'))
        self.add(Unit('onoff', None, 'mdi:toggle-switch'))
        self.add(Unit('seconds', _float1, 'mdi:av-timer', 'seconds'))
        self.add(Unit('pressuresensor', _sensorfab('press'), 'mdi:pipe', 'bar'))
        # self.add(Unit('timer', lambda value: value.replace(';-:-', ''), 'mdi:timer'))
        self.add(Unit('date+time', _datetime))
        self.add(Unit('modes', _modes))

    def __iter__(self):
        yield from self._units.values()


def _float1(valuestr, value):
    if value is not None:
        value = float("%.1f" % float(value))
    return value, None


def _sensorfab(name):
    def decode(valuestr, value):
        valuemap = dict(pair.split("=") for pair in valuestr.split(';'))
        status = valuemap.get('sensor')
        if 'ok' == status:
            value = valuemap.get(name)
        else:
            value = None
        if value is not None:
            value = float("%.1f" % float(value))
        return value, {'status': status}
    return decode


def _datetime(valuestr, value):
    valuemap = dict(pair.split("=") for pair in valuestr.split(';'))
    hour, minute, second = valuemap.get('time').split(":")
    day, month, year = valuemap.get('date').split(".")
    stamp = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    return stamp, None


def _modes(valuestr, value):
    valuemap = dict(pair.split("=") for pair in valuestr.split(';'))
    value = "/".join(valuemap.values())
    return value, valuemap

UNITS = Units()
UNITS.load()
