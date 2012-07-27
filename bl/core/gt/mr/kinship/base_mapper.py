# BEGIN_COPYRIGHT
# END_COPYRIGHT

import logging, time
logging.basicConfig(level=logging.INFO)

import pydoop.pipes as pp
import pydoop.utils as pu


class BaseMapper(pp.Mapper):

  def _feed_builder(self, v):
    raise NotImplementedError

  def _configure(self):
    jc = self.ctx.getJobConf()
    pu.jc_configure_log_level(self, jc, "bl.mr.loglevel", "log_level", "INFO")
    self.logger = logging.getLogger("mapper")
    self.logger.setLevel(self.log_level)
    pu.jc_configure_int(self, jc, "mapred.task.timeout", "timeout")
    pu.jc_configure(self, jc, "bl.hdfs.user", "user", "")

  def _report(self, delta_t):
    msg = "%d records processed (last batch: %.1f s)" % (
      self.record_count, delta_t
      )
    self.logger.info(msg)
    self.ctx.setStatus(msg)

  def __init__(self, ctx):
    super(BaseMapper, self).__init__(ctx)
    self.ctx = ctx
    self._configure()
    self.feedback_interval = self.timeout / 10000.
    self.builder = None
    self.record_count = 0
    self.prev_t = time.time()

  def map(self, ctx):
    v = ctx.getInputValue()
    self.record_count += 1
    self._feed_builder(v)
    t = time.time()
    delta_t = t - self.prev_t
    if delta_t >= self.feedback_interval:
      self._report(delta_t)
      self.prev_t = t

  def close(self):
    if self.builder:
      self._report(time.time() - self.prev_t)
      self.ctx.emit("", self.builder.vectors.serialize())
      self.logger.info("all done")
    else:
      self.logger.info("no input records")
