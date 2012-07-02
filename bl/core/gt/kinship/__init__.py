# BEGIN_COPYRIGHT
# END_COPYRIGHT

"""
Tools for computing the kinship matrix of a set of genotypes.

The reference implementation is the ``ibs`` function from `GenABEL
<http://www.genabel.org>`_.
"""

import operator, itertools as it, struct
import numpy as np
from scipy.lib.blas import fblas


DTYPE = np.dtype(np.float32)


def count_alleles(allele_pairs):
  count = {}
  for a in it.chain(*allele_pairs):
    if a not in "0N":
      count[a] = count.get(a, 0) + 1
  return count


def compute_genotype_codes(m, M):
  codes = {'00': np.NaN, 'NN': np.NaN, M+M: 1.0}
  if m is not None:
    codes.update({m+m: 0.0, m+M: 0.5, M+m: 0.5})
  return codes


def encode_genotypes(line, m, M):
  genotype_codes = compute_genotype_codes(m, M)
  for i in xrange(len(line)):
    line[i] = genotype_codes[line[i]]


def check_size(seq, size):
  if len(seq) != size:
    raise ValueError("size mismatch (%d != %d)" % (len(seq), size))


class KinshipVectors(object):

  VECTORS = "obs_hom", "exp_hom", "present"
  TRIANGLES = "lower_v", "upper_v"
  SIZE_FORMAT = "%sI" % DTYPE.byteorder

  def __init__(self, *args):
    if len(args) == 1:
      self.size = args[0]
      self.__from_scratch()
    elif len(args) == 5:
      self.size = len(args[0])
      self.__from_vectors(args)
    else:
      raise TypeError("wrong number of arguments")

  def __from_scratch(self):
    for n in self.VECTORS:
      setattr(self, n, np.zeros(self.size, dtype=DTYPE))
    for n in self.TRIANGLES:
      setattr(self, n, [np.zeros(i, dtype=DTYPE)
                        for i in xrange(self.size-1, 0, -1)])

  def __from_vectors(self, vectors):
    for i, n in enumerate(self.VECTORS):
      check_size(vectors[i], self.size)
      setattr(self, n, vectors[i])
    for i, n in enumerate(self.TRIANGLES):
      check_size(vectors[i+3], self.size-1)
      for j in xrange(self.size-1, 0, -1):
        check_size(vectors[i+3][self.size-1-j], j)
      setattr(self, n, vectors[i+3])

  def __len__(self):
    return self.size

  def __eq__(self, other):
    for n in self.VECTORS:
      if not np.array_equal(getattr(self, n), getattr(other, n)):
        return False
    for n in self.TRIANGLES:
      for d_v, v in it.izip(getattr(self, n), getattr(other, n)):
        if not np.array_equal(d_v, v):
          return False
    return True

  def __ne__(self, other):
    return not self.__eq__(other)

  def __iadd__(self, other):
    check_size(other, self.size)
    for n in self.VECTORS:
      setattr(self, n, getattr(self, n)+getattr(other, n))
    for n in self.TRIANGLES:
      for old_v, v in it.izip(getattr(self, n), getattr(other, n)):
        old_v += v
    return self

  def serialize(self):
    parts = [struct.pack(self.SIZE_FORMAT, self.size)]
    for n in self.VECTORS:
      parts.append(getattr(self, n).tostring())
    for n in self.TRIANGLES:
      parts.extend([v.tostring() for v in getattr(self, n)])
    return "".join(parts)

  @classmethod
  def deserialize(cls, s):
    N = struct.unpack_from(cls.SIZE_FORMAT, s)[0]
    O = struct.calcsize(cls.SIZE_FORMAT)
    S = DTYPE.itemsize
    vectors = [np.fromstring(s[i:i+S*N], dtype=DTYPE)
               for i in xrange(O, O+3*S*N, S*N)]
    O += 3*S*N
    t_size = S*((N-1)*N/2)
    base_steps = S * np.hstack(([0], np.cumsum(xrange(N-1, 0, -1))))
    for i in xrange(O, O+2*t_size, t_size):
      steps = i + base_steps
      indices = it.izip(steps[:-1], steps[1:])
      vectors.append([np.fromstring(s[j:k], dtype=DTYPE) for j, k in indices])
    return cls(*vectors)


# y = a*x + y --> fblas.saxpy(x, y, x.size, a)
# axpy(x, y, n=(len(x)-offx)/abs(incx), a=1.0, offx=0, incx=1, offy=0, incy=1)

class KinshipBuilder(object):

  def __init__(self, *args):
    if isinstance(args[0], KinshipVectors):
      self.vectors = args[0]
    else:
      self.vectors = KinshipVectors(*args)
    self.N = self.vectors.size
    for n in "obs_hom", "exp_hom", "present", "lower_v", "upper_v":
      setattr(self, n, getattr(self.vectors, n))

  def add_contribution(self, gt_vector):
    allele_count = count_alleles(gt_vector)
    if len(allele_count) < 2:
      return
    (m, mcount), (M, Mcount) = sorted(allele_count.iteritems(),
                                      key=operator.itemgetter(1))
    encode_genotypes(gt_vector, m, M)
    nm = float(mcount+Mcount)
    p = Mcount / nm
    pq = p * (1-p)
    nm /= 2  # number of non-missing genotypes
    gt_vector = np.array(gt_vector, dtype=DTYPE)
    nan_mask = np.isnan(gt_vector)
    if nm > 1:
      self.present += ~nan_mask
      self.obs_hom += ~nan_mask & (gt_vector != 0.5)
      self.exp_hom[~nan_mask] += 1.0 - 2*pq*nm/(nm-1)
    gt_vector -= p
    np.putmask(gt_vector, nan_mask, 0.)
    measured = (~nan_mask).astype(DTYPE)
    for i in xrange(self.N-1):
      fblas.saxpy(gt_vector, self.lower_v[i], self.N-i-1, gt_vector[i]/pq, i+1)
      fblas.saxpy(measured, self.upper_v[i], self.N-i-1, measured[i], i+1)

  def build(self):
    k = np.zeros((self.N, self.N), dtype=DTYPE)
    diag = .5 + (self.obs_hom - self.exp_hom) / (self.present - self.exp_hom)
    np.putmask(k, np.eye(self.N), diag)
    for i, (lv, uv) in enumerate(it.izip(self.lower_v, self.upper_v)):
      lv /= uv
      lv[uv==0.] = -1.
      k[i+1:,i] = lv
      k[i,i+1:] = uv
    return k

  @classmethod
  def serialize(cls, k):
    return k.tostring()

  @classmethod
  def deserialize(cls, s_k):
    k = np.fromstring(s_k, dtype=DTYPE)
    N = int(np.sqrt(k.size))
    k.shape = (N, N)
    return k


def kinship(line_stream, comment="\n"):
  """
  Compute the kinship matrix for the genotypes in ``line_stream``.
  """
  v_allocated = False
  for line in line_stream:
    if line.startswith(comment):
      continue
    line = line.rstrip().split()
    if not v_allocated:
      n_individuals = len(line)
      builder = KinshipBuilder(n_individuals)
      v_allocated = True
    builder.add_contribution(line)
  if v_allocated:
    return builder.build()
  else:
    return None
