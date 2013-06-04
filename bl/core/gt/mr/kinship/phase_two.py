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

"""
Phase two: input data = paths of compressed, serialized KinshipVector objects.

This phase is meant to be run on phase one's output when the latter is
too large for a single process to collect.  Using less mappers than
there are KinshipVector files allows to reduce the burden of
assembling the final matrix.

FIXME: phase_two is a misnomer, since it can be run any number of
times with a progressively reduced number of mappers.
"""

import zlib

import pydoop.hdfs as hdfs
import pydoop.pipes as pp

from bl.core.gt.kinship import KinshipBuilder, KinshipVectors
from common import BaseMapper, Reducer


class Mapper(BaseMapper):

  def _feed_builder(self, v):
    fn = v.strip()
    with hdfs.open(fn, user=self.user) as f:
      s = zlib.decompress(f.read())
    vectors = KinshipVectors.deserialize(s)  # ignores trailing newline char
    if self.builder is None:
      self.builder = KinshipBuilder(vectors)
    else:
      self.builder.vectors += vectors


def run_task():
  return pp.runTask(pp.Factory(Mapper, Reducer))
