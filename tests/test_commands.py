from nose.tools import eq_

from ebus import commands
from tests.util import DummyConnection
from tests.util import run


def test_read():
    connection = DummyConnection(rxlines=["blub", "",], txlines=["read   -m TTL -c CIRCUIT  NAME  FIELD ",])

    async def test():
        data = await commands.read(connection, "NAME", field="FIELD", circuit="CIRCUIT", ttl="TTL")
        eq_(data, "blub")

    run(test)


def test_write():
    connection = DummyConnection(rxlines=["blub", "",], txlines=["write -c  CIRCUIT  NAME  VALUE ",])

    async def test():
        data = await commands.write(connection, "NAME", "CIRCUIT", "VALUE")
        eq_(data, None)

    run(test)


def test_listen():
    connection = DummyConnection(rxlines=["blub", "",], txlines=["listen -v ",])

    async def test():
        data = await commands.start_listening(connection)
        eq_(data, None)

    run(test)


def test_info():
    connection = DummyConnection(
        rxlines=[
            "version: ebusd 3.4.v3.3-51-g57eae05",
            (
                "update check: revision v3.4 available, vaillant/08.bai.csv: different version available, vaillant/"
                "bai.0010015600.inc: different version available, vaillant/hcmode.inc: different version available"
            ),
            "signal: no signal",
            "reconnects: 3",
            "masters: 8",
            "messages: 1012",
            "conditional: 14",
            "poll: 1",
            "update: 12",
            "address 03: master #11",
            (
                'address 08: slave #11, scanned "MF=Vaillant;ID=BAI00;SW=0204;HW=9602", loaded "vaillant/bai.0010015600.inc" '
                '([HW=9602]), "vaillant/08.bai.csv"'
            ),
            "address 10: master #2",
            'address 15: slave #2, scanned "MF=Vaillant;ID=UI   ;SW=0508;HW=6201", loaded "vaillant/15.ui.csv"',
            "address 17: master #17",
            'address 1c: slave #17, scanned "MF=Vaillant;ID=RC C ;SW=0508;HW=6201", loaded "vaillant/1c.rcc.4.csv"',
            'address 23: slave, scanned "MF=Vaillant;ID=VR630;SW=0500;HW=6301", loaded "vaillant/23.vr630.cc.csv"',
            'address 25: slave, scanned "MF=Vaillant;ID=VR630;SW=0500;HW=6301", loaded "vaillant/25.vr630.hwc.csv"',
            'address 26: slave, scanned "MF=Vaillant;ID=VR630;SW=0500;HW=6301", loaded "vaillant/26.vr630.hc.csv"',
            "address 31: master #8, ebusd",
            "address 36: slave #8, ebusd",
            "address 37: master #18",
            'address 3c: slave #18, scanned "MF=Vaillant;ID=RC C ;SW=0508;HW=6201", loaded "vaillant/3c.rcc.5.csv"',
            'address 50: slave, scanned "MF=Vaillant;ID=VR630;SW=0500;HW=6301", loaded "vaillant/50.vr630.mc.csv"',
            'address 51: slave, scanned "MF=Vaillant;ID=VR630;SW=0500;HW=6301", loaded "vaillant/51.vr630.mc.3.csv"',
            'address 52: slave, scanned "MF=Vaillant;ID=MC2  ;SW=0500;HW=6301", loaded "vaillant/52.mc2.mc.4.csv"',
            'address 53: slave, scanned "MF=Vaillant;ID=MC2  ;SW=0500;HW=6301", loaded "vaillant/53.mc2.mc.5.csv"',
            "address 70: master #4",
            'address 75: slave #4, scanned "MF=Vaillant;ID=RC C ;SW=0508;HW=6201", loaded "vaillant/75.rcc.csv"',
            "address 7f: master #24",
            'address 84: slave #24, scanned "MF=Vaillant;ID=VR630;SW=0500;HW=6301"',
            "address f0: master #5",
            'address f5: slave #5, scanned "MF=Vaillant;ID=RC C ;SW=0508;HW=6201", loaded "vaillant/f5.rcc.3.csv"',
            "",
        ],
        txlines=["info ",],
    )

    async def test():
        data = await commands.info(connection)
        eq_(
            data,
            {
                "addresses": {
                    3: ["master #11"],
                    8: [
                        "slave #11",
                        'scanned "MF=Vaillant;ID=BAI00;SW=0204;HW=9602"',
                        'loaded "vaillant/bai.0010015600.inc" ([HW=9602])',
                        '"vaillant/08.bai.csv"',
                    ],
                    16: ["master #2"],
                    21: ["slave #2", 'scanned "MF=Vaillant;ID=UI   ;SW=0508;HW=6201"', 'loaded "vaillant/15.ui.csv"',],
                    23: ["master #17"],
                    28: [
                        "slave #17",
                        'scanned "MF=Vaillant;ID=RC C ;SW=0508;HW=6201"',
                        'loaded "vaillant/1c.rcc.4.csv"',
                    ],
                    35: [
                        "slave",
                        'scanned "MF=Vaillant;ID=VR630;SW=0500;HW=6301"',
                        'loaded "vaillant/23.vr630.cc.csv"',
                    ],
                    37: [
                        "slave",
                        'scanned "MF=Vaillant;ID=VR630;SW=0500;HW=6301"',
                        'loaded "vaillant/25.vr630.hwc.csv"',
                    ],
                    38: [
                        "slave",
                        'scanned "MF=Vaillant;ID=VR630;SW=0500;HW=6301"',
                        'loaded "vaillant/26.vr630.hc.csv"',
                    ],
                    49: ["master #8", "ebusd"],
                    54: ["slave #8", "ebusd"],
                    55: ["master #18"],
                    60: [
                        "slave #18",
                        'scanned "MF=Vaillant;ID=RC C ;SW=0508;HW=6201"',
                        'loaded "vaillant/3c.rcc.5.csv"',
                    ],
                    80: [
                        "slave",
                        'scanned "MF=Vaillant;ID=VR630;SW=0500;HW=6301"',
                        'loaded "vaillant/50.vr630.mc.csv"',
                    ],
                    81: [
                        "slave",
                        'scanned "MF=Vaillant;ID=VR630;SW=0500;HW=6301"',
                        'loaded "vaillant/51.vr630.mc.3.csv"',
                    ],
                    82: [
                        "slave",
                        'scanned "MF=Vaillant;ID=MC2  ;SW=0500;HW=6301"',
                        'loaded "vaillant/52.mc2.mc.4.csv"',
                    ],
                    83: [
                        "slave",
                        'scanned "MF=Vaillant;ID=MC2  ;SW=0500;HW=6301"',
                        'loaded "vaillant/53.mc2.mc.5.csv"',
                    ],
                    112: ["master #4"],
                    117: [
                        "slave #4",
                        'scanned "MF=Vaillant;ID=RC C ;SW=0508;HW=6201"',
                        'loaded "vaillant/75.rcc.csv"',
                    ],
                    127: ["master #24"],
                    132: ["slave #24", 'scanned "MF=Vaillant;ID=VR630;SW=0500;HW=6301"',],
                    240: ["master #5"],
                    245: [
                        "slave #5",
                        'scanned "MF=Vaillant;ID=RC C ;SW=0508;HW=6201"',
                        'loaded "vaillant/f5.rcc.3.csv"',
                    ],
                },
                "version": "ebusd 3.4.v3.3-51-g57eae05",
                "update check": (
                    "revision v3.4 available, vaillant/08.bai.csv: different version available, "
                    "vaillant/bai.0010015600.inc: "
                    "different version available, vaillant/hcmode.inc: different version available"
                ),
                "signal": "no signal",
                "reconnects": "3",
                "masters": "8",
                "messages": "1012",
                "conditional": "14",
                "poll": "1",
                "update": "12",
            },
        )

    run(test)
