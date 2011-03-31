# BEGIN_COPYRIGHT
# END_COPYRIGHT
import zlib
import pydoop.pipes as pp
import pydoop.utils as pu


class Mapper(pp.Mapper):
  """
  Maps FASTA records to (header, sequence) pairs.
  """
  def __get_conf(self, jc):
    pu.jc_configure_bool(self, jc, 'bl.mr.fasta-reader.compress.header',
                         'compress_header', False)
    pu.jc_configure_bool(self, jc, 'bl.mr.fasta-reader.compress.seq',
                         'compress_seq', True)

  def __init__(self, ctx):
    super(Mapper, self).__init__(ctx)
    self.ctx = ctx
    jc = self.ctx.getJobConf()
    self.__get_conf(jc)

  def map(self, ctx):
    header, seq = ctx.getInputKey(), ctx.getInputValue()
    if self.compress_header:
      header = zlib.decompress(header)
    if self.compress_seq:
      seq = zlib.decompress(seq)
    ctx.emit(header, seq)
