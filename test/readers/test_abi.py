# BEGIN_COPYRIGHT
# END_COPYRIGHT

import unittest

from bl.core.readers.abi import SDSReader

class test_sds_reader(unittest.TestCase):

  def open_file(self):
    sds_fname = 'data/taq_man_ex1.txt'
    sds = SDSReader(open(sds_fname))
    for k, v in sds.header['params'].iteritems():
      print '%s: %s' % (k, v)
    for m, v in sds.header['markers_info'].iteritems():
      print '%s: %s' % (m, v)
    for r in sds:
      if r['HMD'] or r['FOS'] or r['LME'] or r['EW'] or r['BPR']:
        print r
      else:
        print 'Well %s:  %s' % (r['Well'], r['Call'])

def suite():
  suite = unittest.TestSuite()
  suite.addTest(test_sds_reader('open_file'))
  return suite


if __name__ == '__main__':
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run((suite()))
