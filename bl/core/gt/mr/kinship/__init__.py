# BEGIN_COPYRIGHT
# END_COPYRIGHT

"""
Compute the kinship matrix of a set of genotypes.

This is a MapReduce implementation of the ``ibs`` function from
`GenABEL <http://www.genabel.org>`_.
"""

import pydoop.pipes as pp

from phase_one_mapper import PhaseOneMapper

class Reducer(pp.Reducer):
  pass

# TODO: add entry point for subsequent jobs
def run_task():
  return pp.runTask(pp.Factory(PhaseOneMapper, Reducer))
