#!/usr/bin/env python
# BEGIN_COPYRIGHT
# END_COPYRIGHT

"""
Read a FASTA file and compute average zlib compression rates for all
compression levels. Output is tabular with three fields: compression
level, header compression factor, sequence compression factor.
"""

import sys, os, zlib, itertools
from bl.core.seq.io.fasta import RawFastaReader


def get_data(fasta_fn):
  f = open(fasta_fn)
  offset, size = 0, os.fstat(f.fileno()).st_size
  reader = RawFastaReader(f, offset, size)
  headers, seqs = [l for l in itertools.izip(*reader)]
  f.close()
  return headers, seqs


class RateCalculator(object):

  def __init__(self, headers, seqs):
    self.headers = headers
    self.seqs = seqs
    self.header_lengths = [float(len(h)) for h in headers]
    self.seq_lengths = [float(len(s)) for s in seqs]
    
  def get_average_rates(self, level):
    n = len(self.headers)
    rates = {"h": [], "s": []}
    for h, hl, s, sl in itertools.izip(self.headers, self.header_lengths,
                                       self.seqs, self.seq_lengths):
      rates["h"].append(hl/len(zlib.compress(h, level)))
      rates["s"].append(sl/len(zlib.compress(s, level)))
    return sum(rates["h"])/n, sum(rates["s"])/n


def main(argv):
  try:
    fasta_fn = argv[1]
  except IndexError:
    sys.exit("USAGE: %s FASTA_FN\n%s" % (argv[0], __doc__))
  headers, seqs = get_data(fasta_fn)
  rc = RateCalculator(headers, seqs)
  for level in xrange(1, 10):
    hdr_rate, seq_rate = rc.get_average_rates(level)
    print level, hdr_rate, seq_rate


if __name__ == "__main__":
  main(sys.argv)
