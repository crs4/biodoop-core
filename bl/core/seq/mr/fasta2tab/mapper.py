# BEGIN_COPYRIGHT
# 
# Copyright (C) 2009-2013 CRS4.
# 
# This file is part of biodoop-core.
# 
# biodoop-core is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
# 
# biodoop-core is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
# 
# You should have received a copy of the GNU General Public License along with
# biodoop-core.  If not, see <http://www.gnu.org/licenses/>.
# 
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
