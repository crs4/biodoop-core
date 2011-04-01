# BEGIN_COPYRIGHT
# END_COPYRIGHT
"""
Convert a FASTA dataset to a <HEADER>\t<SEQUENCE> format.
"""

import pydoop.pipes as pp
from bl.core.seq.mr.fasta_reader import record_reader
from mapper import Mapper


# map-only
class Reducer(pp.Reducer):
  def reduce(self, ctx):
    pass


def run_task():
  return pp.runTask(pp.Factory(Mapper, Reducer, record_reader))
