"""Message Fields."""
import collections

Field = collections.namedtuple('Field', 'circuit title name unit sub icon')


class Fields:

    """Fields Container."""

    def __init__(self):
        """
        Fields Container.

        >>> fields = Fields()
        >>> fields.add('bai', 'Heating T0', 'Status01', sub='0', unit='temp')
        >>> for field in fields:
        ...     print(field)
        Field(circuit='bai', title='Heating T0', name='Status01', unit='temp', sub='0', icon=None)
        """
        self._fields = collections.defaultdict(lambda: collections.defaultdict(list))

    def add(self, circuit, title, name, unit=None, sub=None, icon=None):
        """
        Add decode Field.

        Args:
            circuit (str): EBUS Circuit name
            title (str): Shown title of the decoded value
            name (str): EBUS Message Name.

        Keyword Args:
            unit (str): Unit name
            sub (str): name or index of the value within message
            icon (str): Icon if different from unit icon.
        """
        field = Field(circuit, title, name, unit, sub, icon)
        self._fields[circuit][name].append(field)

    def get(self, circuit, name=None):
        """Return fields for `name` of `circuit`."""
        if '.' in circuit:
            circuit = circuit.split('.')[0]
        if name:
            return self._fields[circuit][name]
        else:
            return itertools.chain.from_iterable(self._fields[circuit].values())

    def __iter__(self):
        for circuitfields in self._fields.values():
            for fields in circuitfields.values():
                yield from fields

    def __len__(self):
        return sum(sum(len(fields) for fields in circuitfields.values()) for circuitfields in self._fields.values())

    def load(self):
        """Load Fields."""
        # mc Status = temp0=32;onoff=off;temp=35.31;temp0=23
        self.add('mc', 'Vorlauf Soll', 'Status', 'temp', '0')
        self.add('mc', 'Vorlauf Ist', 'Status', 'temp', '2')

        # mc Mode = temp0=23;mcmode=auto;days=0;temp0=0;mcmode=low;mctype7=mixer;daynight=day
        self.add('mc', 'Mode', 'Mode', None, '1')
        self.add('mc', 'Day/Night', 'Mode', None, 'daynight')

        # bai Status01 = temp1=27.5;temp1=27.0;temp2=-;temp1=-;temp1=-;pumpstate=off
        self.add('bai', 'T0', 'Status01', 'temp', '0')
        self.add('bai', 'T1', 'Status01', 'temp', '1')
        self.add('bai', 'Pump', 'Status01', 'onoff', 'pumpstate')
        self.add('hwc', 'Soll', 'Status', 'temp', 'temp0')
        self.add('hwc', 'Ist', 'Status', 'temp', 'temp')
        self.add('hwc', 'Heizen', 'Status', 'onoff', 'onoff')
        # hc SumFlowSensor = temp=29.69;sensor=ok
        self.add('hc', 'SumFlow', 'SumFlowSensor', 'temp', 'temp')
        self.add('hc', 'Outside', 'DateTime', 'temp', 'temp2')
        # broadcast datetime = outsidetemp=4.500;time=20:47:01;date=14.12.2019
        self.add('broadcast', 'OutsideTemp', 'datetime', unit='temp', sub='outsidetemp')
        self.add('broadcast', 'DateTime', 'datetime', unit='date+time')

        self.add('700', 'ActualFlowTemperatureDesired', 'Hc1ActualFlowTempDesired', unit='temp'),
        self.add('700', 'MaxFlowTemperatureDesired', 'Hc1MaxFlowTempDesired', unit='temp'),
        self.add('700', 'MinFlowTemperatureDesired', 'Hc1MinFlowTempDesired', unit='temp'),
        self.add('700', 'PumpStatus', 'Hc1PumpStatus', unit='onoff'),
        self.add('700', 'HCSummerTemperatureLimit', 'Hc1SummerTempLimit', unit='temp', icon='weather-sunny'),
        self.add('700', 'HolidayTemperature', 'HolidayTemp', unit='temp'),
        self.add('700', 'HWTemperatureDesired', 'HwcTempDesired', unit='temp'),
        self.add('700', 'HWTimerMonday', 'hwcTimer.Monday', unit='timer'),
        self.add('700', 'HWTimerTuesday', 'hwcTimer.Tuesday', unit='timer'),
        self.add('700', 'HWTimerWednesday', 'hwcTimer.Wednesday', unit='timer'),
        self.add('700', 'HWTimerThursday', 'hwcTimer.Thursday', unit='timer'),
        self.add('700', 'HWTimerFriday', 'hwcTimer.Friday', unit='timer'),
        self.add('700', 'HWTimerSaturday', 'hwcTimer.Saturday', unit='timer'),
        self.add('700', 'HWTimerSunday', 'hwcTimer.Sunday', unit='timer'),
        self.add('700', 'WaterPressure', 'WaterPressure', unit='pressure'),
        # self.add('700', 'Zone1RoomZoneMapping', 'z1RoomZoneMapping', None, 'mdi:label', 0),
        self.add('700', 'Zone1NightTemperature', 'z1NightTemp', unit='temp', icon='mdi:weather-night'),
        self.add('700', 'Zone1DayTemperature', 'z1DayTemp', unit='temp', icon='weather-sunny'),
        self.add('700', 'Zone1HolidayTemperature', 'z1HolidayTemp', unit='temp'),
        self.add('700', 'Zone1RoomTemperature', 'z1RoomTemp', unit='temp'),
        self.add('700', 'Zone1ActualRoomTemperatureDesired', 'z1ActualRoomTempDesired', unit='temp'),
        self.add('700', 'Zone1TimerMonday', 'z1Timer.Monday', unit='timer'),
        self.add('700', 'Zone1TimerTuesday', 'z1Timer.Tuesday', unit='timer'),
        self.add('700', 'Zone1TimerWednesday', 'z1Timer.Wednesday', unit='timer'),
        self.add('700', 'Zone1TimerThursday', 'z1Timer.Thursday', unit='timer'),
        self.add('700', 'Zone1TimerFriday', 'z1Timer.Friday', unit='timer'),
        self.add('700', 'Zone1TimerSaturday', 'z1Timer.Saturday', unit='timer'),
        self.add('700', 'Zone1TimerSunday', 'z1Timer.Sunday', unit='timer'),
        # self.add('700', 'Zone1OperativeMode', 'z1OpMode', None, 'mdi:math-compass', 3),
        self.add('700', 'ContinuosHeating', 'ContinuosHeating', unit='temp', icon='mdi:weather-snowy'),
        self.add('700', 'PowerEnergyConsumptionLastMonth', 'PrEnergySumHcLastMonth', unit='kwh'),
        self.add('700', 'PowerEnergyConsumptionThisMonth', 'PrEnergySumHcThisMonth', unit='kwh'),
        self.add('ehp', 'HWTemperature', 'HwcTemp', unit='tempok'),
        self.add('ehp', 'OutsideTemp', 'OutsideTemp', unit='tempok'),
        self.add('bai', 'HotWaterTemperature', 'HwcTemp', unit='tempok'),
        self.add('bai', 'StorageTemperature', 'StorageTemp', unit='tempok'),
        self.add('bai', 'DesiredStorageTemperature', 'StorageTempDesired', unit='temp'),
        self.add('bai', 'OutdoorsTemperature', 'OutdoorstempSensor', unit='tempok'),
        self.add('bai', 'WaterPreasure', 'WaterPressure', unit='pressure'),
        self.add('bai', 'AverageIgnitionTime', 'averageIgnitiontime', unit='seconds'),
        self.add('bai', 'MaximumIgnitionTime', 'maxIgnitiontime', unit='seconds'),
        self.add('bai', 'MinimumIgnitionTime', 'minIgnitiontime', unit='seconds'),
        self.add('bai', 'ReturnTemperature', 'ReturnTemp', unit='tempok'),
        self.add('bai', 'CentralHeatingPump', 'WP', unit='onoff'),
        self.add('bai', 'HeatingSwitch', 'HeatingSwitch', unit='onoff'),
        self.add('bai', 'DesiredFlowTemperature', 'FlowTempDesired', unit='temp'),
        self.add('bai', 'FlowTemperature', 'FlowTemp', unit='tempok'),
        self.add('bai', 'Flame', 'Flame', unit='onoff'),
        self.add('bai', 'PowerEnergyConsumptionHeatingCircuit', 'PrEnergySumHc1', unit='kwh'),
        self.add('bai', 'PowerEnergyConsumptionHotWaterCircuit', 'PrEnergySumHwc1', unit='kwh'),
        self.add('bai', 'RoomThermostat', 'DCRoomthermostat', unit='onoff'),
        self.add('bai', 'HeatingPartLoad', 'PartloadHcKW', unit='kwh'),
