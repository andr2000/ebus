"""Unit Handling."""
import datetime


class Unit:

    def __init__(self, name, decode, icon=None):
        """
        Unit Description.

        Args:
            name (str): Unique Identifier
            decode (callable): Function for decoding

        Keyword Args:
            icon (str): icon to use in hass.
        """
        self._name = name
        self._decode = decode
        self._icon = icon

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
        """Icon."""
        return self._icon

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self.name!r}, icon={self.icon!r})"


class Units:

    def __init__(self):
        """Container for Units."""
        self._units = {}

    def add(self, unit):
        self._units[unit.name] = unit

    def decode(self, unitname, value):
        """
        Decode `value` with `unit`.

        >>> u = Units()
        >>> u.load()
        >>> u.decode('tempok', '45.9;ok')
        45.9
        >>> u.decode('tempok', '45.9;error')
        >>> u.decode('date+time', 'time=20:47:01;date=14.12.2019')
        datetime.datetime(2019, 12, 14, 20, 47, 1)

        """
        unit = self._units.get(unitname, None)
        if unit:
            value = unit.decode(value)
        return value

    def load(self):
        """
        Load all predefined units.

        >>> u = Units()
        >>> u.load()
        >>> for unit in u:
        ...     print(unit)
        Unit('temp', icon='mdi:thermometer')
        Unit('tempok', icon='mdi:thermometer')
        Unit('onoff', icon='mdi:toggle-switch')
        Unit('seconds', icon='mdi:av-timer')
        Unit('pressure', icon='mdi:pipe')
        Unit('timer', icon='mdi:timer')
        Unit('date+time', icon=None)
        """
        self.add(Unit('temp', float, 'mdi:thermometer'))
        self.add(Unit('tempok', _decode_floatok, 'mdi:thermometer'))
        self.add(Unit('onoff', lambda value: True if value == 'on' else False, 'mdi:toggle-switch'))
        self.add(Unit('seconds', float, 'mdi:av-timer'))
        self.add(Unit('pressure', _decode_floatok, 'mdi:pipe'))
        self.add(Unit('timer', lambda value: value.replace(';-:-', ''), 'mdi:timer'))
        self.add(Unit('date+time', _decode_datetime))

    def __iter__(self):
        yield from self._units.values()


def _decode_floatok(value):
    parts = value.split(';')
    if 'ok' in parts:
        return float(parts[0])


def _decode_datetime(value):
    values = dict(pair.split("=") for pair in value.split(';'))
    hour, minute, second = values.get('time').split(":")
    day, month, year = values.get('date').split(".")
    return datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))


UNITS = Units()
UNITS.load()
