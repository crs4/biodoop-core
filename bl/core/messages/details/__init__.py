import numpy as np

def load_array(a, x):
  assert isinstance(x, np.ndarray)
  dtype = x.dtype
  a.type_name = '%r'  % dtype
  a.byte_order = x.dtype.byteorder
  a.dims       = len(x.shape)
  for d in x.shape:
    a.shape.append(d)
  a.data = x.tostring()

def unload_array(a):
  dtype = np.dtype(eval('np.' + a.type_name))
  x = np.fromstring(a.data, dtype=dtype)
  x.shape = tuple(a.shape)
  assert len(x.shape) == a.dims
  return x


