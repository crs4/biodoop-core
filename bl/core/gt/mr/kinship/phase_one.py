# BEGIN_COPYRIGHT
# END_COPYRIGHT

"""
Phase one: input data = tab-separated genotype matrix where rows
represent SNPs and columns represent samples.
"""

import pydoop.pipes as pp

from bl.core.gt.kinship import KinshipBuilder
from common import BaseMapper, Reducer


class Mapper(BaseMapper):

  def _feed_builder(self, v):
    gt_vector = v.split()
    if self.builder is None:
      self.builder = KinshipBuilder(len(gt_vector))
    self.builder.add_contribution(gt_vector)


def run_task():
  return pp.runTask(pp.Factory(Mapper, Reducer))
