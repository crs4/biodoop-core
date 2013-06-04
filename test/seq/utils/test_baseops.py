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

import unittest
from bl.core.seq.utils.baseops import reverse_complement


RC_TEST_CASES = [
  ('TGGTCCCTACCGTCGACTTG', 'CAAGTCGACGGTAGGGACCA'),
  ('GTGCATCGATTAGCCCGGGT', 'ACCCGGGCTAATCGATGCAC'),
  ('GTCCGCGCCACCGTGTGCTC', 'GAGCACACGGTGGCGCGGAC'),
  ('GCCATGCAAATAGGAACGCA', 'TGCGTTCCTATTTGCATGGC'),
  ('GATACACTTGGTCGTCGAAA', 'TTTCGACGACCAAGTGTATC'),
  ('TTTAGCTCCAAGTGACGTTT', 'AAACGTCACTTGGAGCTAAA'),
  ('AAGGGACCCCTTTTGTTTTC', 'GAAAACAAAAGGGGTCCCTT'),
  ('AGACCAGCAGGCTGCGCTTG', 'CAAGCGCAGCCTGCTGGTCT'),
  ('ACATGGCGATACAGGACGCC', 'GGCGTCCTGTATCGCCATGT'),
  ('GGTGAACTTGCAGTTGGTGA', 'TCACCAACTGCAAGTTCACC'),
  ('TGACCACAAAGGTACGGGTC', 'GACCCGTACCTTTGTGGTCA'),
  ('GGCAAGCCAGCTAGAGTCGG', 'CCGACTCTAGCTGGCTTGCC'),
  ('CTGTTATGTGTCTACGAATT', 'AATTCGTAGACACATAACAG'),
  ('GCTGGGGAGCACTTAGCTTA', 'TAAGCTAAGTGCTCCCCAGC'),
  ('GATCGCAGAACAATTTTCGT', 'ACGAAAATTGTTCTGCGATC'),
  ]


class TestReverseComplement(unittest.TestCase):

  def test_str(self):
    for s, rs in RC_TEST_CASES:
      self.assertEqual(reverse_complement(s), rs)

  def test_list(self):
    for s, rs in RC_TEST_CASES:
      s = list(s)
      self.assertEqual(reverse_complement(s), list(rs))

  def test_tuple(self):
    for s, rs in RC_TEST_CASES:
      s = tuple(s)
      self.assertEqual(reverse_complement(s), tuple(rs))


def load_tests(loader, tests, pattern):
  test_cases = (TestReverseComplement,)
  suite = unittest.TestSuite()
  for tc in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(tc))
  return suite


if __name__ == '__main__':
  suite = load_tests(unittest.defaultTestLoader, None, None)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
