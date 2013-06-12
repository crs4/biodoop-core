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

import unittest, os, tempfile
import bl.core.io.bed as bed


BED_DATA = [
    ("chr1", "66999824", "67210768", "GENE_01", "0", "+", "67000041",
     "67208778", "0,0,255", "4", "227,64,25,72", "0,91705,98928,101802"),
    ("chr7", "48998526", "50489626", "GENE_02", "0", "-", "48999844",
     "50489468", "0", "2", "1439,27,", "0,2035,"),
    ]


class TestRead(unittest.TestCase):

    def setUp(self):
        fd, self.fn = tempfile.mkstemp(prefix="bl_test")
        os.close(fd)
        self.records = []

    def tearDown(self):
        os.remove(self.fn)

    def __common_tests(self, row_size):
        with open(self.fn, "w") as fo:
            fo.write("\n".join("\t".join(r[:row_size]) for r in BED_DATA))
        with bed.open(self.fn) as fi:
            self.records = [r for r in fi]
        self.assertEqual(len(self.records), 2)
        for r in self.records:
            self.assertEqual(set(r.keys()), set(bed.FIELDNAMES))

    def test_complete(self):
        self.__common_tests(len(bed.FIELDS))
        r = self.records[1]
        self.assertEqual(r["chrom"], "chr7")
        self.assertEqual(r["chromStart"], 48998526)
        self.assertEqual(r["chromEnd"], 50489626)
        self.assertEqual(r["name"], "GENE_02")
        self.assertEqual(r["score"], 0)
        self.assertEqual(r["strand"], '-')
        self.assertEqual(r["thickStart"], 48999844)
        self.assertEqual(r["thickEnd"], 50489468)
        self.assertEqual(r["itemRgb"], [0])
        self.assertEqual(r["blockCount"], 2)
        self.assertEqual(r["blockSizes"], [1439, 27])
        self.assertEqual(r["blockStarts"], [0, 2035])

    def test_minimal(self):
        self.__common_tests(len(bed.REQUIRED_FIELDS))
        r = self.records[1]
        self.assertEqual(r["chrom"], "chr7")
        self.assertEqual(r["chromStart"], 48998526)
        self.assertEqual(r["chromEnd"], 50489626)
        for fname, _ in bed.OPTIONAL_FIELDS:
            self.assertEqual(r[fname], None)

    def test_too_short(self):
        self.assertRaises(
            bed.BedError, self.__common_tests, len(bed.REQUIRED_FIELDS) - 1
            )


class TestWrite(unittest.TestCase):

    def setUp(self):
        fields = "chrom", "chromStart", "chromEnd", "name", "score", "strand"
        self.data = [
            dict(zip(fields, ("chr1", 1, 3, "n0", 0, '+'))),
            dict(zip(fields, ("chr2", 5, 9, "n1", 1, '-'))),
            ]
        fd, self.fn = tempfile.mkstemp(prefix="bl_test_")
        os.close(fd)
        with bed.open(self.fn, "w") as fo:
            for r in self.data:
                fo.writerow(r)

    def tearDown(self):
        os.remove(self.fn)

    def runTest(self):
        with bed.open(self.fn) as fi:
            records = [r for r in fi]
        self.assertEqual(len(records), len(self.data))
        for r1, r2 in zip(records, self.data):
            for k, v in r2.iteritems():
                self.assertTrue(k in r1)
                self.assertEqual(r1[k], v)


def load_tests(loader, tests, pattern):
    test_cases = (TestRead, TestWrite)
    suite = unittest.TestSuite()
    for tc in test_cases:
        suite.addTests(loader.loadTestsFromTestCase(tc))
    return suite


if __name__ == '__main__':
    suite = load_tests(unittest.defaultTestLoader, None, None)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
