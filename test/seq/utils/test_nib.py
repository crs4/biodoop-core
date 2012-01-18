# BEGIN_COPYRIGHT
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
