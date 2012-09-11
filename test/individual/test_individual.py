# BEGIN_COPYRIGHT
# END_COPYRIGHT

import unittest
from bl.core.individual import Individual
import bl.core.individual.gender as gender


class TestIndividual(unittest.TestCase):

  def setUp(self):
    #
    #    GRANDPA --- GRANDMA
    #             |
    #          -------
    #          |     |
    # MOM --- DAD   UNCLE
    #      |
    #      ME
    #
    self.grandpa = Individual("GRANDPA", "M")
    self.grandma = Individual("GRANDMA", "F")
    self.mom = Individual("MOM", "F")
    self.dad = Individual("DAD", "M", father=self.grandpa, mother=self.grandma)
    self.uncle = Individual("UNCLE", father=self.grandpa, mother=self.grandma)
    self.me = Individual("ME", "M", father=self.dad, mother=self.mom)

  def test_init(self):
    print
    print self.grandpa
    print self.grandma
    print self.mom
    print self.dad
    print self.uncle
    print self.me
    self.assertEqual(Individual("GRANDPA", "M"), self.grandpa)
    for i in self.grandpa, self.grandma:
      self.assertEqual(i.children, set([self.dad, self.uncle]))
    for i in self.dad, self.mom:
      self.assertEqual(i.children, set([self.me]))

  def test_properties(self):
    self.assertEqual(self.grandpa.gender, gender.MALE)
    self.grandpa.gender = "unknown"
    self.assertEqual(self.grandpa.gender, gender.UNKNOWN)
    self.assertEqual(self.dad.father, self.grandpa)
    batman = Individual("BATMAN", "M")
    self.mom.father = batman
    self.assertEqual(batman.children, set([self.mom]))
    self.assertEqual(self.dad.father_id, self.grandpa.id)
    self.assertTrue(batman.father_id is None)

  def test_methods(self):
    self.assertTrue(self.grandpa.is_male())
    self.assertTrue(self.grandma.is_female())
    for predicate in "is_male", "is_female":
      self.assertFalse(getattr(self.uncle, predicate)())
    for i in self.grandpa, self.grandma:
      self.assertTrue(i.is_founder())

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
