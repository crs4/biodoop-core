# BEGIN_COPYRIGHT
# END_COPYRIGHT
import sys, logging
from subprocess import Popen, PIPE
from bl.core.seq.stats.karlin_altschul import BlastallLKCalculator


ENGINE_OPTS = {"blastall.program": "blastn"}


formatdb_exe, err = Popen("which formatdb", shell=True,
                          stdout=PIPE, stderr=PIPE).communicate()
if err:
  sys.exit("formatdb executable not found")
formatdb_exe = formatdb_exe.strip()
blastall_exe, err = Popen("which blastall", shell=True,
                          stdout=PIPE, stderr=PIPE).communicate()
if err:
  sys.exit("blastall executable not found")
blastall_exe = blastall_exe.strip()


calculator = BlastallLKCalculator(
  formatdb_exe,
  blastall_exe,
  log_level=logging.DEBUG,
  engine_opts=ENGINE_OPTS,
  )

lambda_, k = calculator.calculate()

print "engine options: %r" % ENGINE_OPTS
print "lambda, k = %f, %f" % (lambda_, k)
