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
import bl.core.utils.random_ext as rext


N_ITER = 100


class TestSampleWR(unittest.TestCase):

  def runTest(self):
    pop = 'ACGT'
    size = 10
    for i in xrange(N_ITER):
      s = rext.sample_wr(pop, size)
      self.assertEqual(len(s), size)
      self.assertTrue(set(s).issubset(pop))


class TestRandomString(unittest.TestCase):

  def test_defaults(self):
    for i in xrange(N_ITER):
      s = rext.random_string()
      self.assertEqual(len(s), rext.RAND_STR_LEN)
      self.assertTrue(set(s).issubset(rext.RAND_STR_POOL))

  def test_params(self):
    length = rext.RAND_STR_LEN + 1
    pool = 'ACGT'
    for i in xrange(N_ITER):
      s = rext.random_string(length, pool)
      self.assertEqual(len(s), length)
      self.assertTrue(set(s).issubset(pool))


def load_tests(loader, tests, pattern):
  test_cases = (TestSampleWR, TestRandomString)
  suite = unittest.TestSuite()
  for tc in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(tc))
  return suite


if __name__ == '__main__':
  suite = load_tests(unittest.defaultTestLoader, None, None)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
