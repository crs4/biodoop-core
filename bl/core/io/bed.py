"""
`BED <https://genome.ucsc.edu/FAQ/FAQformat.html#format1>`_ I/O.
"""
import csv

REQUIRED_FIELDS = [
    "chrom",       # name of the chromosome or scaffold, e.g., 'chr1'
    "chromStart",  # 0-based index
    "chromEnd",    # 0-based index plus 1, as in range()
    ]
OPTIONAL_FIELDS = [
    "name",        # name of the feature
    "score",       # 0-1000, higher numbers = darker gray when visualized
    "strand",      # '+' or '-'
    "thickStart",  # starting position at which the feature is drawn thickly
    "thickEnd",    # ending position at which the feature is drawn thickly
    "itemRgb",     # 0-255,0-255,0-255 display color
    "blockCount",  # number of blocks (exons)
    "blockSizes",  # comma-separated block sizes
    "blockStarts", # comma-separated block starts, relative to chromStart
    ]
FIELDS = REQUIRED_FIELDS + OPTIONAL_FIELDS


class BedReader(object):

    def __init__(self, f):
        self.f = f
        self.csv_reader = csv.DictReader(self.f, FIELDS, delimiter="\t")

    def close(self):
        self.f.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def next(self):
        r = self.csv_reader.next()
        # TODO: type conversion
        return r
