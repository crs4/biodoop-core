# BEGIN_COPYRIGHT
# END_COPYRIGHT

import struct

import pydoop.pipes as pp
from bl.core.gt.kinship import KinshipBuilder
from bl.core.messages.KinshipVectors import KinshipVectors_to_msg


class Mapper(pp.Mapper):

  def __init__(self, ctx):
    super(Mapper, self).__init__(ctx)
    self.builder = None
    #--- workaround to detect the last record ---
    isplit = pp.InputSplit(ctx.getInputSplit())
    self.split_end = isplit.offset + isplit.length
    #--------------------------------------------

  def map(self, ctx):
    v = ctx.getInputValue()    
    #--- workaround to detect the last record ---
    k = struct.unpack(">q", ctx.getInputKey())[0]
    is_last_record = k + len(v) + 2 >= self.split_end
    #--------------------------------------------
    gt_vector = v.split()
    if self.builder is None:
      self.builder = KinshipBuilder(len(gt_vector))
    self.builder.add_contribution(gt_vector)
    if is_last_record:
      vectors = self.builder.get_vectors()
      ctx.emit("", KinshipVectors_to_msg(*vectors))
