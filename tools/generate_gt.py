#!/usr/bin/env python

"""
Generate random genotypes.  Ideally, this script should support the
automatic creation of twins, brothers and so on by means of
appropriate command line parameters.  For now, this is accomplished by
means of appropriate hacks.
"""

import sys, argparse
from random import choice
from itertools import izip

import numpy as np

from bl.core.utils.random_ext import sample_wr


# from itertools import combinations, combinations_with_replacement
# GT_TABLE = [["".join(c) for c in combinations_with_replacement(_, 2)]
#              for _ in combinations("ACGT", 2)]
GT_TABLE = [
  ['AA', 'AC', 'CC'],
  ['AA', 'AG', 'GG'],
  ['AA', 'AT', 'TT'],
  ['CC', 'CG', 'GG'],
  ['CC', 'CT', 'TT'],
  ['GG', 'GT', 'TT'],
  ]


def generate(n_snps, n_samples):
  """
  Generate random genotypes.
  """
  gt_array = np.empty((n_snps, n_samples), dtype="|S2")
  for i in xrange(n_snps):
    pairs = choice(GT_TABLE)
    gt_array[i,:] = sample_wr(pairs, n_samples)
  #--- hack: first two are twins ---
  assert n_samples > 1
  gt_array[:,1] = gt_array[:,0]
  #---------------------------------
  return gt_array


def colordump(gt_array):
  red = "\033[01;31m{0}\033[00m"
  n_snps = gt_array.shape[0]
  for i, row in enumerate(gt_array):
    for j, x in enumerate(row):
      if j > 1 and i > n_snps - j:
        print red.format(x),
      else:
        print x,
    print


def generate_spectrum(n_samples):
  """
  Generate genotypes that differ for an increasing number of loci.
  """
  n_snps = n_samples - 2
  gt_array = np.empty((n_snps, n_samples), dtype="|S2")
  pairs_list = [choice(GT_TABLE) for _ in xrange(n_snps)]
  orig_gt = [choice(p) for p in pairs_list]
  mismatch_list = [[_ for _ in pl if _ != p]
                   for pl, p in izip(pairs_list, orig_gt)]
  gt_array[:,0] = gt_array[:,1] = orig_gt
  for i in xrange(2, n_samples):
    gt_array[:-i+1,i] = orig_gt[:-i+1]
    gt_array[-i+1:,i] = [choice(_) for _ in mismatch_list[-i+1:]]
  ## colordump(gt_array)  # activate only for small arrays!
  return gt_array


def write(gt_array, f):
  for row in gt_array:
    row.tofile(f, sep=" ")
    f.write("\n")


def make_parser():
  parser = argparse.ArgumentParser(description="generate random genotypes")
  parser.add_argument("-o", "--output", metavar="FILE", default="random.gt",
                      help="output file name")
  parser.add_argument("--n-samples", type=int, metavar="INT", default=20,
                      help="number of samples")
  parser.add_argument("--n-snps", type=int, metavar="INT", default=10000,
                      help="number of SNPs")
  parser.add_argument("--spectrum", action="store_true",
                      help="generate full spectrum (n_snps is ignored)")
  return parser


def main(argv):
  parser = make_parser()
  args = parser.parse_args(argv[1:])
  if args.spectrum:
    gt_array = generate_spectrum(args.n_samples)
  else:
    gt_array = generate(args.n_snps, args.n_samples)
  with open(args.output, "w") as fo:
    write(gt_array, fo)
  print "wrote %r" % (args.output,)


if __name__ == "__main__":
  main(sys.argv)
