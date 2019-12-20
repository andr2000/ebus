import ebus
from nose.tools import eq_
import pathlib
from tests.util import cmp_

TESTDATAPATH = pathlib.Path(__file__).parent / "testdata"


def test_examples():
    fields = ebus.Fields()
    fields.load()
    decoder = ebus.Decoder(fields, ebus.UNITS)
    outputtxt = TESTDATAPATH / "output.txt"
    outfilepath = TESTDATAPATH / "decode.gen.txt"
    reffilepath = TESTDATAPATH / "decode.txt"
    with outfilepath.open('w') as outfile:
        for line in outputtxt.read_text().splitlines():
            if line:
                try:
                    outfile.write(f"{line}\n")
                    for value in decoder.decode(line):
                        outfile.write(f"  {value.circuit} {value.field.title} {value.value}\n")
                except (ValueError, ebus.decoder.UnknownError) as err:
                    outfile.write(f"  ERROR: {err}\n")

    cmp_(outfilepath, reffilepath)
