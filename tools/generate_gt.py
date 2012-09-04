#!/usr/bin/env python

"""
Generate random genotypes.  Ideally, this script should support the
automatic creation of twins, brothers and so on by means of
appropriate command line parameters.  For now, this is accomplished by
means of appropriate hacks.
"""

import sys, argparse
from random import choice

import numpy as np

from bl.core.utils.random_ext import sample_wr


def generate(n_snps, n_samples):
  # from itertools import product, combinations
  # [["".join(p) for p in product(_, _)] for _ in combinations("ACGT", 2)]
  gt_table = [
    ['AA', 'AC', 'CA', 'CC'],
    ['AA', 'AG', 'GA', 'GG'],
    ['AA', 'AT', 'TA', 'TT'],
    ['CC', 'CG', 'GC', 'GG'],
    ['CC', 'CT', 'TC', 'TT'],
    ['GG', 'GT', 'TG', 'TT'],
    ]
  gt_array = np.empty((n_snps, n_samples), dtype="|S2")
  for i in xrange(n_snps):
    pairs = choice(gt_table)
    gt_array[i,:] = sample_wr(pairs, n_samples)
  #--- hack: first two are twins ---
  assert n_samples > 1
  gt_array[:,1] = gt_array[:,0]
  #---------------------------------
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
  return parser


def main(argv):
  parser = make_parser()
  args = parser.parse_args(argv[1:])
  gt_array = generate(args.n_snps, args.n_samples)
  with open(args.output, "w") as fo:
    write(gt_array, fo)
  print "wrote %r" % (args.output,)


if __name__ == "__main__":
  main(sys.argv)
