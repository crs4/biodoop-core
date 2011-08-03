# BEGIN_COPYRIGHT
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
