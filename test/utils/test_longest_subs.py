import unittest
from bl.core.utils import longest_subs


class TestLongestSubs(unittest.TestCase):

  def setUp(self):
    self.seqs = ['abcd0', 'abc0d', 'abc0000']
    self.longest = 'abc'
    self.rseqs = ['000abc', '0bc0abc', 'dbc']
    self.rlongest = 'bc'

  def test_forward(self):
    self.assertEqual(longest_subs(self.seqs), self.longest)
    self.assertEqual(longest_subs(self.seqs, reverse=True), '')

  def test_reverse(self):
    self.assertEqual(longest_subs(self.rseqs, reverse=True), self.rlongest)
    self.assertEqual(longest_subs(self.rseqs), '')

  def test_corner_cases(self):
    self.assertTrue(longest_subs([]) is None)
    for reverse in False, True:
      self.assertEqual(longest_subs(['a'], reverse=reverse), 'a')


def load_tests(loader, tests, pattern):
  test_cases = (TestLongestSubs,)
  suite = unittest.TestSuite()
  for tc in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(tc))
  return suite


if __name__ == '__main__':
  suite = load_tests(unittest.defaultTestLoader, None, None)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
