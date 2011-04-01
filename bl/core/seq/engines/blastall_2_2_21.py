# BEGIN_COPYRIGHT
# END_COPYRIGHT
import os, tarfile, warnings
from bl.core.utils.pspawner import ProcessSpawner


class Engine(object):

  EXE="/usr/bin/blastall"
  NAME="blastall"
  TMP_DIR = os.environ.get("TMPDIR", "/var/tmp")
  FLAG_MAP = {
    "program": "-p",
    "database": "-d",
    "input.file": "-i",
    "output.file": "-o",
    "out.xml": "-m 7",
    "out.tabular": "-m 8",
    "evalue": "-e",
    "gap.cost": "-G",
    "word.size": "-W",
    "filter": "-F",  # 'T' for True, 'F' for False
    }

  def __init__(self, exe_file=EXE, **kwargs):
    self.wrapper = ProcessSpawner(exe_file, **kwargs)
    for opt, flag in self.FLAG_MAP.iteritems():
      self.wrapper.add_opt_mapper("%s.%s" % (self.NAME, opt), flag)

  def blastall(self, args=[], opts={}):
    if "filter" in opts:
      opts["filter"] = "T" if opts["filter"] else "F"
    self.wrapper.run(args, opts)
