# BEGIN_COPYRIGHT
# END_COPYRIGHT

import zlib

import pydoop.hdfs as hdfs

from bl.core.gt.kinship import KinshipBuilder, KinshipVectors
from base_mapper import BaseMapper


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
