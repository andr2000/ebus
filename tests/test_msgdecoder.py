import pathlib
import sys

from nose.tools import eq_

import ebus

from .util import cmp_

TESTDATAPATH = pathlib.Path(__file__).parent / "testdata"


def test_listen0a():
    """Process `listen0a.txt`."""
    _test(TESTDATAPATH / "find0.txt", TESTDATAPATH / "listen0a", 699)


def test_listen0b():
    """Process `listen0b.txt`."""
    _test(TESTDATAPATH / "find0.txt", TESTDATAPATH / "listen0b", 699)


def _test(deffilepath, basepath, num):
    infilepath = basepath.with_suffix(".txt")
    outfilepath = basepath.with_suffix(".decoded.gen.txt")
    reffilepath = basepath.with_suffix(".decoded.txt")

    # load definitions
    msgdefs = ebus.MsgDefs()
    for line in deffilepath.read_text().splitlines():
        if line:
            try:
                msgdefs.add(ebus.decode_msgdef(line))
            except ValueError as e:
                print(e)

    eq_(len(msgdefs), num)

    # decode
    decoder = ebus.MsgDecoder(msgdefs)
    with outfilepath.open("w") as outfile:
        for line in infilepath.read_text().splitlines():
            if line:
                try:
                    outfile.write(f"\n{line}\n")
                    msg = decoder.decode_line(line)
                    if msg:
                        values = tuple(f"{field.fielddef.name}={field.unitvalue!r}" for field in msg.fields)
                        outfile.write(f"  {msg.msgdef.circuit} {msg.msgdef.name} {values}\n")
                except (ebus.UnknownMsgError, ValueError) as err:
                    outfile.write(f"  {err!r}\n")

    # compare
    cmp_(outfilepath, reffilepath)
