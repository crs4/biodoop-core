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

from details.NamedArrayCollection_pb2 import NamedArrayCollection
from details import load_array, unload_array


def NamedArrayCollection_to_msg(my_id, xl):
  assert isinstance(my_id, str)
  assert isinstance(xl, list)
  nac = NamedArrayCollection()
  nac.id = my_id
  for x in xl:
    assert isinstance(x, np.ndarray)
    a = nac.array.add()
    load_array(a, x)
  return nac.SerializeToString()


def msg_to_NamedArrayCollection(msg):
  nac = NamedArrayCollection()
  nac.ParseFromString(msg)
  my_id = nac.id
  xl = []
  for a in nac.array:
    xl.append(unload_array(a))
  return (str(my_id), xl)
