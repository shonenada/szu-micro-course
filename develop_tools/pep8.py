from __future__ import print_function
from os import popen
from sys import stderr

from find import find


def pep8(path="."):
    """Check the project's coding style according to PEP 8."""
    modules = " ".join(find(path, r"^[a-zA-Z0-9_]+\.py$"))
    print("\n", "-" * 78, sep="")
    with popen("pep8 --statistics --count %s" % modules) as sh:
        result = sh.read()
        if not result:
            print("The project through the PEP8 check.")
        else:
            print(result, file=stderr)
    print("-" * 78)
