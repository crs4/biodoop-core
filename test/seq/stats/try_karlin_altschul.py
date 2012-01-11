# BEGIN_COPYRIGHT
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
