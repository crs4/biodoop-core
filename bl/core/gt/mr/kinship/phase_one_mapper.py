# BEGIN_COPYRIGHT
# END_COPYRIGHT

from bl.core.gt.kinship import KinshipBuilder
from base_mapper import BaseMapper


class PhaseOneMapper(BaseMapper):

  def _feed_builder(self, v):
    gt_vector = v.split()
    if self.builder is None:
      self.builder = KinshipBuilder(len(gt_vector))
    self.builder.add_contribution(gt_vector)
