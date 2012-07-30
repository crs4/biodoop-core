# BEGIN_COPYRIGHT
# END_COPYRIGHT

"""
Transpose a tab-separated text matrix without preserving final row ordering.

  pydoop script -t '' transpose_random_rows.py INPUT OUTPUT

The output matrix can be fed directly to the kinship application.
"""

import struct

def mapper(key, value, writer):
  value = value.split()
  for i, a in enumerate(value):
    writer.emit(struct.pack(">q", i), "%s%s" % (key, a))

def reducer(key, ivalue, writer):
  vector = [v for v in ivalue]
  vector.sort(key=lambda v: struct.unpack(">q", v[:8])[0])
  writer.emit("", "\t".join(v[8:] for v in vector))
