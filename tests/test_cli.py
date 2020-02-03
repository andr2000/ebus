from nose.tools import assert_raises

import ebus


def test_noargs():
    """No Arguments."""
    with assert_raises(SystemExit):
        ebus.cli.argvhandler([])
