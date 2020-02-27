import datetime
import re

from .util import repr_

_RE_BIT = re.compile(r"\ABI\d(:(\d))?\Z")


class Type:
    def __init__(self):
        """Abstract Type."""
        pass

    def __repr__(self):
        return repr_(self, self._getargs(), self._getkwargs())

    def __ident(self):
        return self._getargs(), self._getkwargs()

    def __hash__(self):
        return hash(self.__ident())

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.__ident() == other.__ident()
        else:
            return NotImplemented

    def __ne__(self, other):
        if self.__class__ is other.__class__:
            return self.__ident() != other.__ident()
        else:
            return NotImplemented

    def _getargs(self):
        return ()

    def _getkwargs(self):
        return ()

    def with_divider(self, divider):
        """Return copy and apply `divider`."""
        raise NotImplementedError(self)

    def decode(self, value):
        """Decode `value`."""
        try:
            value = self._decode(value)
        except ValueError as e:
            value = ValueError(str(e))
        return value

    def _decode(self, value):
        raise NotImplementedError(self)


class EnumType(Type):
    def __init__(self, values):
        """Enumeration of `values`."""
        self._values = values

    @property
    def values(self):
        """Enumeration Values."""
        return self._values

    def _getargs(self):
        return (self._values,)

    def _decode(self, value):
        return value


class StrType(Type):
    def __init__(self, length=None):
        """String with maximum `length`."""
        self._length = length

    @property
    def length(self):
        """Length."""
        return self._length

    def _getkwargs(self):
        return (("length", self.length, None),)

    def _decode(self, value):
        return value


class HexType(Type):
    def __init__(self, length=None):
        """`length` number of Hex Bytes."""
        self._length = length

    @property
    def length(self):
        """Width."""
        return self._length

    def _getkwargs(self):
        return (("length", self.length, None),)

    def _decode(self, value):
        values = value.split(" ")
        if self.length:
            if len(values) != self.length:
                raise ValueError(f"Hex value {value} has not expected length of {self.length}")
        return tuple(Hex(int(value, 16)) for value in values)


class IntType(Type):
    def __init__(self, min_, max_, divider=None):
        """Integer in the range of [min_, max_] with granularity of `1 / divider`."""
        self._min = min_
        self._max = max_
        self._divider = divider

    @property
    def min_(self):
        """Lower Limit."""
        return self._min

    @property
    def max_(self):
        """Upper Limit."""
        return self._max

    @property
    def divider(self):
        """Divider."""
        return self._divider

    def _getargs(self):
        return (self.min_, self.max_)

    def _getkwargs(self):
        return (("divider", self.divider, None),)

    def with_divider(self, divider):
        """Return copy and apply `divider`."""
        divider = _try_int(divider * (self.divider or 1))
        min_ = _try_int(self.min_ / divider)
        max_ = _try_int(self.max_ / divider)
        return IntType(min_, max_, divider=divider)

    def _decode(self, value):
        if value != "-":
            if self.divider and self.divider > 0:
                return float(value)
            else:
                return int(value)
        else:
            return None


class BoolType(Type):
    def __init__(self):
        """Boolean Type."""
        pass

    def _decode(self, value):
        if value != "-":
            return bool(int(value))
        else:
            return None


class FloatType(Type):
    def __init__(self):
        """Floating Type."""
        pass

    def _decode(self, value):
        if value != "-":
            return float(value)
        else:
            return None


class DateType(Type):
    def __init__(self):
        """Date Type."""
        pass

    def _decode(self, value):
        if value != "-.-.-":
            return datetime.datetime.strptime(value, "%d.%m.%Y").date()
        else:
            return None


class TimeType(Type):
    def __init__(self, minres=None, nosecond=False):
        """
        Time.

        Keyword Args:
            minres: Minute Resolution
            nosecond: Skip second
        """
        self._minres = minres
        self._nosecond = nosecond

    @property
    def minres(self):
        """Minute Resolution."""
        return self._minres

    @property
    def nosecond(self):
        """Skip Second."""
        return self._nosecond

    def _getkwargs(self):
        return (("minres", self._minres, None),)

    def _decode(self, value):
        if self.nosecond:
            if value != "-:-":
                dt = datetime.datetime.strptime(value, "%H:%M")
                return ShortTime(dt.hour, dt.minute)
            else:
                return None
        else:
            if value != "-:-:-":
                dt = datetime.datetime.strptime(value, "%H:%M:%S")
                return ShortTime(dt.hour, dt.minute, dt.second)
            else:
                return None


class DateTimeType(Type):
    def __init__(self):
        """Date Time."""
        pass


class WeekdayType(Type):
    def __init__(self):
        """Weekday Type."""
        pass

    # def _decode(self, value):
    #     # TODO
    #     return value


class PinType(Type):
    def __init__(self):
        """Pin."""

    # def _decode(self, value):
    #     # TODO
    #     return value


TYPEMAP = {
    # BDA       BCD date                      dd.mm.yyyy               day first, including weekday, Sunday=0x06
    # BDA:3     BCD date                      dd.mm.yyyy               day first, excluding weekday
    # HDA       hex date                      dd.mm.yyyy               day first, including weekday, Sunday=0x07
    # HDA:3     hex date                      dd.mm.yyyy               day first, excluding weekday
    "BDA": DateType(),
    "BDA:3": DateType(),
    "HDA": DateType(),
    "HDA:3": DateType(),
    # DAY       date in days                  dd.mm.yyyy               days since 01.01.1900
    # BTI       BCD time                      hh:mm:ss                 seconds first
    # HTI       hex time                      hh:mm:ss                 hours first
    # VTI       hex time                      hh:mm:ss                 seconds first
    "BTI": TimeType(),
    "HTI": TimeType(),
    "VTI": TimeType(),
    # BTM       BCD time                      hh:mm                    minutes first
    # HTM       hex time                      hh:mm                    hours first
    # VTM       hex time                      hh:mm                    minutes first
    # MIN       time in minutes               hh:mm                    minutes since last midnight
    # TTM       truncated time                hh:m0                    multiple of 10 minutes
    # TTH       truncated time                hh:m0                    multiple of 30 minutes
    # TTQ       truncated time                hh:mm                    multiple of 15 minutes
    "BTM": TimeType(nosecond=True),
    "HTM": TimeType(nosecond=True),
    "VTM": TimeType(nosecond=True),
    "MIN": TimeType(nosecond=True),
    "TTM": TimeType(minres=10, nosecond=True),
    "TTH": TimeType(minres=30, nosecond=True),
    "TTQ": TimeType(minres=15, nosecond=True),
    # BDY       weekday                       Mon...Sun                Sunday=0x06
    # HDY       weekday                       Mon...Sun                Sunday=0x07
    "BDY": WeekdayType(),
    "HDY": WeekdayType(),
    # BCD       unsigned BCD                  0...99
    # BCD:2     unsigned BCD                  0...9999
    # BCD:3     unsigned BCD                  0...999999
    # BCD:4     unsigned BCD                  0...99999999
    "BCD": IntType(0, 99),
    "BCD:2": IntType(0, 9999),
    "BCD:3": IntType(0, 999999),
    "BCD:4": IntType(0, 99999999),
    # TODO: HCD       unsigned hex BCD              0...99999999             each BCD byte converted to hex
    # TODO: HCD:1     unsigned hex BCD              0...99                   each BCD byte converted to hex
    # TODO: HCD:2     unsigned hex BCD              0...9999                 each BCD byte converted to hex
    # TODO: HCD:3     unsigned hex BCD              0...999999               each BCD byte converted to hex
    # PIN       unsigned BCD                  0000...9999
    "PIN": PinType(),
    # UCH       unsigned integer              0...254
    "UCH": IntType(0, 254),
    # SCH       signed integer               -127...127
    # D1B       signed integer               -127...127
    "SCH": IntType(-127, 127),
    "D1B": IntType(-127, 127),
    # D1C       unsigned number               0.0...100.0              fraction 1/2 = divisor 2
    "D1C": IntType(0, 100, divider=2),
    # D2B       signed number                -127.99...127.99          fraction 1/256 = divisor 256
    "D2B": IntType(-127.99, 127.99, divider=256),
    # D2C       signed number                -2047.9...2047.9          fraction 1/16 = divisor 16
    "D2C": IntType(-2047.9, 2047.9, divider=16),
    # FLT       signed number                -32.767...32.767         low byte first, fraction 1/1000 = divisor 1000
    # FLR       signed number reverse        -32.767...32.767         high byte first, fraction 1/1000 = divisor 1000
    "FLT": IntType(-32.767, 32.767, divider=1000),
    "FLR": IntType(-32.767, 32.767, divider=1000),
    # EXP       signed float number          -3.0e38...3.0e38          low byte first
    # EXR       signed float number reverse  -3.0e38...3.0e38          high byte first
    "EXP": FloatType(),
    "EXR": FloatType(),
    # UIN       unsigned integer              0...65534                low byte first
    # UIR       unsigned integer reverse      0...65534                high byte first
    "UIN": IntType(0, 65534),
    "UIR": IntType(0, 65534),
    # SIN       signed integer               -32767...32767            low byte first
    # SIR       signed integer reverse       -32767...32767            high byte first
    "SIN": IntType(-32767, 32767),
    "SIR": IntType(-32767, 32767),
    # U3N       unsigned 3 byte int           0...16777214             low byte first
    # U3R       unsigned 3 byte int reverse   0...16777214             high byte first
    "U3N": IntType(0, 16777214),
    "U3R": IntType(0, 16777214),
    # S3N       signed 3 byte int            -8388607...8388607        low byte first
    # S3R       signed 3 byte int reverse    -8388607...8388607        high byte first
    "S3N": IntType(-8388607, 8388607),
    "S3R": IntType(-8388607, 8388607),
    # ULG       unsigned integer              0...4294967294           low byte first
    # ULR       unsigned integer reverse      0...4294967294           high byte first
    "ULG": IntType(0, 4294967294),
    "ULR": IntType(0, 4294967294),
    # SLG       signed integer               -2147483647...2147483647  low byte first
    # SLR       signed integer reverse       -2147483647...2147483647  high byte first
    "SLG": IntType(-2147483647, 2147483647),
    "SLR": IntType(-2147483647, 2147483647),
}


def gettype(name, divider=None):
    """Get :any:`Type` instance for `name` with `divider`."""
    # create missing types
    if name not in TYPEMAP:
        # STR       character string              Hello
        # NTS       character string              Hello
        if name.startswith(("STR:", "NTS:")):
            len_ = name.split(":")[1]
            if len_ != "*":
                TYPEMAP[name] = StrType(int(len_))
            else:
                TYPEMAP[name] = StrType()
        # HEX       hex digit string              hex octet sep by space
        if name.startswith("HEX:"):
            len_ = name.split(":")[1]
            if len_ != "*":
                TYPEMAP[name] = HexType(int(len_))
            else:
                TYPEMAP[name] = HexType()
        # BI0:7     bit 0                         0...1
        m = _RE_BIT.match(name)
        if m:
            width = int(m.groups()[1])
            if width > 1:
                TYPEMAP[name] = IntType(0, 2 ** width - 1)
            else:
                TYPEMAP[name] = BoolType()
    # get type
    type_ = TYPEMAP[name]
    # divider
    if divider:
        type_ = type_.with_divider(divider)
    return type_


class Time(datetime.time):

    """Time."""

    def __str__(self):
        return self.strftime("%H:%M:%S")


class ShortTime(datetime.time):

    """Time without Seconds."""

    def __str__(self):
        return self.strftime("%H:%M")


class Hex(int):

    """Integer with Hex Representation."""

    def __repr__(self):
        value = int(self)
        return f"0x{self:02X}"

    __str__ = __repr__


def _try_int(value):
    intvalue = int(value)
    if float(value) == float(intvalue):
        value = intvalue
    return value
