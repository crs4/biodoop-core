# BEGIN_COPYRIGHT
# END_COPYRIGHT

"""
Compute the kinship matrix of a set of genotypes.

This is a MapReduce implementation of the ``ibs`` function from
`GenABEL <http://www.genabel.org>`_.
"""

import pydoop.pipes as pp
from mapper import Mapper


# map-only
class Reducer(pp.Reducer):
  def reduce(self, ctx):
    pass


def run_task():
  return pp.runTask(pp.Factory(Mapper, Reducer))
