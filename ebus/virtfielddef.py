import datetime

from .msgdef import VirtFieldDef
from .types import DateTimeType
from .types import DateType
from .types import TimeType
from .util import repr_


def iter_virtfielddefs(fielddefs):
    """Iterate over Generic Field Definitions."""
    typeclss = [fielddef.type_.__class__ for fielddef in fielddefs]
    names = [fielddef.name for fielddef in fielddefs]
    if DateType in typeclss and TimeType in typeclss:
        # date and time need to be next to each other
        # Limitation: Just the first pair is found, which should be sufficient
        didx = typeclss.index(DateType)
        tidx = typeclss.index(TimeType)
        if abs(didx - tidx) == 1:
            if "dcfstate" in names:
                sidx = names.index("dcfstate")
                yield VirtFieldDef(
                    f"+{names[didx]}+{names[tidx]}+dcfstate",
                    DateTimeType(),
                    lambda fields: _merge_date_time(fields[didx].value, fields[tidx].value, fields[sidx].value),
                )
            else:
                yield VirtFieldDef(
                    f"+{names[didx]}+{names[tidx]}",
                    DateTimeType(),
                    lambda fields: _merge_date_time(fields[didx].value, fields[tidx].value),
                )
    if len(fielddefs) > 1 and names[-1] == "sensor":
        valuedef = fielddefs[0]
        sensordef = fielddefs[-1]
        yield VirtFieldDef(
            f"+{valuedef.name}+{sensordef.name}",
            valuedef.type_,
            lambda fields: _merge_sensor_status(fields[valuedef.idx].value, fields[sensordef.idx].value),
            unit=valuedef.unit,
        )


def _merge_date_time(date, time, state=None):
    if date is not None and time is not None:
        if state in (None, "valid"):
            return datetime.datetime(date.year, date.month, date.day, time.hour, time.minute, time.second)
        else:
            return state


def _merge_sensor_status(value, sensor):
    if sensor == "ok":
        return value
    else:
        return sensor
