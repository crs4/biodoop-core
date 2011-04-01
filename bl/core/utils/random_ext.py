# BEGIN_COPYRIGHT
# END_COPYRIGHT
import random, itertools

# http://code.activestate.com/recipes/273085/
def sample_wr(population, k):
  """
  Choose k random elements (with replacement) from a population.
  """
  n = len(population)
  _random, _int = random.random, int  # speed hack
  return [population[_int(_random()*n)] for _ in itertools.repeat(None, k)]
