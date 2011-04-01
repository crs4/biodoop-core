# BEGIN_COPYRIGHT
# END_COPYRIGHT
import logging
from bl.core.seq.stats.karlin_altschul import BlastallLKCalculator


ENGINE_OPTS = {"blastall.program": "blastn"}


calculator = BlastallLKCalculator(
  "/usr/bin/formatdb",
  "/usr/bin/blastall",
  log_level=logging.DEBUG,
  engine_opts=ENGINE_OPTS,
  )

lambda_, k = calculator.calculate()

print "engine options: %r" % ENGINE_OPTS
print "lambda, k = %f, %f" % (lambda_, k)
