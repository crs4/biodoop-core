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

# FIXME: This is not really a test. Just checking that it is
# exporting the right interface.

import unittest, os
from bl.core.io.abi import SDSReader


D = os.path.dirname(os.path.abspath(__file__))


class test_sds_reader(unittest.TestCase):

  def open_file(self):
    sds_fname = os.path.join(D, 'data', 'taq_man_ex1.txt')
    sds = SDSReader(open(sds_fname), swap_sample_well_columns=True)
    print sds.datetime
    print sds.fieldnames
    for k, v in sds.header['params'].iteritems():
      print '%s: %s' % (k, v)
    for m, v in sds.header['markers_info'].iteritems():
      print '%s: %s' % (m, v)
    for r in sds:
      self.assertNotEqual(r['Well'], 'Well')
      # if r['HMD'] or r['FOS'] or r['LME'] or r['EW'] or r['BPR']:
      #   print r
      # else:
      #   print 'Well %s:  %s' % (r['Well'], r['Call'])

  def runTest(self):
    self.open_file()


def load_tests(loader, tests, pattern):
  test_cases = (test_sds_reader,)
  suite = unittest.TestSuite()
  for tc in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(tc))
  return suite


if __name__ == '__main__':
  suite = load_tests(unittest.defaultTestLoader, None, None)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
