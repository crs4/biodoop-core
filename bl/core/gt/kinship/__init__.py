# BEGIN_COPYRIGHT
# END_COPYRIGHT

"""
Tools for computing the kinship matrix of a set of genotypes.

This is essentially a reimplementation of the ``ibs`` function from
`GenABEL <http://www.genabel.org>`_.
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

def kinship(line_stream, comment="\n"):
  """
  Compute kinship matrix.

  Return number of lines read and kinsh4ip vectors.
  """
  v_allocated = False
  for line in line_stream:
    if line.startswith(comment):
      continue
    line = line.rstrip().split()
    if not v_allocated:
      n_individuals = len(line)
      lower_v = [np.zeros(i, dtype=np.float32)
                 for i in xrange(n_individuals-1, 0, -1)]
      upper_v = [np.zeros(i, dtype=np.float32)
                 for i in xrange(n_individuals-1, 0, -1)]
      obs_hom = np.zeros(n_individuals, dtype=np.float32)
      exp_hom = np.zeros(n_individuals, dtype=np.float32)
      present = np.zeros(n_individuals, dtype=np.float32)
      v_allocated = True
    allele_count = count_alleles(line)
    if len(allele_count) < 2:
      continue
    (m, mcount), (M, Mcount) = sorted(allele_count.iteritems(),
                                      key=operator.itemgetter(1))
    encode_genotypes(line, m, M)
    nm = float(mcount+Mcount)
    p = Mcount / nm
    pq = p * (1-p)
    nm /= 2  # number of non-missing genotypes
    line = np.array(line, dtype=np.float32)
    nan_mask = np.isnan(line)
    if nm > 1:
      present += ~nan_mask
      obs_hom += ~nan_mask & (line != 0.5)
      exp_hom[~nan_mask] += 1.0 - 2*pq*nm/(nm-1)
    line -= p
    np.putmask(line, nan_mask, 0.)
    measured = (~nan_mask).astype(np.float32)
    for i in xrange(n_individuals-1):
      fblas.saxpy(line, lower_v[i], n_individuals-i-1, line[i]/pq, i+1)
      fblas.saxpy(measured, upper_v[i], n_individuals-i-1, measured[i], i+1)
  if v_allocated:
    return obs_hom, exp_hom, present, lower_v, upper_v
  else:
    return None


def build_k(obs_hom, exp_hom, present, lower_v, upper_v):
  N = obs_hom.size
  assert exp_hom.size == present.size == N
  assert lower_v[0].size == upper_v[0].size == N-1
  assert len(lower_v) == len(upper_v) == N-1
  k = np.zeros((N,N))
  diag = .5 + (obs_hom-exp_hom) / (present-exp_hom)
  np.putmask(k, np.eye(N), diag)
  for i, (lv, uv) in enumerate(it.izip(lower_v, upper_v)):
    lv /= uv
    lv[uv==0.] = -1.
    k[i+1:,i] = lv
    k[i,i+1:] = uv
  return k
