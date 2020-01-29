import pathlib

from ebus.messagedefdecoder import decode
from tests.util import cmp_

TESTDATAPATH = pathlib.Path(__file__).parent / "testdata"


def test_find0():
    """Process `find0.txt`."""
    _test('find0')


def test_find1():
    """Process `find1.txt`."""
    _test('find1')


def _test(basename):
    infilepath = TESTDATAPATH / f"{basename}.txt"
    outfilepath = TESTDATAPATH / f"{basename}.decoded.gen.txt"
    reffilepath = TESTDATAPATH / f"{basename}.decoded.txt"
    with outfilepath.open('w') as outfile:
        for line in infilepath.read_text().splitlines():
            if line:
                messagedef = decode(line)
                outfile.write(f"\n{messagedef[:-1]}\n")
                for field in messagedef.fields:
                    outfile.write(f"    {field}\n")
    cmp_(outfilepath, reffilepath)
