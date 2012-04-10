# BEGIN_COPYRIGHT
# END_COPYRIGHT

import logging, struct, time
logging.basicConfig(level=logging.INFO)

import pydoop.pipes as pp
import pydoop.utils as pu

from bl.core.gt.kinship import KinshipBuilder
from bl.core.messages.KinshipVectors import KinshipVectors_to_msg


class Mapper(pp.Mapper):

  def __init__(self, ctx):
    super(Mapper, self).__init__(ctx)
    jc = ctx.getJobConf()
    pu.jc_configure_log_level(self, jc, "bl.mr.loglevel", "log_level", "INFO")
    pu.jc_configure_int(self, jc, "mapred.task.timeout", "timeout")
    self.logger = logging.getLogger("mapper")
    self.logger.setLevel(self.log_level)
    self.feedback_interval = self.timeout / 10.
    self.builder = None
    self.snp_count = 0
    #--- workaround to detect the last record ---
    isplit = pp.InputSplit(ctx.getInputSplit())
    self.split_end = isplit.offset + isplit.length
    #--------------------------------------------
    self.prev_t = time.time()

  def map(self, ctx):
    v = ctx.getInputValue()
    self.snp_count += 1
    #--- workaround to detect the last record ---
    k = struct.unpack(">q", ctx.getInputKey())[0]
    is_last_record = k + len(v) + 2 >= self.split_end
    #--------------------------------------------
    gt_vector = v.split()
    if self.builder is None:
      self.builder = KinshipBuilder(len(gt_vector))
    self.builder.add_contribution(gt_vector)
    t = time.time()
    if t - self.prev_t >= self.feedback_interval:
      msg = "%d SNPs processed" % self.snp_count
      self.logger.info(msg)
      ctx.setStatus(msg)
      self.prev_t = t
    if is_last_record:
      vectors = self.builder.get_vectors()
      msg = KinshipVectors_to_msg(*vectors)
      ctx.emit("", msg)
      self.logger.info("all done")
