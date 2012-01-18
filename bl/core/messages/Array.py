# BEGIN_COPYRIGHT
# END_COPYRIGHT

import numpy as np

from details.Array_pb2 import Array
from details import load_array, unload_array


def Array_to_msg(x):
  assert isinstance(x, np.ndarray)
  a = Array()
  load_array(a, x)
  return a.SerializeToString()

def msg_to_Array(msg):
  a = Array()
  a.ParseFromString(msg)
  x = unload_array(a)
  return x
