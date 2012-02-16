# BEGIN_COPYRIGHT
# END_COPYRIGHT


import struct


class BlobStream(object):
  
  MAGIC = 'BLOB_MAGIC-0.0'

  def __init__(self, f, mode='r'):
    if isinstance(f, basestring):
      self.f = open(f, mode)
    else:
      self.f = f
    self.closed = self.f.closed

  def __complain_if_closed(self):
    if self.closed:
      raise ValueError("I/O operation on closed object")

  def write(self, blob):
    self.__complain_if_closed()
    self.f.write(self.MAGIC)
    self.f.write(struct.pack('i', len(blob)))
    self.f.write(blob)

  def read(self, n=1):
    """
    Try to read as many as possible, but no more than n blobs from f.
    """
    self.__complain_if_closed()
    results = []
    while len(results) < n:
      magic = self.f.read(len(self.MAGIC))
      if not magic:
        break
      if magic != self.MAGIC:
        raise IOError('bad magic')
      results.append(self.__read_block())
    else:
      return results if n > 1 else results[0]

  def __read_block(self):
    size_s = self.f.read(4)
    if len(size_s) < 4:
      raise IOError('bad block size')
    size = struct.unpack('i', size_s)[0]
    b = self.f.read(size)
    if len(b) < size:
      raise IOError('not enough data for blob')
    return b

  def close(self):
    if not self.closed:
      self.closed = True
      return self.f.close()

  def __iter__(self):
    return self

  def next(self):
    d = self.read()
    if not d:
      raise StopIteration
    return d

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.close()


class BlobStreamWriter(BlobStream):
  def __init__(self, f):
    super(BlobStreamWriter, self).__init__(f, mode='w')


class BlobStreamReader(BlobStream):
  def __init__(self, f):
    super(BlobStreamReader, self).__init__(f, mode='r')
