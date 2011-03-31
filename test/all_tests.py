# BEGIN_COPYRIGHT
# END_COPYRIGHT
import os, unittest
if not hasattr(unittest.TestLoader, "discover"):
  try:
    import unittest2 as unittest
  except ImportError:
    raise ImportError("Python older than 2.7, please install unittest2")


suite = unittest.defaultTestLoader.discover(os.path.dirname(__file__))


if __name__ == "__main__":
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
