# BEGIN_COPYRIGHT
# END_COPYRIGHT
"""
Get Karlin-Altschul parameters lambda and k.
"""

import logging, tempfile, os, shutil, subprocess
import xml.dom.minidom
logging.basicConfig(level=logging.DEBUG)

import bl.seq.engines.blastall_2_2_21 as blastall
from bl.utils.random_ext import sample_wr


class LKCalculator(object):

  def calculate(self):
    raise NotImplementedError


class BlastallLKCalculator(LKCalculator):
  """
  Use blastall to get lambda and k.
  
  Lambda and k depend on:
    1. substitution matrix [-M]
    2. gap opening cost [-G]
    3. gap extension cost [-E]

  Substitution matrix:
    1. amino acid sequences: pre-calculated [-M]
    2. nucleotide sequences: depends on:
      2.1 penalty for nucleotide mismatch [-q]
      2.2 reward for nucleotide match [-r]
  """
  HEADER = "foo"
  SYMBOLS = "ACGT"  # good for both nucleotides and amino acids
  SEQ_LEN = 40
  DB_SIZE = 10

  def __init__(self, formatdb_exe, blastall_exe,
               log_level=None, engine_opts={}):
    super(BlastallLKCalculator, self).__init__()
    self.formatdb_exe = formatdb_exe
    self.opts = {}
    self.opts.update(engine_opts)
    self.wd = tempfile.mkdtemp(prefix="bioland_")
    self.input_file = os.path.join(self.wd, "blastall.in")
    self.output_file = os.path.join(self.wd, "blastall.out")
    engine_logger = logging.getLogger("blastall")
    engine_logger.setLevel(log_level)
    self.engine = blastall.Engine(exe_file=blastall_exe,
                                  logger=engine_logger,
                                  create_guardian=False)
    self.db = self.__build_db()
    self.opts["blastall.database"] = self.db
    self.opts["blastall.out.tabular"] = False
    self.opts["blastall.out.xml"] = True
    self.opts["blastall.input.file"] = self.input_file
    self.opts["blastall.output.file"] = self.output_file

  def __del__(self):
    if hasattr(self, "wd"):
      shutil.rmtree(self.wd)

  def calculate(self):
    # TODO: use stdin/stdout instead
    f = open(self.input_file, "w")
    f.write(">%s\n" % self.HEADER)
    f.write("%s\n" % "".join(sample_wr(self.SYMBOLS, self.SEQ_LEN)))
    f.close()
    self.engine.blastall(opts=self.opts)
    return map(float, self.__get_lk())

  def __build_db(self):
    prog = self.opts["blastall.program"]  # actually a required parameter
    ftype = "T" if prog in ("blastp", "blastx") else "F"
    tag = "db"
    data = []
    for i in xrange(self.DB_SIZE):
      data.append(">%s_%d\n" % (self.HEADER, i))
      data.append("%s\n" % "".join(sample_wr(self.SYMBOLS, self.SEQ_LEN)))
    db_fn = os.path.join(self.wd, tag)
    f = open(db_fn, "w")
    f.writelines(data)
    f.close()
    cl = [self.formatdb_exe, "-p", ftype, "-o", "T", "-i", tag]
    subprocess.check_call(cl, cwd=self.wd)
    return db_fn

  def __get_lk(self):
    dom = xml.dom.minidom.parse(self.output_file)
    return [dom.getElementsByTagName("Statistics_%s" % p)[0].firstChild.data
            for p in "lambda", "kappa"]
