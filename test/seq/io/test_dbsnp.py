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

import unittest, tempfile, os
from itertools import izip

from bl.core.seq.io import DbSnpReader


DATA = '''>gnl|dbSNP|rs8896 rs=8896|pos=84|len=184|taxid=9606|mol="genomic"|class=1|alleles="C/T"|build=131
GGTGTTGGTT CTCTTAATCT TTAACTTAAA AGGTTAATGC TAAGTTAGCT TTACAGTGGG CTCTAGAGGG GGTAGAGGGG
GTG
Y
TATAGGGTAA ATACGGGCCC TATTTCAAAG ATTTTTAGGG GAATTAATTC TAGGACGATG GGCATGAAAC TGTGGTTTGC
TCCACAGATT TCAGAGCATT 

>gnl|dbSNP|rs8936 rs=8936|pos=201|len=401|taxid=9606|mol="genomic"|class=1|alleles="A/C/T"|build=125
ACTACGGCGG ACTAATCTTC AACTCCTACA TACTTCCCCC ATTATTCCTA GAACCAGGCG ACCTGCGACT CCTTGACGTT
GACAATCGAG TAGTACTCCC GATTGAAGCC CCCATTCGTA TAATAATTAC ATCACAAGAC GTCTTGCACT CATGAGCTGT
CCCCACATTA GGCTTAAAAA CAGATGCAAT TCCCGGACGT 
H
TAAACCAAAC CACTTTCACC GCTACACGAC CGGGGGTATA CTACGGTCAA TGCTCTGAAA TCTGTGGAGC AAACCACAGT
TTCATGCCCA TCGTCCTAGA ATTAATTCCC CTAAAAATCT TTGAAATAGG GCCCGTATTT ACCCTATAGC ACCCCCTCTA
CCCCCTCTAG AGCCCACTGT AAAGCTAACT TAGCATTAAC 
'''

EXPECTED_OUTPUT = [
  ("rs8896", "GGTGTTGGTTCTCTTAATCTTTAACTTAAAAGGTTAATGCTAAGTTAGCTTTACAGTGGGCTCTAGAGGGGGTAGAGGGGGTG", "C/T", "TATAGGGTAAATACGGGCCCTATTTCAAAGATTTTTAGGGGAATTAATTCTAGGACGATGGGCATGAAACTGTGGTTTGCTCCACAGATTTCAGAGCATT"),
  ("rs8936", "ACTACGGCGGACTAATCTTCAACTCCTACATACTTCCCCCATTATTCCTAGAACCAGGCGACCTGCGACTCCTTGACGTTGACAATCGAGTAGTACTCCCGATTGAAGCCCCCATTCGTATAATAATTACATCACAAGACGTCTTGCACTCATGAGCTGTCCCCACATTAGGCTTAAAAACAGATGCAATTCCCGGACGT", "A/C/T", "TAAACCAAACCACTTTCACCGCTACACGACCGGGGGTATACTACGGTCAATGCTCTGAAATCTGTGGAGCAAACCACAGTTTCATGCCCATCGTCCTAGAATTAATTCCCCTAAAAATCTTTGAAATAGGGCCCGTATTTACCCTATAGCACCCCCTCTACCCCCTCTAGAGCCCACTGTAAAGCTAACTTAGCATTAAC"),
  ]


class TestDbSnpReader(unittest.TestCase):

  def setUp(self):
    fd, self.fn = tempfile.mkstemp(prefix="bioland_")
    os.write(fd, DATA)
    os.close(fd)

  def tearDown(self):
    os.remove(self.fn)

  def runTest(self):
    with open(self.fn) as f:
      reader = DbSnpReader(f)
      output = list(reader)
    self.assertEqual(len(output), len(EXPECTED_OUTPUT))
    for t, exp_t in izip(output, EXPECTED_OUTPUT):
      self.assertEqual(len(t), len(exp_t))
      for x, exp_x in izip(t, exp_t):
        self.assertEqual(x, exp_x)


def load_tests(loader, tests, pattern):
  test_cases = (TestDbSnpReader,)
  suite = unittest.TestSuite()
  for tc in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(tc))
  return suite


if __name__ == '__main__':
  suite = load_tests(unittest.defaultTestLoader, None, None)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
