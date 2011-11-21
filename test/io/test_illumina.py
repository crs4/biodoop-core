# BEGIN_COPYRIGHT
# END_COPYRIGHT

# FIXME: This is not really a test. Just checking that it is
# exporting the right interface.

import unittest, os
from bl.core.io.illumina import GenomeStudioFinalReportReader as Reader
from bl.core.io.illumina import IllSNPReader


D = os.path.dirname(os.path.abspath(__file__))


class test_gs_frep_reader(unittest.TestCase):

  def open_file(self):
    gs_frep_fname = os.path.join(D, 'data', 'genome_studio_final_report_0.txt')
    gs_frep = Reader(open(gs_frep_fname))
    print
    print gs_frep.header
    for block in gs_frep.get_sample_iterator():
      print block.sample_id
      print block.snp_names()
      for k in block.snp_names():
        snp = block.snp[k]
        print '\nSNP:', snp['SNP'],
        for a in ['Allele1 - Top', 'Allele2 - Top']:
          print '%s -> %s' % (a, snp[a]),
      print

  def runTest(self):
    self.open_file()


class test_IllSNPReader(unittest.TestCase):

  def runTest(self):
    print
    with open(os.path.join(D, 'data', 'ill_annot.csv')) as f:
      reader = IllSNPReader(f)
      for r in reader:
        print r["IlmnID"], r["Name"]


def load_tests(loader, tests, pattern):
  test_cases = (test_gs_frep_reader, test_IllSNPReader)
  suite = unittest.TestSuite()
  for tc in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(tc))
  return suite


if __name__ == '__main__':
  suite = load_tests(unittest.defaultTestLoader, None, None)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
