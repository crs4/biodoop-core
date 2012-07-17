# BEGIN_COPYRIGHT
# END_COPYRIGHT

import pydoop.pipes as pp
import pydoop.utils as pu
import pydoop.hdfs as hdfs


class RecordWriter(pp.RecordWriter):

  def __init__(self, ctx):
    super(RecordWriter, self).__init__(ctx)
    jc = ctx.getJobConf()
    pu.jc_configure_int(self, jc, "mapred.task.partition", "part")
    pu.jc_configure(self, jc, "mapred.work.output.dir", "outdir")
    pu.jc_configure(self, jc, "bl.hdfs.user", "user", "")
    self.out_fn = hdfs.path.join(self.outdir, "part-%05d" % self.part)

  def emit(self, key, value):
    hdfs.dump(value, self.out_fn, user=self.user)
