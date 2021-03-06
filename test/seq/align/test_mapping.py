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

import unittest, copy
from itertools import izip

from bl.core.seq.align.mapping import SimpleMapping, SAMMapping
from bl.core.seq.align.sam_flags import *


class TestMapping(unittest.TestCase):
  
  def setUp(self):
    self.mapping = SimpleMapping()

  def test_is_paired(self):
    self.assertFalse(self.mapping.is_paired())
    self.mapping.flag |= SAM_FPD
    self.assertTrue(self.mapping.is_paired())

  def test_is_properly_paired(self):
    self.assertFalse(self.mapping.is_properly_paired())
    self.mapping.flag |= SAM_FPP
    self.assertTrue(self.mapping.is_properly_paired())

  def test_is_mapped(self):
    self.assertTrue(self.mapping.is_mapped())
    self.mapping.flag |= SAM_FSU
    self.assertFalse(self.mapping.is_mapped())

  def test_is_unmapped(self):
    self.assertFalse(self.mapping.is_unmapped())
    self.mapping.flag |= SAM_FSU
    self.assertTrue(self.mapping.is_unmapped())

  def test_is_mate_mapped(self):
    self.assertTrue(self.mapping.is_mate_mapped())
    self.mapping.flag |= SAM_FMU
    self.assertFalse(self.mapping.is_mate_mapped())

  def test_is_mate_unmapped(self):
    self.assertFalse(self.mapping.is_mate_unmapped())
    self.mapping.flag |= SAM_FMU
    self.assertTrue(self.mapping.is_mate_unmapped())

  def test_is_on_reverse(self):
    self.assertFalse(self.mapping.is_on_reverse())
    self.mapping.flag |= SAM_FSR
    self.assertTrue(self.mapping.is_on_reverse())

  def test_is_mate_on_reverse(self):
    self.assertFalse(self.mapping.is_mate_on_reverse())
    self.mapping.flag |= SAM_FMR
    self.assertTrue(self.mapping.is_mate_on_reverse())

  def test_is_read1(self):
    self.assertFalse(self.mapping.is_read1())
    self.mapping.flag |= SAM_FR1
    self.assertTrue(self.mapping.is_read1())

  def test_is_read2(self):
    self.assertFalse(self.mapping.is_read2())
    self.mapping.flag |= SAM_FR2
    self.assertTrue(self.mapping.is_read2())

  def test_is_secondary_align(self):
    self.assertFalse(self.mapping.is_secondary_align())
    self.mapping.flag |= SAM_FSC
    self.assertTrue(self.mapping.is_secondary_align())

  def test_set_paired(self):
    self.assertFalse(self.mapping.is_paired())
    self.mapping.set_paired(True)
    self.assertTrue(self.mapping.is_paired())
    self.mapping.set_paired(False)
    self.assertFalse(self.mapping.is_paired())

  def test_set_properly_paired(self):
    self.assertFalse(self.mapping.is_properly_paired())
    self.mapping.set_properly_paired(True)
    self.assertTrue(self.mapping.is_properly_paired())
    self.mapping.set_properly_paired(False)
    self.assertFalse(self.mapping.is_properly_paired())

  def test_set_mapped(self):
    self.assertTrue(self.mapping.is_mapped())
    self.mapping.set_mapped(False)
    self.assertFalse(self.mapping.is_mapped())
    self.mapping.set_mapped(True)
    self.assertTrue(self.mapping.is_mapped())

  def test_set_mate_mapped(self):
    self.assertTrue(self.mapping.is_mate_mapped())
    self.mapping.set_mate_mapped(False)
    self.assertFalse(self.mapping.is_mate_mapped())
    self.mapping.set_mate_mapped(True)
    self.assertTrue(self.mapping.is_mate_mapped())

  def test_set_mate_unmapped(self):
    self.assertFalse(self.mapping.is_paired())
    self.mapping.set_paired(True)
    self.assertTrue(self.mapping.is_paired())
    self.mapping.set_paired(False)
    self.assertFalse(self.mapping.is_paired())

  def test_set_on_reverse(self):
    self.assertFalse(self.mapping.is_on_reverse())
    self.mapping.set_on_reverse(True)
    self.assertTrue(self.mapping.is_on_reverse())
    self.mapping.set_on_reverse(False)
    self.assertFalse(self.mapping.is_on_reverse())

  def test_set_mate_on_reverse(self):
    self.assertFalse(self.mapping.is_mate_on_reverse())
    self.mapping.set_mate_on_reverse(True)
    self.assertTrue(self.mapping.is_mate_on_reverse())
    self.mapping.set_mate_on_reverse(False)
    self.assertFalse(self.mapping.is_mate_on_reverse())

  def test_set_read1(self):
    self.assertFalse(self.mapping.is_read1())
    self.mapping.set_read1(True)
    self.assertTrue(self.mapping.is_read1())
    self.mapping.set_read1(False)
    self.assertFalse(self.mapping.is_read1())

  def test_set_read2(self):
    self.assertFalse(self.mapping.is_read2())
    self.mapping.set_read2(True)
    self.assertTrue(self.mapping.is_read2())
    self.mapping.set_read2(False)
    self.assertFalse(self.mapping.is_read2())

  def test_set_secondary_align(self):
    self.assertFalse(self.mapping.is_secondary_align())
    self.mapping.set_secondary_align(True)
    self.assertTrue(self.mapping.is_secondary_align())
    self.mapping.set_secondary_align(False)
    self.assertFalse(self.mapping.is_secondary_align())

  def test_set_failed_qc(self):
    self.assertFalse(self.mapping.is_failed_qc())
    self.mapping.set_failed_qc(True)
    self.assertTrue(self.mapping.is_failed_qc())
    self.mapping.set_failed_qc(False)
    self.assertFalse(self.mapping.is_failed_qc())

  def test_set_duplicate(self):
    self.assertFalse(self.mapping.is_duplicate())
    self.mapping.set_duplicate(True)
    self.assertTrue(self.mapping.is_duplicate())
    self.mapping.set_duplicate(False)
    self.assertFalse(self.mapping.is_duplicate())

  def test_get_untrimmed_pos_unclipped_forward(self):
    # hit has not been clipped and it's on the forward strand
    self.mapping.pos = 12345
    self.assertEqual(self.mapping.pos, self.mapping.get_untrimmed_pos())

  def test_get_untrimmed_pos_clipped_forward(self):
    # hit has been clipped to length 90, and it's not on the reverse strand
    self.mapping.pos = 12345
    self.mapping.add_tag(('XC', 'i', 90))
    self.assertEqual(self.mapping.pos, self.mapping.get_untrimmed_pos())

  def test_get_untrimmed_pos_unclipped_reverse(self):
    # hit has not been clipped and it's on the reverse strand
    self.mapping.set_on_reverse(True)
    self.mapping.pos = 12345
    self.assertEqual(self.mapping.pos, self.mapping.get_untrimmed_pos())

  def test_get_untrimmed_pos_clipped_reverse(self):
    # hit has been clipped to 35 and it's on the reverse strand
    self.mapping.pos = 12345
    self.mapping.set_seq_5("A"*50) # a 50-base sequence
    self.mapping.add_tag(('XC', 'i', 35)) # clipped to 35
    self.mapping.set_on_reverse(True)
    self.assertEqual(self.mapping.pos - 15, self.mapping.get_untrimmed_pos())

  def test_get_seq_len(self):
    self.mapping.set_seq_5("")
    self.assertEqual(0, self.mapping.get_seq_len())
    self.mapping.set_seq_5("AB" * 10)
    self.assertEqual(20, self.mapping.get_seq_len())

  def test_remove_mate(self):
    m = self.mapping
    m.set_name("p1:read/1")
    m.tid = "chr1"
    m.pos = 12345
    m.set_read1(True)
    m.mtid = "chr1"
    m.mpos = m.pos + 150
    m.set_paired(True)
    m.set_properly_paired(True)
    m.set_mate_mapped(False)
    original = copy.copy(m)
    m.remove_mate()
    self.assertEqual(original.tid, m.tid)
    self.assertEqual(original.pos, m.pos)
    self.assertEqual(None, m.mtid)
    self.assertEqual(0, m.mpos)
    self.assertFalse(m.is_properly_paired())
    self.assertTrue(m.is_mate_mapped()) # make sure the bit ISN'T set


class TestSAMMapping(unittest.TestCase):
  
  SEQ = 'AGCTTCTTTGACTCTCGAATTTTAGCACTAGAAGAAATAGTGAGGATTATATATTTCAGAAGTTCTCACCCAGGATATCAGAACACATTCA'
  QUAL = '5:CB:CCBCCB>:C@;BBBB??B;?>1@@=C=4ACCAB3A8=CC=C?CBC=CBCCCCCCCCCCCCC@5>?=?CAAB=3=>====5>=AC?C'
  SAM_FIELDS = [
    'FOO/1', '81', 'chr6', '3558357', '37', '5M1I85M', '*', '0', '0', SEQ,
    QUAL, 'XT:A:U', 'NM:i:0', 'SM:i:37', 'AM:i:0', 'X0:i:1', 'X1:i:0',
    'XM:i:0', 'XO:i:0', 'XG:i:0', 'MD:Z:91'
    ]
  
  def setUp(self):
    self.mapping = SAMMapping(self. SAM_FIELDS)

  def runTest(self):
    self.assertEqual(self.mapping.get_name(), "FOO/1")
    self.assertEqual(self.mapping.flag, 81)
    self.assertEqual(self.mapping.tid, "chr6")
    self.assertEqual(self.mapping.pos, 3558357)
    self.assertEqual(self.mapping.qual, 37)
    self.assertEqual(self.mapping.get_cigar(), [(5, 'M'), (1, 'I'), (85, 'M')])
    self.assertTrue(self.mapping.mtid is None)
    self.assertEqual(self.mapping.mpos, 0)
    self.assertEqual(self.mapping.isize, 0)
    self.assertEqual(self.mapping.get_seq_5(), self.SEQ)
    self.assertEqual(self.mapping.get_ascii_base_qual(), self.QUAL)
    for t, tstr in izip(self.mapping.each_tag(), self.SAM_FIELDS[11:]):
      self.assertEqual(t, tuple(tstr.split(":")))


def load_tests(loader, tests, pattern):
  test_cases = (TestMapping, TestSAMMapping)
  suite = unittest.TestSuite()
  for tc in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(tc))
  return suite


if __name__ == '__main__':
  suite = load_tests(unittest.defaultTestLoader, None, None)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
