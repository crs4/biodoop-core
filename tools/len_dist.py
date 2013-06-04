#!/usr/bin/env python
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

import sys, os, optparse, operator
import matplotlib.pyplot as plt

from bl.core.seq.io.fasta import RawFastaReader


def get_lengths(files):
  lengths = []
  for i, fn in enumerate(files):
    print "processing %r (%d/%d)" % (fn, i, len(files))
    f = open(fn)
    reader = RawFastaReader(f)
    for header, seq in reader:
      lengths.append(len(seq))
    f.close()
  return lengths


def plot_histo(lengths, fn, **kw):
  plt.hist(lengths, **kw)
  plt.grid(True)
  plt.title("seq len distribution")
  plt.draw()
  plt.savefig(fn, dpi=300)


def dump_full_histo(lengths, dumpfn):
  data = {}
  f = open(dumpfn, "w")
  for l in lengths:
    data[l] = data.get(l, 0) + 1
  for i in sorted(data.iteritems(), key=operator.itemgetter(1), reverse=True):
    f.write("%d\t%d\n" % i)
  f.close()


def make_parser():
  parser = optparse.OptionParser(usage="%prog [OPTIONS] FILE [FILE]...")
  parser.add_option("-o", type="str", dest="outfn", metavar="STRING",
                    help="output file name [%default]", default="len_dist.png")
  parser.add_option("-b", type="int", dest="bins", metavar="INT",
                    help="number of bins for histogram")
  parser.add_option("-d", type="str", dest="dumpfn", metavar="STRING",
                    help="dump file name [none]")
  return parser


def main(argv):

  kw = {}

  parser = make_parser()
  opt, args = parser.parse_args()
  if len(args) < 1:
    parser.print_help()
    sys.exit(2)
  if opt.bins:
    kw["bins"] = opt.bins
  
  lengths = get_lengths(args)
  print "generating img"
  plot_histo(lengths, opt.outfn, **kw)
  if opt.dumpfn:
    print "dumping full data to %r" % opt.dumpfn
    dump_full_histo(lengths, opt.dumpfn)


if __name__ == "__main__":
  main(sys.argv)
