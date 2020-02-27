import datetime

from .util import repr_


class NotAvailable:
    def __repr__(self):
        return repr_(self)


class Type:
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

    def decode(self, fielddef, value):
        if fielddef.values is None:
            try:
                value = fielddef.type_._decode(fielddef, value)
            except ValueError as e:
                value = ValueError(str(e))
        return value

    def _decode(self, fielddef, value):
        raise NotImplementedError(self)


class StrType(Type):
    def __init__(self, length=None):
        self._length = length

    @property
    def length(self):
        """Width."""
        return self._length

    def _getkwargs(self):
        return (("length", self.length, None),)

    def _decode(self, fielddef, value):
        return value


class HexType(Type):
    def __init__(self, length=None):
        self._length = length

    @property
    def length(self):
        """Width."""
        return self._length

    def _getkwargs(self):
        return (("length", self.length, None),)

    def _decode(self, fielddef, value):
        values = value.split(" ")
        if self.length:
            if len(values) != self.length:
                raise ValueError(f"Hex value {value} has not expected length of {self.length}")
        return tuple(Hex(int(value, 16)) for value in values)


class IntType(Type):
    def __init__(self, min_, max_, frac=None):
        self._min = min_
        self._max = max_
        self._frac = frac

    @property
    def min_(self):
        return self._min

    @property
    def max_(self):
        return self._max

    @property
    def frac(self):
        return self._frac

    def _getargs(self):
        return (self.min_, self.max_)

    def _getkwargs(self):
        return (("frac", self.frac, None),)

    def _decode(self, fielddef, value):
        if value != "-":
            if fielddef.dividervalues or self.frac is not None:
                return float(value)
            else:
                return int(value)
        else:
            return None


class BoolType(Type):
    def _decode(self, fielddef, value):
        if value != "-":
            return bool(int(value))
        else:
            return None


class FloatType(Type):
    def _decode(self, fielddef, value):
        if value != "-":
            return float(value)
        else:
            return None


class DateType(Type):
    def _decode(self, fielddef, value):
        if value != "-.-.-":
            return datetime.datetime.strptime(value, "%d.%m.%Y").date()
        else:
            return None


class TimeType(Type):
    def __init__(self, minres=None, nosecond=False):
        self._minres = minres
        self._nosecond = nosecond

    @property
    def minres(self):
        """Minute Resolution."""
        return self._minres

    @property
    def nosecond(self):
        return self._nosecond

    def _getkwargs(self):
        return (("minres", self._minres, None),)

    def _decode(self, fielddef, value):
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


class WeekdayType(Type):

    pass
    # def _decode(self, fielddef, value):
    #     # TODO
    #     return value


class PinType(Type):
    def __init__(self, length=None):
        self._length = length

    @property
    def length(self):
        """Width."""
        return self._length

    def _getkwargs(self):
        return (("length", self.length, None),)

    # def _decode(self, fielddef, value):
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
    "PIN": PinType(4),
    # UCH       unsigned integer              0...254
    "UCH": IntType(0, 254),
    # SCH       signed integer               -127...127
    # D1B       signed integer               -127...127
    "SCH": IntType(-127, 127),
    "D1B": IntType(-127, 127),
    # D1C       unsigned number               0.0...100.0              fraction 1/2 = divisor 2
    "D1C": IntType(0, 100, frac=1.0 / 2),
    # D2B       signed number                -127.99...127.99          fraction 1/256 = divisor 256
    "D2B": IntType(-127.99, 127.99, frac=1.0 / 256),
    # D2C       signed number                -2047.9...2047.9          fraction 1/16 = divisor 16
    "D2C": IntType(-2047.9, 2047.9, frac=1.0 / 16),
    # FLT       signed number                -32.767...32.767         low byte first, fraction 1/1000 = divisor 1000
    # FLR       signed number reverse        -32.767...32.767         high byte first, fraction 1/1000 = divisor 1000
    "FLT": IntType(-32.767, 32.767, frac=1.0 / 1000),
    "FLR": IntType(-32.767, 32.767, frac=1.0 / 1000),
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


def gettype(name):
    """Get Type for Name."""
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
        # BI0       bit 0                         0...1
        # BI1       bit 1                         0...1
        # BI2       bit 2                         0...1
        # BI3       bit 3                         0...1
        # BI4       bit 4                         0...1
        # BI5       bit 5                         0...1
        # BI6       bit 6                         0...1
        # BI7       bit 7                         0...1
        if name.startswith(("BI0:", "BI1:", "BI2:", "BI3:", "BI4:", "BI5:", "BI6:", "BI7:")):
            TYPEMAP[name] = BoolType()
    return TYPEMAP[name]


class Time(datetime.time):

    """:any:`datetime.time` with '%H:%M:%S' string representation."""

    def __str__(self):
        return self.strftime("%H:%M:%S")


class ShortTime(datetime.time):

    """:any:`datetime.time` with '%H:%M' string representation."""

    def __str__(self):
        return self.strftime("%H:%M")


class Hex(int):
    def __repr__(self):
        value = int(self)
        return f"0x{self:02X}"

    __str__ = __repr__
