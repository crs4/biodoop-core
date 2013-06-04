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


class Reducer(pp.Reducer):
  pass
