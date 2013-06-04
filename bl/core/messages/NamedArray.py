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

from details.NamedArray_pb2 import NamedArray
from details import load_array, unload_array


def NamedArray_to_msg(my_id, x):
  assert isinstance(my_id, str)
  assert isinstance(x, np.ndarray)
  na = NamedArray()
  na.id = my_id
  load_array(na.array, x)
  return na.SerializeToString()


def msg_to_NamedArray(msg):
  na = NamedArray()
  na.ParseFromString(msg)
  my_id = na.id
  x = unload_array(na.array)
  return (str(my_id), x)
