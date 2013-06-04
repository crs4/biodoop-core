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

# this should only be used to perform a quick check for missing
# imports and similar macroscopic errors: try*.py modules are not
# meant to be used for automated testing.

import sys, os


def get_try_scripts():
  scripts = []
  D = os.path.dirname(os.path.abspath(__file__))
  for root, dirs, files in os.walk(D):
    for fn in files:
      if fn.startswith("try") and fn.endswith(".py"):
        path = os.path.join(root, fn)
        yield path


if __name__ == "__main__":
  for i, s in enumerate(get_try_scripts()):
    print "\n* RUNNING %r" % s
    os.system("%s %s" % (sys.executable, s))
  print "\n* RAN %d scripts" % (i+1)
