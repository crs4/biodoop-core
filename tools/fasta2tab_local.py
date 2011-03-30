#!/usr/bin/env python
# BEGIN_COPYRIGHT
# END_COPYRIGHT

import sys, os, shutil
from bl.seq.io.fasta import RawFastaReader


def main(argv):
    if len(argv) < 3:
        print "USAGE: %s OUT_DIR FILE [FILE] ..." % argv[0]
        sys.exit(2)
    out_dir = argv[1]
    filenames = argv[2:]

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)
    for fn in filenames:
        outfn = os.path.join(out_dir, os.path.basename(fn))
        print "%r --> %r" % (fn, outfn)
        f = open(fn)
        reader = RawFastaReader(f)
        outf = open(outfn, "w")
        for header, seq in reader:
            outf.write("%s\t%s\n" % (header, seq))
        outf.close()
        f.close()


if __name__ == "__main__":
    main(sys.argv)
