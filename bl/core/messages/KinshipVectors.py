# BEGIN_COPYRIGHT
# END_COPYRIGHT

from details.KinshipVectors_pb2 import KinshipVectors
from details import load_array, unload_array


def KinshipVectors_to_msg(obs_hom, exp_hom, present, lower_v, upper_v):
  args = locals().copy()
  msg = KinshipVectors()
  for k, v in args.iteritems():
    slot = getattr(msg, k)
    if not k.endswith("_v"):
      load_array(slot, v)
    else:
      for x in v:
        load_array(slot.add(), x)
  return msg.SerializeToString()


def msg_to_KinshipVectors(msg):
  vectors = KinshipVectors()
  vectors.ParseFromString(msg)
  res = []
  for k in "obs_hom", "exp_hom", "present":
    res.append(unload_array(getattr(vectors, k)))
  for k in "lower_v", "upper_v":
    res.append([])
    for x in getattr(vectors, k):
      res[-1].append(unload_array(x))
  return tuple(res)
