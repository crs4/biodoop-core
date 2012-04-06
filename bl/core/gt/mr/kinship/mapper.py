# BEGIN_COPYRIGHT
# END_COPYRIGHT

import logging, struct
logging.basicConfig(level=logging.INFO)

import pydoop.pipes as pp
import pydoop.utils as pu
import pydoop.hdfs as hdfs

from bl.core.gt.kinship import KinshipBuilder
from bl.core.messages.KinshipVectors import KinshipVectors_to_msg


class Mapper(pp.Mapper):

  def __init__(self, ctx):
    super(Mapper, self).__init__(ctx)
    jc = ctx.getJobConf()
    pu.jc_configure_log_level(self, jc, "bl.mr.loglevel", "log_level", "INFO")
    pu.jc_configure_int(self, jc, "mapred.task.partition", "part")
    pu.jc_configure(self, jc, "mapred.work.output.dir", "outdir")
    self.logger = logging.getLogger("mapper")
    self.logger.setLevel(self.log_level)
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
      msg = KinshipVectors_to_msg(*vectors)
      out_fn = hdfs.path.join(self.outdir, "kinship-%05d" % self.part)
      self.logger.info("writing to %r" % (out_fn,))
      hdfs.dump(msg, out_fn)
