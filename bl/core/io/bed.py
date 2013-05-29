"""
`BED <https://genome.ucsc.edu/FAQ/FAQformat.html#format1>`_ I/O.
"""

import __builtin__
import os, csv


def cs_int(s):
    return map(int, s.strip(",").split(","))

REQUIRED_FIELDS = [
    ("chrom", str),          # name of the chromosome or scaffold, e.g., 'chr1'
    ("chromStart", int),     # 0-based index
    ("chromEnd", int),       # 0-based index plus 1, as in range()
    ]
OPTIONAL_FIELDS = [
    ("name", str),           # name of the feature
    ("score", int),          # 0-1000, determines gray level when visualized
    ("strand", str),         # '+' or '-'
    ("thickStart", int),     # draw feature thickly starting from this position
    ("thickEnd", int),       # stop drawing feature thickly at this position
    ("itemRgb", cs_int),     # 0-255,0-255,0-255 display color
    ("blockCount", int),     # number of blocks (exons)
    ("blockSizes", cs_int),  # block sizes
    ("blockStarts", cs_int), # block starts, relative to chromStart
    ]
FIELDS = REQUIRED_FIELDS + OPTIONAL_FIELDS
FIELDNAMES = [f[0] for f in FIELDS]


class BedFile(object):

    PARAMS = {"delimiter": "\t", "lineterminator": os.linesep}

    def __init__(self, name, mode="r", buffering=-1):
        if mode == "r":
            wrapper_type = csv.DictReader
        elif mode == "w" or mode == "a":
            wrapper_type = csv.DictWriter
        else:
            raise ValueError("opening mode '%s' not supported" % mode)
        self.f = __builtin__.open(name, mode, buffering)
        self.__wrapper = wrapper_type(self.f, FIELDNAMES, **self.PARAMS)

    @property
    def name(self):
        return self.f.name

    @property
    def closed(self):
        return self.f.closed

    def close(self):
        self.f.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def next(self):
        r = self.__wrapper.next()
        for fname, ftype in FIELDS:
            r[fname] = ftype(r[fname])
        return r

    def __iter__(self):
        return self


def open(name, mode="r", buffering=-1):
    return BedFile(name, mode, buffering)
