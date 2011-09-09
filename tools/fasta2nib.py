#!/usr/bin/env python
# BEGIN_COPYRIGHT
# END_COPYRIGHT

"""
Convert FASTA sequences to the UCSC .nib format. This program takes as
input the name of a directory where sequences are stored in the FASTA
format (only .fa and .fasta extensions are taken into account), with
one sequence per file (any other sequences will be ignored), and the
name of a directory where corresponding .nib files will be written.

Note that sequences are fully read into memory.
"""

import sys, os, errno
from contextlib import nested
from bl.core.seq.io import RawFastaReader
from bl.core.seq.utils import seq2nib


def main(argv):
  
  if len(argv) < 3:
    print "USAGE: %s IN_DIR OUT_DIR" % argv[0]
    print __doc__
    sys.exit(2)
  in_dir = argv[1]
  out_dir = argv[2]

  try:
    os.makedirs(out_dir)
  except OSError, e:
    if e.errno != errno.EEXIST:
      sys.exit("could not create %s: %s" % (out_dir, e))

  filenames = [os.path.join(in_dir, fn) for fn in os.listdir(in_dir)
               if fn.endswith(".fa") or fn.endswith(".fasta")]
  print "found %d FASTA files in %s" % (len(filenames), in_dir)
  for fn in filenames:
    outbn = "%s.nib" % os.path.splitext(os.path.basename(fn))[0]
    outfn = os.path.join(out_dir, outbn)
    print "%s --> %s" % (fn, outfn)
    with nested(open(fn), open(outfn, "wb")) as (f, outf):
      reader = RawFastaReader(f)
      _, seq = reader.next()
      outf.write(seq2nib(seq))


if __name__ == "__main__":
  main(sys.argv)
