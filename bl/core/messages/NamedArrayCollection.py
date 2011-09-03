#import details.NamedArrayCollection_pb2 as NamedArrayCollection_pb
from details.NamedArrayCollection_pb2 import NamedArrayCollection
from details import load_array
from details import unload_array

import numpy as np

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
