# BEGIN_COPYRIGHT
# 
# Copyright (C) 2009-2013 CRS4.
# 
# This file is part of biodoop-core.
# 
# biodoop-core is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
# 
# biodoop-core is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
# 
# You should have received a copy of the GNU General Public License along with
# biodoop-core.  If not, see <http://www.gnu.org/licenses/>.
# 
# END_COPYRIGHT

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


class DictWriter(csv.DictWriter):

    def _dict_to_list(self, rowdict):
        return [_ for _ in csv.DictWriter._dict_to_list(self, rowdict) if _]


class BedError(Exception):
    pass


class BedFile(object):

    PARAMS = {"delimiter": "\t", "lineterminator": os.linesep}

    def __init__(self, name, mode="r", buffering=-1):
        if mode == "r":
            wrapper_type = csv.DictReader
        elif mode == "w" or mode == "a":
            wrapper_type = DictWriter
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
        for fname, ftype in REQUIRED_FIELDS:
            if r[fname] is None:
                raise BedError("at least 3 tab-separated fields are required")
            r[fname] = ftype(r[fname])
        for fname, ftype in OPTIONAL_FIELDS:
            if r[fname] is not None:
                r[fname] = ftype(r[fname])
        return r

    def writerow(self, row):
        out_row = {}
        for fname, _ in REQUIRED_FIELDS:
            value = row.get(fname)
            if value is None:
                raise BedError("missing required field '%s'" % fname)
            out_row[fname] = str(value)
        for fname, ftype in OPTIONAL_FIELDS:
            value = row.get(fname)
            if value is None:
                break  # no holes allowed
            if ftype == cs_int:
                value = ",".join(map (str, value))
            out_row[fname] = str(value)
        self.__wrapper.writerow(out_row)

    def __iter__(self):
        return self


def open(name, mode="r", buffering=-1):
    return BedFile(name, mode, buffering)
