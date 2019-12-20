import contextlib
import filecmp
import os
import shutil
import sys

_LEARN = True


def cmp_(out, ref):
    """Compare files."""
    if _LEARN:
        shutil.copyfile(out, ref)
    else:
        assert filecmp.cmp(out, ref)
    os.remove(out)
