import os
import re


def find(path, pattern, use_full_path=False):
    """Same as GNU find tool."""
    if use_full_path:
        path = os.path.abspath(path)
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if re.match(pattern, filename):
                yield os.path.join(dirpath, filename)
