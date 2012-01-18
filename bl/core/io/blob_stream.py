# BEGIN_COPYRIGHT
# END_COPYRIGHT

# FIXME: this should be converted to a metaclass, so that we can add a
# blob wrapper to any byte stream.

import struct


class BlobStream(file):
  
  MAGIC = 'BLOB_MAGIC-0.0'
  
  def write(self, blob):
    super(BlobStream, self).write(self.MAGIC)
    super(BlobStream, self).write(struct.pack('i', len(blob)))
    super(BlobStream, self).write(blob)

  def __iter__(self):
    return self

  def next(self):
    d = self.read()
    if not d:
      raise StopIteration
    return d

  def read(self, n=1):
    """
    Try to read as many as possible, but no more than n blobs from file.
    """
    def read_block():
      size_s = super(BlobStream, self).read(4)
      if len(size_s) < 4:
        raise IOError('bad block size')
      size = struct.unpack('i', size_s)[0]
      b = super(BlobStream, self).read(size)
      if len(b) < size:
        raise IOError('not enough data for blob')
      return b
    results = []
    while len(results) < n:
      magic = super(BlobStream, self).read(len(self.MAGIC))
      if not magic:
        break
      if magic != self.MAGIC:
        raise IOError('bad magic')
      results.append(read_block())
    else:
      return results if n > 1 else results[0]


class BlobStreamWriter(BlobStream):
  def __init__(self, fname):
    super(BlobStreamWriter, self).__init__(fname, mode='w')


class BlobStreamReader(BlobStream):
  def __init__(self, fname):
    super(BlobStreamReader, self).__init__(fname, mode='r')
