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

import sys, os, shutil
from bl.core.seq.io.fasta import RawFastaReader


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
