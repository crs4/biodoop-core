# BEGIN_COPYRIGHT
# END_COPYRIGHT

from itertools import izip
import pydoop.pipes as pp

from bl.core.messages.KinshipVectors import msg_to_KinshipVectors
from bl.core.messages.KinshipVectors import KinshipVectors_to_msg
from bl.core.gt.kinship import KinshipBuilder


class Reducer(pp.Reducer):

  def __init__(self, context):
    super(Reducer, self).__init__(context)
    self.builder = None

  def reduce(self, context):
    while context.nextValue():
      msg = context.getInputValue()
      obs_hom, exp_hom, present, lower_v, upper_v = msg_to_KinshipVectors(msg)
      if self.builder is None:
        self.builder = KinshipBuilder(obs_hom.size)
      self.builder.obs_hom += obs_hom
      self.builder.exp_hom += exp_hom
      self.builder.present += present
      for old_v, v in izip(self.builder.lower_v, lower_v):
        old_v += v
      for old_v, v in izip(self.builder.upper_v, upper_v):
        old_v += v
    msg = KinshipVectors_to_msg(*self.builder.get_vectors())
    context.emit(context.getInputKey(), msg)
