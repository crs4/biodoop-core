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

import sys, os, logging
from subprocess import Popen, PIPE
from bl.core.seq.stats.karlin_altschul import BlastallLKCalculator


ENGINE_OPTS = {"blastall.program": "blastn"}


if __name__ == "__main__":
  formatdb_exe = os.getenv("BL_FORMATDB_EXE", "/usr/bin/formatdb").strip()
  blastall_exe = os.getenv("BL_BLASTALL_EXE", "/usr/bin/blastall").strip()
  for exe in formatdb_exe, blastall_exe:
    if not (os.path.isfile(exe) and os.access(exe, os.X_OK)):
      sys.exit("%s not found or not executable" % exe)
  calculator = BlastallLKCalculator(
    formatdb_exe,
    blastall_exe,
    log_level=logging.DEBUG,
    engine_opts=ENGINE_OPTS,
    )
  lambda_, k = calculator.calculate()
  print "engine options: %r" % ENGINE_OPTS
  print "lambda, k = %f, %f" % (lambda_, k)
