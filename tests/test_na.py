import asyncio

from nose.tools import eq_

import ebus


def test_na():
    """Not Available."""
    eq_(str(ebus.NA), "Not Available")
    eq_(repr(ebus.NA), "NA")


def test_na_cmp():
    """Not Available Compare."""
    eq_(ebus.NA is ebus.NA, True)
    eq_(ebus.NA == ebus.NA, True)

    eq_(ebus.NA == ebus.NotAvailable(), True)


def test_na_singleton():
    """Not Available Singleton."""
    eq_(ebus.NotAvailable() is ebus.NotAvailable(), True)  # Singleton


def test_na_bool():
    eq_(bool(ebus.NA), False)
