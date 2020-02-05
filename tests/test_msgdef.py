import sys

from nose.tools import eq_

import ebus


def test_msgdef0():
    """MsgDef Example 0"""
    m = ebus.MsgDef("circuit", "name", ("field0",), True, 5, False, False)
    eq_(m.circuit, "circuit")
    eq_(m.name, "name")
    eq_(m.read, True)
    eq_(m.prio, 5)
    eq_(m.write, False)
    eq_(m.update, False)
    eq_(m.fields, ("field0",))
    eq_(m.type_, "r5--")
    eq_(sys.getsizeof(m), 104)
    eq_(str(m), "circuit/name")
    eq_(
        repr(m), "MsgDef('circuit', 'name', ('field0',), read=True, prio=5)",
    )


def test_msgdef1():
    """MsgDef Example 1"""
    m = ebus.MsgDef("circuit", "name", ("field0",), False, None, True, False)
    eq_(m.circuit, "circuit")
    eq_(m.name, "name")
    eq_(m.read, False)
    eq_(m.prio, None)
    eq_(m.write, True)
    eq_(m.update, False)
    eq_(m.fields, ("field0",))
    eq_(m.type_, "--w-")
    eq_(sys.getsizeof(m), 104)
    eq_(str(m), "circuit/name")
    eq_(
        repr(m), "MsgDef('circuit', 'name', ('field0',), write=True)",
    )


def test_msgdef2():
    """MsgDef Example 2"""
    m = ebus.MsgDef("circuit", "name", ("field0",), False, None, False, True)
    eq_(m.circuit, "circuit")
    eq_(m.name, "name")
    eq_(m.read, False)
    eq_(m.prio, None)
    eq_(m.write, False)
    eq_(m.update, True)
    eq_(m.fields, ("field0",))
    eq_(m.type_, "---u")
    eq_(sys.getsizeof(m), 104)
    eq_(str(m), "circuit/name")
    eq_(
        repr(m), "MsgDef('circuit', 'name', ('field0',), update=True)",
    )


def test_fielddef0():
    """FieldDef Example 0."""
    f = ebus.FieldDef("uname", "name", ("uin",), "4", "unit")
    eq_(f.uname, "uname")
    eq_(f.name, "name")
    eq_(f.types, ("uin",))
    eq_(f.dividervalues, "4")
    eq_(f.divider, 4.0)
    eq_(f.values, None)
    eq_(f.unit, "unit")
    eq_(sys.getsizeof(f), 88)
    eq_(str(f), "uname")
    eq_(
        repr(f), "FieldDef('uname', 'name', ('uin',), dividervalues='4', unit='unit')",
    )


def test_fielddef1():
    """FieldDef Example 1."""
    f = ebus.FieldDef("uname", "name", ("uin",), "-4", "unit")
    eq_(f.uname, "uname")
    eq_(f.name, "name")
    eq_(f.types, ("uin",))
    eq_(f.dividervalues, "-4")
    eq_(f.divider, 0.25)
    eq_(f.values, None)
    eq_(f.unit, "unit")
    eq_(sys.getsizeof(f), 88)
    eq_(
        repr(f), "FieldDef('uname', 'name', ('uin',), dividervalues='-4', unit='unit')",
    )


def test_fielddef2():
    """FieldDef Example 2."""
    f = ebus.FieldDef("uname", "name", ("uin",), "0=off;1=on", "unit")
    eq_(f.uname, "uname")
    eq_(f.name, "name")
    eq_(f.types, ("uin",))
    eq_(f.dividervalues, "0=off;1=on")
    eq_(f.divider, None)
    eq_(f.values, {"0": "off", "1": "on"})
    eq_(f.unit, "unit")
    eq_(sys.getsizeof(f), 88)
    eq_(
        repr(f), "FieldDef('uname', 'name', ('uin',), dividervalues='0=off;1=on', unit='unit')",
    )
