# BEGIN_COPYRIGHT
# 
# Copyright (C) 2009-2013 CRS4.
# 
# This file is part of biodoop-core.
# 
# biodoop-core is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
# 
# biodoop-core is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
# 
# You should have received a copy of the GNU General Public License along with
# biodoop-core.  If not, see <http://www.gnu.org/licenses/>.
# 
# END_COPYRIGHT

import unittest, operator
from itertools import izip
import numpy as np

import bl.core.gt.kinship as kinship


NO_MISSING = (
  # data
  ["AC AC AA\n",
   "GT TT TT\n",
   "TA AT TA\n"],
  # allele count
  [{'C': 2, 'A': 4},
   {'G': 1, 'T': 5},
   {'A': 3, 'T': 3}],
  # encoding
  [[0.5, 0.5, 1.0],
   [0.5, 1.0, 1.0],
   [0.5, 0.5, 0.5]],
  # kinship matrix
  np.array([[ -3./22 ,  3.   ,  3.   ],
            [-11./120,  9./22,  3.   ],
            [-13./60 , -1./60, 21./22]], dtype=kinship.DTYPE)
  )

MISSING = [
  # data
  ["AC 00 AA\n",
   "GT TT TT\n",
   "TA AT 00\n"],
  # allele count
  [{'C': 1, 'A': 3},
   {'G': 1, 'T': 5},
   {'A': 2, 'T': 2}],
  # encoding
  [[0.5, np.NaN, 1.0],
   [0.5,  1.0,   1.0],
   [0.5,  0.5,  np.NaN]],
  # kinship matrix
  np.array([[  3./26,  2.   , 2.  ],
            [ -1./5 , 27./34, 1.  ],
            [-11./30,  1./5 , 3./2]], dtype=kinship.DTYPE)
  ]

MISSING_LINE = [
  # data
  ["AC 00 AA\n",
   "GT TT TT\n",
   "00 00 00\n"],
  # allele count
  [{'C': 1, 'A': 3},
   {'G': 1, 'T': 5},
   {}],
  # encoding
  [[0.5   , np.NaN,  1.0  ],
   [0.5   ,  1.0  ,  1.0  ],
   [np.NaN, np.NaN, np.NaN]],
  # kinship matrix (FIXME - add analytical result, this is from R)
  np.array([[-0.2142857, 1.0, 2.0],
            [-0.4000000, 1.5, 1.0],
            [-0.3666667, 0.2, 1.5]], dtype=kinship.DTYPE)
  ]


TWO_MISSING = [
  # data
  ["AC 00 AA\n",
   "GT TT TT\n",
   "TA 00 00\n"],
  # allele count
  [{'C': 1, 'A': 3},
   {'G': 1, 'T': 5},
   {'T': 1, 'A': 1}],
  # encoding
  [[0.5, np.NaN,  1.0  ],
   [0.5,  1.0  ,  1.0  ],
   [0.5, np.NaN, np.NaN]],
  # kinship matrix (FIXME - add analytical result, this is from R)
  np.array([[-0.2142857, 1.0, 2.0],
            [-0.4000000, 1.5, 1.0],
            [-0.3666667, 0.2, 1.5]], dtype=kinship.DTYPE)
  ]

MONOMORPHIC = (
  # data
  ["AC AC AA\n",
   "TT TT TT\n",
   "TA AT TA\n"],
  # allele count
  [{'C': 2, 'A': 4},
   {'T': 6},
   {'A': 3, 'T': 3}],
  # encoding
  [[0.5, 0.5, 1.0],
   [1.0, 1.0, 1.0],
   [0.5, 0.5, 0.5]],
  # kinship matrix (FIXME - add analytical result, this is from R)
  np.array([[0.0882352941176471, 2, 2],
            [0.0625, 0.0882352941176471, 2],
            [-0.125,  -0.125, 0.794117647058824]], dtype=kinship.DTYPE)
  )


def make_vectors(n, dtype):
  vectors = [np.random.random(n).astype(dtype) for _ in xrange(3)]
  for _ in xrange(2):
    vectors.append([])
    for i in xrange(n-1, 0, -1):
      vectors[-1].append(np.random.random(i).astype(dtype))
  return vectors


class TestKinshipVectors(unittest.TestCase):

  N = 5
  DTYPE = kinship.DTYPE

  def test_iadd(self):
    vectors = make_vectors(self.N, self.DTYPE)
    inc_vectors = make_vectors(self.N, self.DTYPE)
    exp_vectors = [vectors[i]+inc_vectors[i] for i in xrange(3)]
    for i in xrange(3, 5):
      exp_vectors.append([sum(t) for t in izip(vectors[i], inc_vectors[i])])
    vectors, inc_vectors, exp_vectors = [
      kinship.KinshipVectors(*_) for _ in vectors, inc_vectors, exp_vectors
      ]
    vectors += inc_vectors    
    self.assertEqual(vectors, exp_vectors)

  def test_serialize(self):
    vectors = make_vectors(self.N, self.DTYPE)
    kv = kinship.KinshipVectors(*vectors)
    s_kv = kv.serialize()
    d_kv = kinship.KinshipVectors.deserialize(s_kv)
    self.assertEqual(d_kv, kv)


class TestKinship(unittest.TestCase):

  def __test_count_alleles(self, f, expected_count):
    for line, ec in izip(f, expected_count):
      line = line.rstrip().split()
      self.assertEqual(kinship.count_alleles(line), ec)

  def __test_encode_genotypes(self, f, expected_codes):
    for line, ec in izip(f, expected_codes):
      line = line.rstrip().split()
      allele_count = kinship.count_alleles(line)
      if len(allele_count) < 2:
        continue
      (m, _), (M, _) = sorted(
          kinship.count_alleles(line).iteritems(),
          key=operator.itemgetter(1)
          )
      kinship.encode_genotypes(line, m, M)
      for x, exp_x in izip(line, ec):
        if not np.isnan(exp_x):
          self.assertEqual(x, exp_x)

  def __test_kinship(self, f, expected_k):
    k = kinship.kinship(f)  # TODO: add tests for KinshipBuilder.build
    self.assertEqual(k.shape, expected_k.shape)
    for i in xrange(k.shape[0]):
      for j in xrange(k.shape[0]):
        self.assertAlmostEqual(k[i,j], expected_k[i,j], 5)

  def __test_all(self, f, expected_count, expected_codes, expected_k):
    self.__test_count_alleles(f, expected_count)
    self.__test_encode_genotypes(f, expected_codes)
    self.__test_kinship(f, expected_k)

  def test_no_missing(self):
    self.__test_all(*NO_MISSING)

  def test_missing(self):
    self.__test_all(*MISSING)

  def test_missing_line(self):
    self.__test_all(*MISSING_LINE)

  def test_two_missing(self):
    self.__test_all(*TWO_MISSING)

  def test_monomorphic(self):
    self.__test_all(*MONOMORPHIC)

  def test_serialize(self):
    for tc in NO_MISSING, MISSING, MISSING_LINE, TWO_MISSING, MONOMORPHIC:
      k = tc[-1]
      s_k = kinship.KinshipBuilder.serialize(k)
      d_k = kinship.KinshipBuilder.deserialize(s_k)
      self.assertTrue(np.array_equal(d_k, k))


def load_tests(loader, tests, pattern):
  test_cases = (TestKinshipVectors, TestKinship)
  suite = unittest.TestSuite()
  for tc in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(tc))
  return suite


if __name__ == '__main__':
  suite = load_tests(unittest.defaultTestLoader, None, None)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
