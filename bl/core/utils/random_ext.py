# BEGIN_COPYRIGHT
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


def random_string(len=RAND_STR_LEN):
  choice = random.choice  # speed hack
  return "".join(choice(RAND_STR_POOL) for _ in xrange(RAND_STR_LEN))
