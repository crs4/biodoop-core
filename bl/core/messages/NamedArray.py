# BEGIN_COPYRIGHT
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
