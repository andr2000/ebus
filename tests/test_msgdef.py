import sys

from nose.tools import eq_

import ebus


def test_msgdef0():
    """MsgDef Example 0"""
    m = ebus.MsgDef("circuit", "name", (), True, 5, False, False)
    eq_(m.circuit, "circuit")
    eq_(m.name, "name")
    eq_(m.read, True)
    eq_(m.prio, 5)
    eq_(m.write, False)
    eq_(m.update, False)
    eq_(m.children, ())
    eq_(m.type_, "r5--")
    eq_(m.ident, "circuit/name")
    eq_(sys.getsizeof(m), 104)
    eq_(
        repr(m), "MsgDef('circuit', 'name', (), read=True, prio=5)",
    )


def test_msgdef1():
    """MsgDef Example 1"""
    m = ebus.MsgDef("circuit", "name", (), False, None, True, False)
    eq_(m.circuit, "circuit")
    eq_(m.name, "name")
    eq_(m.read, False)
    eq_(m.prio, None)
    eq_(m.write, True)
    eq_(m.update, False)
    eq_(m.children, ())
    eq_(m.type_, "--w-")
    eq_(m.ident, "circuit/name")
    eq_(sys.getsizeof(m), 104)
    eq_(
        repr(m), "MsgDef('circuit', 'name', (), write=True)",
    )


def test_msgdef2():
    """MsgDef Example 2"""
    m = ebus.MsgDef("circuit", "name", (), False, None, False, True)
    eq_(m.circuit, "circuit")
    eq_(m.name, "name")
    eq_(m.read, False)
    eq_(m.prio, None)
    eq_(m.write, False)
    eq_(m.update, True)
    eq_(m.children, ())
    eq_(m.type_, "---u")
    eq_(m.ident, "circuit/name")
    eq_(sys.getsizeof(m), 104)
    eq_(
        repr(m), "MsgDef('circuit', 'name', (), update=True)",
    )


def test_fielddef0():
    """FieldDef Example 0."""
    f = ebus.FieldDef(0, "name", "ename", ("uin",), "4", "unit")
    m = ebus.MsgDef("circuit", "name", (f,), False, None, False, True)
    eq_(f.name, "name")
    eq_(f.ename, "ename")
    eq_(f.types, ("uin",))
    eq_(f.dividervalues, "4")
    eq_(f.divider, 4.0)
    eq_(f.values, None)
    eq_(f.unit, "unit")
    eq_(f.ident, "circuit/name/name")
    eq_(sys.getsizeof(f), 112)
    eq_(
        repr(f), "FieldDef(0, 'name', 'ename', ('uin',), dividervalues='4', unit='unit')",
    )


def test_fielddef1():
    """FieldDef Example 1."""
    f = ebus.FieldDef(0, "name", "ename", ("uin",), "-4", "unit")
    eq_(f.name, "name")
    eq_(f.ename, "ename")
    eq_(f.types, ("uin",))
    eq_(f.dividervalues, "-4")
    eq_(f.divider, 0.25)
    eq_(f.values, None)
    eq_(f.unit, "unit")
    eq_(f.ident, None)
    eq_(sys.getsizeof(f), 112)
    eq_(
        repr(f), "FieldDef(0, 'name', 'ename', ('uin',), dividervalues='-4', unit='unit')",
    )


def test_fielddef2():
    """FieldDef Example 2."""
    f = ebus.FieldDef(0, "name", "ename", ("uin",), "0=off;1=on", "unit")
    eq_(f.name, "name")
    eq_(f.ename, "ename")
    eq_(f.types, ("uin",))
    eq_(f.dividervalues, "0=off;1=on")
    eq_(f.divider, None)
    eq_(f.values, {"0": "off", "1": "on"})
    eq_(f.unit, "unit")
    eq_(f.ident, None)
    eq_(sys.getsizeof(f), 112)
    eq_(
        repr(f), "FieldDef(0, 'name', 'ename', ('uin',), dividervalues='0=off;1=on', unit='unit')",
    )


def test_eq():
    """Test EQ."""
    f0 = ebus.FieldDef(0, "name", "ename", ("uin",), "0=off;1=on", "unit")
    f1 = ebus.FieldDef(0, "name", "ename", ("uin",), "0=off;1=on", "unit")
    g1 = ebus.FieldDef(1, "name", "ename", ("uin",), "0=off;1=on", "unit")
    eq_(f0, f1)

    m0 = ebus.MsgDef("circuit", "name", (f0,), False, None, False, True)
    m1 = ebus.MsgDef("circuit", "name", (f1,), False, None, False, True)
    n1 = ebus.MsgDef("circuit", "name", (g1,), True, None, False, True)
    eq_(m0 == m1, True)
    eq_(m0 == n1, False)
    eq_(m0 == None, False)
    eq_(hash(m0) == hash(m1), True)
    eq_(hash(m0) == hash(n1), False)


def test_hash():
    """Test Hash."""
    f0 = ebus.FieldDef(0, "name", "ename", ("uin",), "0=off;1=on", "unit")
    f1 = ebus.FieldDef(0, "name", "ename", ("uin",), "0=off;1=on", "unit")
    eq_(hash(f0), hash(f1))
