from __future__ import print_function
from os import remove

from find import find


def clean(path=None):
    """Remove all compiled opcode cache files (*.pyc)."""
    if path is None:
        path = "./"
    count = 0
    for pycfile in find(path, r"^[a-zA-Z0-9_]+\.(?:pyc|pyo)$"):
        print("Removing %s" % pycfile)
        remove(pycfile)
        count += 1
    print("-" * 78)
    print("%d files has been removed." % count)
