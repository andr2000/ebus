import sys

from nose.tools import eq_

import ebus


def test_msgdef():
    m = ebus.MsgDef("circuit", "name", ("field0",), True, None, False, "update")
    eq_(m.circuit, "circuit")
    eq_(m.name, "name")
    eq_(m.read, True)
    eq_(m.prio, None)
    eq_(m.write, False)
    eq_(m.update, "update")
    eq_(m.fields, ("field0",))
    eq_(sys.getsizeof(m), 104)
    eq_(
        repr(m), "MsgDef('circuit', 'name', ('field0',), read=True, update='update')",
    )


def test_fielddef():
    """FieldDef."""
    f = ebus.FieldDef("uname", "name", ("typ",), "4", "unit")
    eq_(f.uname, "uname")
    eq_(f.name, "name")
    eq_(f.types, ("typ",))
    eq_(f.dividervalues, "4")
    eq_(f.unit, "unit")
    eq_(sys.getsizeof(f), 88)
    eq_(
        repr(f), "FieldDef('uname', 'name', ('typ',), dividervalues='4', unit='unit')",
    )
