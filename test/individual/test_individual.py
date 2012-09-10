# BEGIN_COPYRIGHT
# END_COPYRIGHT

import unittest
import bl.core.individual as ind


class TestIndividual(unittest.TestCase):

  def test_init(self):
    a_grandpa = ind.Individual("A_GRANDPA", "M")
    a_grandma = ind.Individual("A_GRANDMA", "F")
    a_dad = ind.Individual("A_DAD", "M", father=a_grandpa, mother=a_grandma)
    a_mule = ind.Individual("A_MULE", "F", father=a_grandpa, mother=a_grandma)
    b_mom = ind.Individual("B_MOM", "F")
    a_son = ind.Individual("A_SON", "M", father=a_dad, mother=b_mom)
    #--
    print
    print a_grandpa
    print a_grandma
    print a_dad
    print a_mule
    print b_mom
    print a_son
    #--
    for i in a_grandpa, a_grandma:
      self.assertEqual(i.children, set([a_dad, a_mule]))
    for i in a_dad, b_mom:
      self.assertEqual(i.children, set([a_son]))


def load_tests(loader, tests, pattern):
  test_cases = (TestIndividual,)
  suite = unittest.TestSuite()
  for tc in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(tc))
  return suite


if __name__ == '__main__':
  suite = load_tests(unittest.defaultTestLoader, None, None)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
