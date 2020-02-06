import pathlib

from nose.tools import assert_raises
from nose.tools import eq_

import ebus

from .util import cmp_

TESTDATAPATH = pathlib.Path(__file__).parent / "testdata"


def test_msgdefs():
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

    eq_(len(msgdefs), 699)
    eq_(msgdefs.get_info(), "699 message definitions found (688 read, 11 update, 4 write)")

    eq_(msgdefs.get("bai", "foo"), None)
    eq_(msgdefs.get("bar", "foo"), None)

    eq_(len(tuple(msgdefs.find("?c"))), 110)
    eq_(
        list(msgdefs.find("cc", "StatPowerOn")),
        [ebus.MsgDef("cc", "StatPowerOn", (ebus.FieldDef("", "", ("UIN",)),), read=True)],
    )

    with assert_raises(ValueError):
        tuple(msgdefs.resolve("a/"))
    with assert_raises(ValueError):
        tuple(msgdefs.resolve("a/b/c/"))
    with assert_raises(ValueError):
        tuple(msgdefs.resolve("/b/"))

    eq_(
        list(msgdefs.resolve("*/FlowTempDesired/temp1;cc/StatPowerOn;hc/FlowTemp*")),
        [
            ebus.MsgDef("bai", "FlowTempDesired", (), read=True),
            ebus.MsgDef("hc", "FlowTempDesired", (ebus.FieldDef("temp1", "temp1", ("D1C",), unit="°C"),), read=True),
            ebus.MsgDef("mc", "FlowTempDesired", (ebus.FieldDef("temp1", "temp1", ("D1C",), unit="°C"),), read=True),
            ebus.MsgDef("mc.3", "FlowTempDesired", (ebus.FieldDef("temp1", "temp1", ("D1C",), unit="°C"),), read=True),
            ebus.MsgDef("mc.4", "FlowTempDesired", (ebus.FieldDef("temp1", "temp1", ("D1C",), unit="°C"),), read=True),
            ebus.MsgDef("mc.5", "FlowTempDesired", (ebus.FieldDef("temp1", "temp1", ("D1C",), unit="°C"),), read=True),
            ebus.MsgDef("ui", "FlowTempDesired", (), read=True),
            ebus.MsgDef("cc", "StatPowerOn", (ebus.FieldDef("", "", ("UIN",)),), read=True),
            ebus.MsgDef("hc", "FlowTempMax", (ebus.FieldDef("temp0", "temp0", ("UCH",), unit="°C"),), read=True),
            ebus.MsgDef("hc", "FlowTempMin", (ebus.FieldDef("temp0", "temp0", ("UCH",), unit="°C"),), read=True),
        ],
    )
