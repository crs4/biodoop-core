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
