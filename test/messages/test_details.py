# BEGIN_COPYRIGHT
# END_COPYRIGHT

import unittest
import numpy as np

from bl.core.messages.details.Array_pb2 import Array
from bl.core.messages.details import load_array, unload_array


class test_details(unittest.TestCase):

  def runTest(self):
    for t in np.int32, np.int64, np.float32, np.float64:
      a = Array()
      orig_x = np.arange(12, dtype=t).reshape(3, 4)
      load_array(a, orig_x)
      x = unload_array(a)
      self.assertTrue(np.array_equal(x, orig_x))


def load_tests(loader, tests, pattern):
  test_cases = (test_details,)
  suite = unittest.TestSuite()
  for tc in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(tc))
  return suite


if __name__ == '__main__':
  suite = load_tests(unittest.defaultTestLoader, None, None)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
