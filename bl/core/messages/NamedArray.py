
#import details.NamedArray_pb2 as NamedArray_pb
from details.NamedArray_pb2 import NamedArray
from details import load_array
from details import unload_array

import numpy as np

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
