import pathlib

from nose.tools import assert_raises
from nose.tools import eq_

import ebus
from ebus import FieldDef
from ebus import MsgDef
from ebus.types import IntType
from ebus.types import TimeType

from .util import cmp_

TESTDATAPATH = pathlib.Path(__file__).parent / "testdata"


def test_msgdefs0():
    """Message Defs."""
    msgdefs = ebus.MsgDefs()

    # load
    infilepath = TESTDATAPATH / "find0.txt"
    for line in infilepath.read_text().splitlines():
        if line:
            try:
                msgdefs.add(ebus.decode_msgdef(line))
            except ValueError as e:
                pass

    eq_(len(msgdefs), 777)
    eq_(msgdefs.summary(), "777 messages (685 read, 19 update, 231 write) with 1654 fields")

    eq_(msgdefs.get("bai", "foo"), None)
    eq_(msgdefs.get("bar", "foo"), None)

    eq_(len(msgdefs.find("?c")), 132)
    eq_(
        list(msgdefs.find("cc", "StatPowerOn")),
        [MsgDef("cc", "StatPowerOn", (FieldDef(0, "", IntType(0, 65534)),), read=True)],
    )

    with assert_raises(ValueError):
        msgdefs.resolve(["a/"])
    with assert_raises(ValueError):
        msgdefs.resolve(["a/b/c/"])
    with assert_raises(ValueError):
        msgdefs.resolve(["/b/"])

    eq_(
        list(msgdefs.resolve(["*/FlowTempDesired/temp1", "cc/StatPowerOn", "hc/FlowTemp*"])),
        [
            MsgDef("hc", "FlowTempDesired", (FieldDef(0, "temp1", IntType(0, 100, frac=0.5), unit="°C"),), read=True),
            MsgDef("hc", "FlowTempMax", (FieldDef(0, "temp0", IntType(0, 254), unit="°C"),), read=True, write=True),
            MsgDef("hc", "FlowTempMin", (FieldDef(0, "temp0", IntType(0, 254), unit="°C"),), read=True, write=True),
            MsgDef("mc", "FlowTempDesired", (FieldDef(0, "temp1", IntType(0, 100, frac=0.5), unit="°C"),), read=True),
            MsgDef("mc.3", "FlowTempDesired", (FieldDef(0, "temp1", IntType(0, 100, frac=0.5), unit="°C"),), read=True),
            MsgDef("mc.4", "FlowTempDesired", (FieldDef(0, "temp1", IntType(0, 100, frac=0.5), unit="°C"),), read=True),
            MsgDef("mc.5", "FlowTempDesired", (FieldDef(0, "temp1", IntType(0, 100, frac=0.5), unit="°C"),), read=True),
            MsgDef("cc", "StatPowerOn", (FieldDef(0, "", IntType(0, 65534)),), read=True),
        ],
    )
    eq_(list(msgdefs.resolve(["mc.5/Timer.*/foo"])), [])
    eq_(
        list(msgdefs.resolve(["mc.5/Timer.*/to*"])),
        [
            MsgDef(
                "mc.5",
                "Timer.Friday",
                (
                    FieldDef(1, "to.0", TimeType(minres=10)),
                    FieldDef(3, "to.1", TimeType(minres=10)),
                    FieldDef(5, "to.2", TimeType(minres=10)),
                ),
                read=True,
                write=True,
            ),
            MsgDef(
                "mc.5",
                "Timer.Monday",
                (
                    FieldDef(1, "to.0", TimeType(minres=10)),
                    FieldDef(3, "to.1", TimeType(minres=10)),
                    FieldDef(5, "to.2", TimeType(minres=10)),
                ),
                read=True,
                write=True,
            ),
            MsgDef(
                "mc.5",
                "Timer.Saturday",
                (
                    FieldDef(1, "to.0", TimeType(minres=10)),
                    FieldDef(3, "to.1", TimeType(minres=10)),
                    FieldDef(5, "to.2", TimeType(minres=10)),
                ),
                read=True,
                write=True,
            ),
            MsgDef(
                "mc.5",
                "Timer.Sunday",
                (
                    FieldDef(1, "to.0", TimeType(minres=10)),
                    FieldDef(3, "to.1", TimeType(minres=10)),
                    FieldDef(5, "to.2", TimeType(minres=10)),
                ),
                read=True,
                write=True,
            ),
            MsgDef(
                "mc.5",
                "Timer.Thursday",
                (
                    FieldDef(1, "to.0", TimeType(minres=10)),
                    FieldDef(3, "to.1", TimeType(minres=10)),
                    FieldDef(5, "to.2", TimeType(minres=10)),
                ),
                read=True,
                write=True,
            ),
            MsgDef(
                "mc.5",
                "Timer.Tuesday",
                (
                    FieldDef(1, "to.0", TimeType(minres=10)),
                    FieldDef(3, "to.1", TimeType(minres=10)),
                    FieldDef(5, "to.2", TimeType(minres=10)),
                ),
                read=True,
                write=True,
            ),
            MsgDef(
                "mc.5",
                "Timer.Wednesday",
                (
                    FieldDef(1, "to.0", TimeType(minres=10)),
                    FieldDef(3, "to.1", TimeType(minres=10)),
                    FieldDef(5, "to.2", TimeType(minres=10)),
                ),
                read=True,
                write=True,
            ),
        ],
    )
    eq_(
        list(msgdefs.resolve(["mc.5/Timer.Friday#3/to*"])),
        [
            MsgDef(
                "mc.5",
                "Timer.Friday",
                (
                    FieldDef(1, "to.0", TimeType(minres=10)),
                    FieldDef(3, "to.1", TimeType(minres=10)),
                    FieldDef(5, "to.2", TimeType(minres=10)),
                ),
                read=True,
                prio=3,
                write=True,
            )
        ],
    )


def test_msgdefs1():
    """Message Defs."""
    msgdefs = ebus.MsgDefs()

    # load
    infilepath = TESTDATAPATH / "find1.txt"
    for line in infilepath.read_text().splitlines():
        if line:
            try:
                msgdefs.add(ebus.decode_msgdef(line))
            except ValueError as e:
                pass

    eq_(len(msgdefs), 413)
    eq_(msgdefs.summary(), "413 messages (396 read, 12 update, 229 write) with 830 fields")
