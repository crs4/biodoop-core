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

import unittest, cStringIO

from bl.core.io.ped import read_ped
import bl.core.individual.gender as G


PED = """example granpa unknown unknown m
example granny unknown unknown f
example father unknown unknown m
example mother granpa granny f
example sister father mother f
example brother father mother m
"""


class Test_read_ped(unittest.TestCase):

  def __check(self, ped):
    for id_ in "granpa", "granny", "father", "mother", "sister", "brother":
      self.assertIn(id_, ped)
      self.assertEqual(id_, ped[id_].id)
    for id_ in "granpa", "father", "brother":
      self.assertEqual(ped[id_].gender, G.MALE)
    for id_ in "granny", "mother", "sister":
      self.assertEqual(ped[id_].gender, G.FEMALE)
    for id_ in "granpa", "granny", "father":
      self.assertIsNone(ped[id_].father)
      self.assertIsNone(ped[id_].mother)
    self.assertIs(ped["mother"].father, ped["granpa"])
    self.assertIs(ped["mother"].mother, ped["granny"])
    for id_ in "sister", "brother":
      self.assertIs(ped[id_].father, ped["father"])
      self.assertIs(ped[id_].mother, ped["mother"])

  def __run(self, ped_txt):
    f = cStringIO.StringIO(ped_txt)
    ped = read_ped(f, sep=" ")
    self.__check(ped)
    f.close()

  def test_top_down(self):
    self.__run(PED)

  def test_bottom_up(self):
    rped = "".join(l for l in reversed(PED.splitlines(True)))
    self.__run(rped)


def load_tests(loader, tests, pattern):
  test_cases = (Test_read_ped,)
  suite = unittest.TestSuite()
  for tc in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(tc))
  return suite


if __name__ == '__main__':
  suite = load_tests(unittest.defaultTestLoader, None, None)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
