# -*- coding: utf-8 -*-

"""
Python Client for EBUS daemon.

>>> import ebus

EBUS Message Fields are stored in the Fields container

>>> fields = ebus.Fields()
>>> fields.load()
>>> print(len(fields))
65

The :any:`Decoder` can process ebus output and transform the values

>>> decoder = ebus.Decoder(fields, ebus.UNITS)

>>> for item in decoder.decode('bai Status01 = temp1=27.5;temp1=27.0;temp2=-;temp1=-;temp1=-;pumpstate=off'):
...     print(item)
Value(field=Field(circuit='bai', title='VL', name='Status01', unitname='temp', sub='0', icon=None), circuit='bai', value=27.5)
Value(field=Field(circuit='bai', title='RL', name='Status01', unitname='temp', sub='1', icon=None), circuit='bai', value=27.0)
Value(field=Field(circuit='bai', title='Pump', name='Status01', unitname='onoff', sub='pumpstate', icon=None), circuit='bai', value='off')

>>> for item in decoder.decode('mc.4 Status = temp0=32;onoff=off;temp=35.31;temp0=23'):
...     print(item)
Value(field=Field(circuit='mc', title='Soll', name='Status', unitname='temp', sub='0', icon=None), circuit='mc.4', value=32.0)
Value(field=Field(circuit='mc', title='Ist', name='Status', unitname='temp', sub='2', icon=None), circuit='mc.4', value=35.3)
Value(field=Field(circuit='mc', title='Heizen', name='Status', unitname='onoff', sub='onoff', icon=None), circuit='mc.4', value='off')

>>> for item in decoder.decode('broadcast datetime = outsidetemp=4.500;time=20:47:01;date=14.12.2019'):
...     print(item)
Value(field=Field(... title='OutsideTemp', ...), circuit='broadcast', value=4.5)
Value(field=Field(... title='DateTime', ...), circuit='broadcast', value=datetime.datetime(2019, 12, 14, 20, 47, 1))
"""

__version__ = "0.0.1"
__author__ = "c0fec0de"
__author_email__ = "c0fec0de@gmail.com"
__description__ = """Python Client for EBUS daemon."""
__url__ = "https://github.com/c0fec0de/ebus"

from .circuitmap import CircuitMap  # noqa
from .connection import Connection  # noqa
from .decoder import Decoder  # noqa
from .fields import Field  # noqa
from .fields import Fields  # noqa
from .units import UNITS  # noqa
