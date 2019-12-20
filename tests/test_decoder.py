import pathlib

import ebus
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
                    outfile.write(f"\n{line}\n")
                    for value in decoder.decode(line):
                        outfile.write(f"  * {value.circuit} {value.field.title} {value.value} {value.attrs}\n")
                except (ebus.decoder.UnknownError, ebus.decoder.FormatError) as err:
                    outfile.write(f"  * {err!r}\n")

    cmp_(outfilepath, reffilepath)
