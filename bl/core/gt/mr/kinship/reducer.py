# BEGIN_COPYRIGHT
# END_COPYRIGHT

import logging
logging.basicConfig(level=logging.INFO)

import pydoop.pipes as pp
import pydoop.utils as pu

from bl.core.gt.kinship import KinshipVectors, KinshipBuilder


class Reducer(pp.Reducer):

  def __configure(self):
    jc = self.ctx.getJobConf()
    pu.jc_configure_log_level(self, jc, "bl.mr.loglevel", "log_level", "INFO")
    self.logger = logging.getLogger("reducer")
    self.logger.setLevel(self.log_level)

  def __init__(self, ctx):
    super(Reducer, self).__init__(ctx)
    self.ctx = ctx
    self.__configure()
    self.builder = None

  def reduce(self, ctx):
    while ctx.nextValue():
      vectors = KinshipVectors.deserialize(ctx.getInputValue())
      if self.builder is None:
        self.builder = KinshipBuilder(vectors)
      else:
        self.builder.vectors += vectors
    if self.builder is None:
      self.logger.info("no input records")
    else:
      self.logger.info("building kinship matrix")
      k = self.builder.build()
      payload = KinshipBuilder.serialize(k)
      self.logger.debug("payload (len=%d): %r [...] %r" % (
        len(payload), payload[:10], payload[-10:]
        ))
      ctx.emit("", payload)
      # FIXME: KinshipBuilder.serialize is not prepending the array size
      # FIXME: we need a record writer
