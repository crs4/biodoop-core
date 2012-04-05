# BEGIN_COPYRIGHT
# END_COPYRIGHT

"""
Tools for computing the kinship matrix of a set of genotypes.

The reference implementation is the ``ibs`` function from `GenABEL
<http://www.genabel.org>`_.
"""

import operator, itertools as it
import numpy as np
from scipy.lib.blas import fblas


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


# y = a*x + y --> fblas.saxpy(x, y, x.size, a)
# axpy(x, y, n=(len(x)-offx)/abs(incx), a=1.0, offx=0, incx=1, offy=0, incy=1)

class KinshipBuilder(object):

  def __init__(self, n_individuals):
    self.lower_v = [np.zeros(i, dtype=np.float32)
                    for i in xrange(n_individuals-1, 0, -1)]
    self.upper_v = [np.zeros(i, dtype=np.float32)
                    for i in xrange(n_individuals-1, 0, -1)]
    self.obs_hom = np.zeros(n_individuals, dtype=np.float32)
    self.exp_hom = np.zeros(n_individuals, dtype=np.float32)
    self.present = np.zeros(n_individuals, dtype=np.float32)
    self.N = n_individuals

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
    gt_vector = np.array(gt_vector, dtype=np.float32)
    nan_mask = np.isnan(gt_vector)
    if nm > 1:
      self.present += ~nan_mask
      self.obs_hom += ~nan_mask & (gt_vector != 0.5)
      self.exp_hom[~nan_mask] += 1.0 - 2*pq*nm/(nm-1)
    gt_vector -= p
    np.putmask(gt_vector, nan_mask, 0.)
    measured = (~nan_mask).astype(np.float32)
    for i in xrange(self.N-1):
      fblas.saxpy(gt_vector, self.lower_v[i], self.N-i-1, gt_vector[i]/pq, i+1)
      fblas.saxpy(measured, self.upper_v[i], self.N-i-1, measured[i], i+1)

  def build(self):
    k = np.zeros((self.N, self.N))
    diag = .5 + (self.obs_hom - self.exp_hom) / (self.present - self.exp_hom)
    np.putmask(k, np.eye(self.N), diag)
    for i, (lv, uv) in enumerate(it.izip(self.lower_v, self.upper_v)):
      lv /= uv
      lv[uv==0.] = -1.
      k[i+1:,i] = lv
      k[i,i+1:] = uv
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
