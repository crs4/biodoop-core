from details.Array_pb2 import Array as Array

#import details.Array_pb2 as Array_pb
from details import load_array
from details import unload_array

import numpy as np

#
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
