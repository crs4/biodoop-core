# BEGIN_COPYRIGHT
# END_COPYRIGHT
import os


BUFSIZE = 4096


class FastaError(Exception):

  def __init__(self, msg):
    self.msg = msg

  def __str__(self):
    return self.msg


def find_first_record(f, offset, split_size):
  """
  Find position of first fasta record in f, in the range (offset,
  offset+split_size); return position or -1 if not found in range.

  NOTE: File pointer position after search is UNDEFINED.
  """
  bytes_read = 0
  if offset:
    f.seek(offset)
  pos = -1
  while pos < 0 and bytes_read <= split_size:
    chunk = f.read(BUFSIZE)
    if chunk == "":
      break
    rel_pos = chunk.find(">", 0, split_size-bytes_read)
    if rel_pos >= 0:
      pos = rel_pos + offset + bytes_read
      break
    else:
      bytes_read += len(chunk)
  return pos


class RawFastaReader(object):
  """
  Split-aware raw FASTA reader.

  Default values for offset and split_size are intended for usage on a
  (whole) regular file.
  """
  def __init__(self, f, offset=0, split_size=None):
    if split_size is None:
      try:
        fd = f.fileno()
      except AttributeError:
        raise TypeError("if split_size is None, f must have a descriptor")
      else:
        split_size = os.fstat(fd).st_size
    p = find_first_record(f, offset, split_size)
    if p < 0:
      p = offset + split_size
    f.seek(p)
    self.__bytes_read = p - offset
    self.f = f
    self.split_size = split_size
    self.chunk = ""
    self.chunk_p = 0
    self.next_p = -1
    self.record = []

  def __iter__(self):
    return self

  def next(self):
    if self.finished():
      raise StopIteration
    if not self.chunk:
      self.chunk = self.f.read(BUFSIZE)
      if not self.chunk:
        raise StopIteration
      self.chunk_p = 0
    self.next_p = self.chunk.find(">", self.chunk_p+1)
    while self.next_p < 0:
      s = self.chunk[self.chunk_p:]
      self.record.append(s)
      self.__bytes_read += len(s)
      self.chunk = self.f.read(BUFSIZE)
      if not self.chunk:
        self.next_p = 0
        break
      self.chunk_p = 0
      self.next_p = self.chunk.find(">", self.chunk_p)
    s = self.chunk[self.chunk_p:self.next_p]
    self.record.append(s)
    self.__bytes_read += len(s)
    self.chunk_p = self.next_p
    rec = "".join(self.record)
    self.record = []
    try:
      header, rec = rec.split("\n", 1)
    except ValueError:
      raise FastaError('Bad fasta entry "%s"' % rec)
    return header[1:], rec.replace("\n", "")

  @property
  def bytes_read(self):
    return self.__bytes_read

  def finished(self):
    return self.__bytes_read >= self.split_size
