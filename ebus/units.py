"""Unit Handling."""
import datetime


class Unit:

    def __init__(self, name, decode, icon=None, uom=None):
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

    def decode(self, unitname, value):
        """
        Decode `value` with `unit`.

        >>> u = Units()
        >>> u.load()
        >>> u.decode('tempok', '45.95;ok')
        46.0
        >>> u.decode('tempok', '45.9;error')
        >>> u.decode('date+time', 'time=20:47:01;date=14.12.2019')
        datetime.datetime(2019, 12, 14, 20, 47, 1)

        """
        unit = self.get(unitname)
        if unit and unit.decode:
            value = unit.decode(value)
        return value

    def load(self):
        """
        Load all predefined units.

        >>> u = Units()
        >>> u.load()
        >>> for unit in u:
        ...     print(unit)
        Unit('temp', icon='mdi:thermometer'), uom='°C')
        Unit('tempok', icon='mdi:thermometer'), uom='°C')
        Unit('onoff', icon='mdi:toggle-switch'), uom=None)
        Unit('seconds', icon='mdi:av-timer'), uom='seconds')
        Unit('pressure', icon='mdi:pipe'), uom='bar')
        Unit('timer', icon='mdi:timer'), uom=None)
        Unit('date+time', icon=None), uom=None)
        """
        self.add(Unit('temp', _decodefloatfab(digits=1), 'mdi:thermometer', '°C'))
        self.add(Unit('tempok', _decodefloatfab(digits=1, checkok=True), 'mdi:thermometer', '°C'))
        self.add(Unit('onoff', None, 'mdi:toggle-switch'))
        self.add(Unit('seconds', int, 'mdi:av-timer', 'seconds'))
        self.add(Unit('pressure', _decodefloatfab(digits=2, checkok=True), 'mdi:pipe', 'bar'))
        self.add(Unit('timer', lambda value: value.replace(';-:-', ''), 'mdi:timer'))
        self.add(Unit('date+time', _decode_datetime))

    def __iter__(self):
        yield from self._units.values()


def _decodefloatfab(digits=None, checkok=False):
    def decode(value):
        parts = value.split(';')
        value = float(parts[0])
        # checkok
        if checkok and 'ok' not in parts:
            value = None
        # digits
        if digits is not None and value is not None:
            value = float(("%%.%df" % digits) % value)
        return value
    return decode


def _decode_datetime(value):
    values = dict(pair.split("=") for pair in value.split(';'))
    hour, minute, second = values.get('time').split(":")
    day, month, year = values.get('date').split(".")
    return datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))


UNITS = Units()
UNITS.load()
