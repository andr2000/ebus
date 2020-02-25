import datetime


class Date(datetime.date):

    """:any:`datetime.time` with '%H:%M' string representation."""

    # def __str__(self):
    #     return self.strftime("%d.%m.%Y")


class HourMinute(datetime.time):

    """:any:`datetime.time` with '%H:%M' string representation."""

    def __str__(self):
        return self.strftime("%H:%M")


class HourMinuteSecond(datetime.time):

    """:any:`datetime.time` with '%H:%M:%S' string representation."""

    def __str__(self):
        return self.strftime("%H:%M:%S")
