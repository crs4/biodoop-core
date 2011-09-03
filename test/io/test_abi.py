# BEGIN_COPYRIGHT
# END_COPYRIGHT

# FIXME: This is not really a test. Just checking that it is
# exporting the right interface.

import unittest

from bl.core.io.abi import SDSReader

class test_sds_reader(unittest.TestCase):

  def open_file(self):
    sds_fname = 'data/taq_man_ex1.txt'
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
