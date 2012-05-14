#!/usr/bin/env python
import re
import sys
from optparse import OptionParser

from textfilecache import TextFileCache

USAGE="%prog <options> <txt-file>"

PLACEHOLDER_START = "${"
PLACEHOLDER_END = "}"
PLACEHOLDER_RX = re.compile("^\s*" + re.escape(PLACEHOLDER_START) + "(.*)" + re.escape(PLACEHOLDER_END) + "$")

class ReplacerFunctor(object):
    def __init__(self, cache):
        self.cache = cache

    def __call__(self, match):
        text = self.cache[match.group(1)].rstrip()
        lines = text.split("\n")
        return "\n".join(["    " + x for x in lines])

def main():
    parser = OptionParser(usage=USAGE)
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("Missing args")

    src_name = args[0]
    src = open(src_name)
    dst = sys.stdout

    cache = TextFileCache(".")
    replacer = ReplacerFunctor(cache)

    for line in src.readlines():
        dst_line = PLACEHOLDER_RX.sub(replacer, line.rstrip())
        print >>dst, dst_line

    return 0


if __name__ == "__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
