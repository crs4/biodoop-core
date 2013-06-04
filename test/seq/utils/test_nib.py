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

import unittest, os

from bl.core.seq.utils import seq2nib


D = os.path.dirname(os.path.abspath(__file__))
SEQ_F = os.path.join(D, "data", "hg18_chrM.txt")
NIB_F = os.path.join(D, "data", "hg18_chrM.nib")


class TestSeq2Nib(unittest.TestCase):

  def runTest(self):
    with open(SEQ_F) as f:
      seq = f.read().strip()
    with open(NIB_F) as f:
      nib = f.read()
    self.assertEqual(seq2nib(seq), nib)


def load_tests(loader, tests, pattern):
  test_cases = (TestSeq2Nib,)
  suite = unittest.TestSuite()
  for tc in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(tc))
  return suite


if __name__ == '__main__':
  suite = load_tests(unittest.defaultTestLoader, None, None)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
