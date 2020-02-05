import pathlib

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
