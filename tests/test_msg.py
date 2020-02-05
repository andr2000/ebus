import sys

from nose.tools import eq_

import ebus


def test_msgdef0():
    """MsgDef Example 0"""
    fielddef = ebus.FieldDef("uname", "name", ("uin",), "4", "unit")
    msgdef = ebus.MsgDef("circuit", "name", (fielddef,), True, 5, False, False)

    fields = (ebus.Field(msgdef, fielddef, "5"),)
    msg = ebus.Msg(msgdef, fields)

    eq_(str(msg), "Msg('name', (Field('uname', '5'),))")
    eq_(str(fields[0]), "circuit/name/uname 5unit")

    eq_(repr(msg), "Msg('name', (Field('uname', '5'),))")
    eq_(repr(fields[0]), "Field('uname', '5')")
