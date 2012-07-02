# BEGIN_COPYRIGHT
# END_COPYRIGHT

import logging, time
logging.basicConfig(level=logging.INFO)

import pydoop.pipes as pp
import pydoop.utils as pu

from bl.core.gt.kinship import KinshipVectors, KinshipBuilder


SEQF_INPUT_FORMAT = "org.apache.hadoop.mapred.SequenceFileInputFormat"


class Mapper(pp.Mapper):

  def __configure(self):
    jc = self.ctx.getJobConf()
    pu.jc_configure_log_level(self, jc, "bl.mr.loglevel", "log_level", "INFO")
    self.logger = logging.getLogger("mapper")
    self.logger.setLevel(self.log_level)
    pu.jc_configure_int(self, jc, "mapred.task.timeout", "timeout")
    pu.jc_configure(self, jc, "mapred.input.format.class", "input_format", "")
    self.is_first_step = self.input_format != SEQF_INPUT_FORMAT

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
    if self.is_first_step:
      gt_vector = v.split()
      if self.builder is None:
        self.builder = KinshipBuilder(len(gt_vector))
      self.builder.add_contribution(gt_vector)
    else:
      vectors = KinshipVectors.deserialize(v)
      if self.builder is None:
        self.builder = KinshipBuilder(vectors)
      else:
        self.builder.vectors += vectors
    t = time.time()
    if t - self.prev_t >= self.feedback_interval:
      msg = "%d records processed" % self.record_count
      self.logger.info(msg)
      ctx.setStatus(msg)
      self.prev_t = t

  def close(self):
    if self.builder:
      self.ctx.emit("", self.builder.vectors.serialize())
      self.logger.info("all done")
    else:
      self.logger.info("no input records")
