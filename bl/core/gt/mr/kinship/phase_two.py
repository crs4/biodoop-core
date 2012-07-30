# BEGIN_COPYRIGHT
# END_COPYRIGHT

"""
Phase two: input data = paths of compressed, serialized KinshipVector objects.

This phase is meant to be run on phase one's output when the latter is
too large for a single process to collect.  Using less mappers than
there are KinshipVector files allows to reduce the burden of
assembling the final matrix.
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
