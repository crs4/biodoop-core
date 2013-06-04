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
import random, itertools, string


RAND_STR_LEN = 10
RAND_STR_POOL = string.letters + string.digits


# http://code.activestate.com/recipes/273085/
def sample_wr(population, k):
  """
  Choose k random elements (with replacement) from a population.
  """
  n = len(population)
  _random, _int = random.random, int  # speed hack
  return [population[_int(_random()*n)] for _ in itertools.repeat(None, k)]


def random_string(len=RAND_STR_LEN, pool=RAND_STR_POOL):
  return "".join(sample_wr(pool, len))
