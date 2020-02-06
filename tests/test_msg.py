import sys

from nose.tools import eq_

import ebus


def test_msgdef0():
    """MsgDef Example 0"""
    fielddef = ebus.FieldDef("uname", "name", ("uin",), "4", "unit")
    msgdef = ebus.MsgDef("circuit", "name", (fielddef,), True, 5, False, False)

    fields = (ebus.Field(fielddef, "5"),)
    msg = ebus.Msg(msgdef, fields)

    eq_(repr(msg), "Msg('name', (Field('uname', '5'),))")
    eq_(repr(fields[0]), "Field('uname', '5')")


def test_filter_msg():
    """Message Filtering."""
    fielddef0 = ebus.FieldDef("uname.0", "name", ("uin",), "4", "unit")
    fielddef1 = ebus.FieldDef("uname.1", "name", ("uin",), "4", "unit")
    fielddef5 = ebus.FieldDef("uname", "name", ("uin",), "4", "unit")
    msgdef01 = ebus.MsgDef("circuit0", "name", (fielddef0, fielddef1), True, 5, False, False)
    msgdef0 = ebus.MsgDef("circuit0", "name", (fielddef0,), True, 5, False, False)
    msgdef5 = ebus.MsgDef("circuit5", "name", (fielddef5,), True, 5, False, False)

    field0 = ebus.Field(fielddef0, "4")
    field1 = ebus.Field(fielddef1, "5")
    field5 = ebus.Field(fielddef5, "5")
    msg01 = ebus.Msg(msgdef01, (field0, field1))
    msg0 = ebus.Msg(msgdef0, (field0,))
    msg5 = ebus.Msg(msgdef5, (field5,))

    eq_(ebus.msg.filter_msg(msg5, [msgdef01]), None)  # not in
    eq_(ebus.msg.filter_msg(msg01, [msgdef5, msgdef01]), msg01)  # in
    eq_(ebus.msg.filter_msg(msg01, [msgdef5, msgdef0]), msg0)  # strip
