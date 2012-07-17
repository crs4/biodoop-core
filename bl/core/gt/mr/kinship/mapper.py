# BEGIN_COPYRIGHT
# END_COPYRIGHT

import logging, time
logging.basicConfig(level=logging.INFO)

import pydoop.pipes as pp
import pydoop.utils as pu

from bl.core.gt.kinship import KinshipBuilder


class Mapper(pp.Mapper):

  def __configure(self):
    jc = self.ctx.getJobConf()
    pu.jc_configure_log_level(self, jc, "bl.mr.loglevel", "log_level", "INFO")
    self.logger = logging.getLogger("mapper")
    self.logger.setLevel(self.log_level)
    pu.jc_configure_int(self, jc, "mapred.task.timeout", "timeout")

  def __report(self, delta_t):
    msg = "%d records processed (last batch: %.1f s)" % (
      self.record_count, delta_t
      )
    self.logger.info(msg)
    self.ctx.setStatus(msg)

  def __init__(self, ctx):
    super(Mapper, self).__init__(ctx)
    self.ctx = ctx
    self.__configure()
    self.feedback_interval = self.timeout / 10000.
    self.builder = None
    self.record_count = 0
    self.prev_t = time.time()

  def map(self, ctx):
    v = ctx.getInputValue()
    self.record_count += 1
    gt_vector = v.split()
    if self.builder is None:
      self.builder = KinshipBuilder(len(gt_vector))
    self.builder.add_contribution(gt_vector)
    t = time.time()
    delta_t = t - self.prev_t
    if delta_t >= self.feedback_interval:
      self.__report(delta_t)
      self.prev_t = t

  def close(self):
    if self.builder:
      self.__report(time.time() - self.prev_t)
      self.ctx.emit("", self.builder.vectors.serialize())
      self.logger.info("all done")
    else:
      self.logger.info("no input records")
