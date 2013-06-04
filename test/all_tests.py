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
