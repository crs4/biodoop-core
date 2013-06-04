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

import numpy as np


def load_array(a, x):
  assert isinstance(x, np.ndarray)
  a.type_name = '%r' % x.dtype
  a.byte_order = x.dtype.byteorder
  a.dims = len(x.shape)
  for d in x.shape:
    a.shape.append(d)
  a.data = x.tostring()


def unload_array(a):
  dtype = eval('np.'+a.type_name)
  x = np.fromstring(a.data, dtype=dtype)
  x.shape = tuple(a.shape)
  assert len(x.shape) == a.dims
  return x
