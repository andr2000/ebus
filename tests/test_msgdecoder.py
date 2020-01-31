import pathlib
import sys

from nose.tools import eq_

import ebus
from tests.util import cmp_

TESTDATAPATH = pathlib.Path(__file__).parent / "testdata"


def test_listen0a():
    """Process `listen0a.txt`."""
    _test(TESTDATAPATH / "find0.txt", TESTDATAPATH / "listen0a", 161)


def test_listen0b():
    """Process `listen0b.txt`."""
    _test(TESTDATAPATH / "find0.txt", TESTDATAPATH / "listen0b", 161)


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
                    msg = decoder.decode(line)
                    values = tuple(_formatfield(field) for field in msg.fields)
                    outfile.write(f"  {msg.circuit} {msg.msgdef.name} {values}\n")
                except (ebus.UnknownMsgError, ValueError) as err:
                    outfile.write(f"  {err!r}\n")

    # compare
    cmp_(outfilepath, reffilepath)


def _formatfield(field):
    unit = field.fielddef.unit or "" if field.value is not None else ""
    return f"{field.fielddef.uname}={field.value!r}{unit}"
