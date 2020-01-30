import pathlib

import ebus
from tests.util import cmp_

TESTDATAPATH = pathlib.Path(__file__).parent / "testdata"


def test_find0():
    """Process `find0.txt`."""
    _test(TESTDATAPATH / 'find0')


def test_find1():
    """Process `find1.txt`."""
    _test(TESTDATAPATH / 'find1')


def _test(basepath):
    infilepath = basepath.with_suffix(".txt")
    outfilepath = basepath.with_suffix(".decoded.gen.txt")
    reffilepath = basepath.with_suffix(".decoded.txt")
    with outfilepath.open('w') as outfile:
        for line in infilepath.read_text().splitlines():
            if line:
                try:
                    msgdef = ebus.decode_msgdef(line)
                    outfile.write(f"\n{msgdef[:-1]}\n")
                    for field in msgdef.fields:
                        outfile.write(f"    {field}\n")
                except ValueError as e:
                    outfile.write(f"{e}\n")
    cmp_(outfilepath, reffilepath)
