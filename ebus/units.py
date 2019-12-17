"""Unit Handling."""
import datetime
import collections


class Unit:

    def __init__(self, name, decode, icon=None):
        self._name = name
        self._decode = decode
        self._icon = icon

    @property
    def name(self):
        """Name."""
        return self._name

    @property
    def decode(self):
        """Decode."""
        return self._decode

    @property
    def icon(self):
        """Icon."""
        return self._icon


class Units:
    """Container for Units."""

    def __init__(self):
        """Container for Units."""
        self._units = {}

    def _add(self, unit):
        self._units[unit.name] = unit

    def decode(self, unit, value):
        """Decode `value` with `unit`."""
        unit = self._units.get(unit, None)
        if unit:
            value = unit.decode(value)
        return value

    def load(self):
        self._add(Unit('temp', float, 'mdi:thermometer'))
        self._add(Unit('tempok', _decode_floatok, 'mdi:thermometer'))
        self._add(Unit('onoff', lambda value: True if value == 'on' else False, 'mdi:toggle-switch'))
        self._add(DateTimeUnit())
        self._add(Unit('seconds', float, 'mdi:av-timer'))
        self._add(Unit('pressure', _decode_floatok, 'mdi:pipe'))
        self._add(Unit('timer', lambda value: value.replace(';-:-', ''), 'mdi:timer'))


def _decode_floatok(value):
    parts = value.split(';')
    if 'ok' in parts:
        return parts[0]


class DateTimeUnit(Unit):

    def __init__(self):
        """
        Date and Time

        >>> dtu = DateTimeUnit()
        >>> dtu.decode('time=20:47:01;date=14.12.2019')
        datetime.datetime(2019, 12, 14, 20, 47, 1)
        """
        super().__init__('date+time', DateTimeUnit._decode)

    @staticmethod
    def _decode(value):
        values = dict(pair.split("=") for pair in value.split(';'))
        hour, minute, second = values.get('time').split(":")
        day, month, year = values.get('date').split(".")
        return datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

UNITS = Units()
UNITS.load()
