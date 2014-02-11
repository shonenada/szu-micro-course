from __future__ import print_function
import re
import sys

from find import find


reload(sys)
sys.setdefaultencoding("utf8")


def search(path, file_pattern, content_pattern):
    """Start to find"""
    files = find(path, file_pattern, True)
    for file in files:
        i = 0
        opened_file = open(file)
        for line in opened_file.readlines():
            i = i + 1
            if re.search(content_pattern, line):
                print(file, "line", i)
