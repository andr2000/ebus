"""Message Fields."""
import collections
import itertools

Field = collections.namedtuple('Field', 'circuit title name unitname sub icon')


class Fields:

    """Fields Container."""

    def __init__(self):
        """
        Fields Container.

        >>> fields = Fields()
        >>> fields.add('bai', 'Heating T0', 'Status01', unitname='temp')
        >>> fields.add('hc', 'SumFlow', 'SumFlowSensor', 'temp', 'temp')
        >>> fields.add('hc', 'Outside', 'DateTime', 'temp', 'temp2')
        >>> for field in fields:
        ...     print(field)
        Field(circuit='bai', title='Heating T0', name='Status01', unitname='temp', sub=None, icon=None)
        Field(circuit='hc', title='SumFlow', name='SumFlowSensor', unitname='temp', sub='temp', icon=None)
        Field(circuit='hc', title='Outside', name='DateTime', unitname='temp', sub='temp2', icon=None)
        >>> fields.get('hc', 'SumFlowSensor')
        (Field(circuit='hc', ..., name='SumFlowSensor', ...),)
        >>> fields.get('hc')
        (Field(circuit='hc', ... name='SumFlowSensor', ...), Field(circuit='hc', ... name='DateTime', ...))

        """
        self._fields = collections.defaultdict(lambda: collections.defaultdict(list))

    def add(self, circuit, title, name, unitname=None, sub=None, icon=None):
        """
        Add decode Field.

        Args:
            circuit (str): EBUS Circuit name
            title (str): Shown title of the decoded value
            name (str): EBUS Message Name.

        Keyword Args:
            unitname (str): Unitname name
            sub (str): name or index of the value within message
            icon (str): Icon if different from unitname icon.
        """
        field = Field(circuit, title, name, unitname, sub, icon)
        self._fields[circuit][name].append(field)

    def get(self, circuit, name=None):
        """Return fields for `name` of `circuit`."""
        if '.' in circuit:
            circuit = circuit.split('.')[0]
        if name:
            return tuple(self._fields[circuit][name])
        else:
            return tuple(itertools.chain.from_iterable(self._fields[circuit].values()))

    def __iter__(self):
        for circuitfields in self._fields.values():
            for fields in circuitfields.values():
                yield from fields

    def __len__(self):
        return sum(sum(len(fields) for fields in circuitfields.values()) for circuitfields in self._fields.values())

    def load(self):
        """Load Fields."""

        self.add('scan', None, '')  # ignore

        # mc Status = temp0=32;onoff=off;temp=35.31;temp0=23
        self.add('mc', 'Soll', 'Status', 'temp', '0')
        self.add('mc', 'Ist', 'Status', 'temp', '2')
        self.add('mc', 'Heizen', 'Status', 'onoff', 'onoff')

        # mc Mode = temp0=23;mcmode=auto;days=0;temp0=0;mcmode=low;mctype7=mixer;daynight=day
        self.add('mc', 'Mode', 'Mode', None, '1')
        self.add('mc', 'Day/Night', 'Mode', None, 'daynight')

        # mc RoomTempOffset = temp=0.00
        self.add('mc', 'RoomTempOffset', 'RoomTempOffset', 'temp')

        # bai Status01 = temp1=27.5;temp1=27.0;temp2=-;temp1=-;temp1=-;pumpstate=off
        self.add('bai', 'VL', 'Status01', 'temp', '0')
        self.add('bai', 'RL', 'Status01', 'temp', '1')
        self.add('bai', 'Pump', 'Status01', 'onoff', 'pumpstate')
        self.add('hwc', 'Soll', 'Status', 'temp', 'temp0')
        self.add('hwc', 'Ist', 'Status', 'temp', 'temp')
        self.add('hwc', 'Heizen', 'Status', 'onoff', 'onoff')
        # hc SumFlowSensor = temp=29.69;sensor=ok
        self.add('hc', 'SumFlow', 'SumFlowSensor', 'temp', 'temp')
        self.add('hc', 'Outside', 'DateTime', 'temp', 'temp2')

        self.add('mc', 'OutsideTemp', 'Status16', 'temp')
        # broadcast datetime = outsidetemp=4.500;time=20:47:01;date=14.12.2019
        self.add('broadcast', 'OutsideTemp', 'datetime', unitname='temp', sub='outsidetemp')
        self.add('broadcast', 'DateTime', 'datetime', unitname='date+time')

        self.add('700', 'ActualFlowTemperatureDesired', 'Hc1ActualFlowTempDesired', unitname='temp'),
        self.add('700', 'MaxFlowTemperatureDesired', 'Hc1MaxFlowTempDesired', unitname='temp'),
        self.add('700', 'MinFlowTemperatureDesired', 'Hc1MinFlowTempDesired', unitname='temp'),
        self.add('700', 'PumpStatus', 'Hc1PumpStatus', unitname='onoff'),
        self.add('700', 'HCSummerTemperatureLimit', 'Hc1SummerTempLimit', unitname='temp', icon='weather-sunny'),
        self.add('700', 'HolidayTemperature', 'HolidayTemp', unitname='temp'),
        self.add('700', 'HWTemperatureDesired', 'HwcTempDesired', unitname='temp'),
        self.add('700', 'HWTimerMonday', 'hwcTimer.Monday', unitname='timer'),
        self.add('700', 'HWTimerTuesday', 'hwcTimer.Tuesday', unitname='timer'),
        self.add('700', 'HWTimerWednesday', 'hwcTimer.Wednesday', unitname='timer'),
        self.add('700', 'HWTimerThursday', 'hwcTimer.Thursday', unitname='timer'),
        self.add('700', 'HWTimerFriday', 'hwcTimer.Friday', unitname='timer'),
        self.add('700', 'HWTimerSaturday', 'hwcTimer.Saturday', unitname='timer'),
        self.add('700', 'HWTimerSunday', 'hwcTimer.Sunday', unitname='timer'),
        self.add('700', 'WaterPressure', 'WaterPressure', unitname='pressuresensor'),
        # self.add('700', 'Zone1RoomZoneMapping', 'z1RoomZoneMapping', None, 'mdi:label', 0),
        self.add('700', 'Zone1NightTemperature', 'z1NightTemp', unitname='temp', icon='mdi:weather-night'),
        self.add('700', 'Zone1DayTemperature', 'z1DayTemp', unitname='temp', icon='weather-sunny'),
        self.add('700', 'Zone1HolidayTemperature', 'z1HolidayTemp', unitname='temp'),
        self.add('700', 'Zone1RoomTemperature', 'z1RoomTemp', unitname='temp'),
        self.add('700', 'Zone1ActualRoomTemperatureDesired', 'z1ActualRoomTempDesired', unitname='temp'),
        self.add('700', 'Zone1TimerMonday', 'z1Timer.Monday', unitname='timer'),
        self.add('700', 'Zone1TimerTuesday', 'z1Timer.Tuesday', unitname='timer'),
        self.add('700', 'Zone1TimerWednesday', 'z1Timer.Wednesday', unitname='timer'),
        self.add('700', 'Zone1TimerThursday', 'z1Timer.Thursday', unitname='timer'),
        self.add('700', 'Zone1TimerFriday', 'z1Timer.Friday', unitname='timer'),
        self.add('700', 'Zone1TimerSaturday', 'z1Timer.Saturday', unitname='timer'),
        self.add('700', 'Zone1TimerSunday', 'z1Timer.Sunday', unitname='timer'),
        # self.add('700', 'Zone1OperativeMode', 'z1OpMode', None, 'mdi:math-compass', 3),
        self.add('700', 'ContinuosHeating', 'ContinuosHeating', unitname='temp', icon='mdi:weather-snowy'),
        self.add('700', 'PowerEnergyConsumptionLastMonth', 'PrEnergySumHcLastMonth', unitname='kwh'),
        self.add('700', 'PowerEnergyConsumptionThisMonth', 'PrEnergySumHcThisMonth', unitname='kwh'),

        self.add('ehp', 'HWTemperature', 'HwcTemp', unitname='tempsensor'),
        self.add('ehp', 'OutsideTemp', 'OutsideTemp', unitname='tempsensor'),

        self.add('bai', 'HotWaterTemperature', 'HwcTemp', unitname='tempsensor'),
        self.add('bai', 'StorageTemperature', 'StorageTemp', unitname='tempsensor'),
        self.add('bai', 'DesiredStorageTemperature', 'StorageTempDesired', unitname='temp'),
        self.add('bai', 'OutdoorsTemperature', 'OutdoorstempSensor', unitname='tempsensor'),
        self.add('bai', 'WaterPreasure', 'WaterPressure', unitname='pressuresensor'),
        self.add('bai', 'AverageIgnitionTime', 'averageIgnitiontime', unitname='seconds'),
        self.add('bai', 'MaximumIgnitionTime', 'maxIgnitiontime', unitname='seconds'),
        self.add('bai', 'MinimumIgnitionTime', 'minIgnitiontime', unitname='seconds'),
        self.add('bai', 'ReturnTemperature', 'ReturnTemp', unitname='tempsensor'),
        self.add('bai', 'CentralHeatingPump', 'WP', unitname='onoff'),
        self.add('bai', 'HeatingSwitch', 'HeatingSwitch', unitname='onoff'),
        self.add('bai', 'DesiredFlowTemperature', 'FlowTempDesired', unitname='temp'),
        self.add('bai', 'FlowTemperature', 'FlowTemp', unitname='tempsensor'),
        self.add('bai', 'Flame', 'Flame', unitname='onoff'),
        self.add('bai', 'PowerEnergyConsumptionHeatingCircuit', 'PrEnergySumHc1', unitname='kwh'),
        self.add('bai', 'PowerEnergyConsumptionHotWaterCircuit', 'PrEnergySumHwc1', unitname='kwh'),
        self.add('bai', 'RoomThermostat', 'DCRoomthermostat', unitname='onoff'),
        self.add('bai', 'HeatingPartLoad', 'PartloadHcKW', unitname='kwh'),

        self.add('hwc', 'Circulation', 'CirPump2', unitname='onoff')

        self.add('bai', 'Modes', 'SetMode', unitname='modes')
