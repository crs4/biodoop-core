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
from itertools import izip
import numpy as np

import bl.core.gt.messages.SnpCall as SnpCall
import bl.core.gt.messages.sample_snp_call as ssc


class TestSSC(unittest.TestCase):

  def setUp(self):
    self.encoder = ssc.Encoder()
    self.decoder = ssc.Decoder()

  def test_ssc(self):
    for call_string in "A", "B", "AA", "AB", "BB", "NC", "MC":
      call = getattr(SnpCall, call_string)
      values = 'foo', 'bar', call, 0.3, 0.5, 0.78, 1.e-4, 1.e-20, np.nan
    msg = self.encoder.encode(*values)
    t_values = self.decoder.decode(msg)
    for v, t_v in izip(values[:3], t_values[:3]):
      self.assertEqual(v, t_v)
    for v, t_v in izip(values[3:-1], t_values[3:-1]):
      self.assertAlmostEqual(v, t_v)
    self.assertTrue(np.isnan(t_values[-1]))


def load_tests(loader, tests, pattern):
  suite = unittest.TestSuite()
  suite.addTest(TestSSC('test_ssc'))
  return suite


if __name__ == '__main__':
  suite = load_tests(unittest.defaultTestLoader, None, None)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
