# BEGIN_COPYRIGHT
# END_COPYRIGHT

"""
Compute the kinship matrix of a set of genotypes.

This is a MapReduce implementation of the ``ibs`` function from
`GenABEL <http://www.genabel.org>`_.
"""

import sys, os, logging, argparse, uuid
from itertools import izip

import pydoop.hdfs as hdfs
import pydoop.hadut as hadut

from bl.core.messages.KinshipVectors import msg_to_KinshipVectors
from bl.core.messages.Array import Array_to_msg
from bl.core.gt.kinship import KinshipBuilder


LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LOG_FORMAT = '%(asctime)s|%(levelname)-8s|%(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
MR_CONF = {
  "hadoop.pipes.java.recordreader": "true",
  "hadoop.pipes.java.recordwriter": "true",
  "mapred.reduce.tasks": "0",
  }


def configure_env(**kwargs):
  reload_pydoop_modules = False
  for name, value in kwargs.iteritems():
    if value:
      os.environ[name] = value
      reload_pydoop_modules = True
  if reload_pydoop_modules:
    for m in hdfs, hadut:
      reload(m)


def configure_logging(log_level, log_file=None):
  logger = logging.getLogger()
  for h in logger.handlers:
    logger.removeHandler(h)
  log_config = {
    'format': LOG_FORMAT,
    'datefmt': LOG_DATEFMT,
    'level': getattr(logging, log_level)
    }
  if log_file:
    log_config['filename'] = log_file
  logging.basicConfig(**log_config)
  return logger


def generate_launcher(app_module, export_env=True):
  lines = [
    '#!/bin/bash',
    '""":"',
    ]
  if export_env:
    for item in os.environ.iteritems():
      lines.append('export %s="%s"' % item)
  lines.extend([
    'exec python -u $0 $@',
    '":"""',
    'from %s import run_task' % app_module,
    'run_task()',
    ])
  return "\n".join(lines)


def run_mr_app(in_path, out_path, logger):
  launcher_name = uuid.uuid4().hex
  logger.debug("launcher_name: %r" % (launcher_name,))
  launcher_text = generate_launcher("bl.core.gt.mr.kinship")
  hdfs.dump(launcher_text, launcher_name)
  if in_path.startswith("file:"):
    hdfs_in_path = uuid.uuid4().hex
    logger.debug("hdfs_in_path: %r" % (hdfs_in_path,))
    logger.info("copying input to hdfs")
    hdfs.cp(in_path, hdfs_in_path)
    in_path = hdfs_in_path
  mr_out_path = uuid.uuid4().hex
  logger.debug("mr_out_path: %r" % (mr_out_path,))
  logger.info("running MapReduce application")
  hadut.run_pipes(launcher_name, in_path, mr_out_path, properties=MR_CONF)
  logger.info("collecting output")
  collect_output(mr_out_path, out_path)


def collect_output(mr_out_path, out_path):
  builder = None
  for fn in hdfs.ls(mr_out_path):
    if not fn.startswith("part-"):
      continue
    with hdfs.open(fn) as f:
      sep = f.read(1)
      assert sep == "\t"
      msg = f.read()
    obs_hom, exp_hom, present, lower_v, upper_v = msg_to_KinshipVectors(msg)
    if builder is None:
      builder = KinshipBuilder(obs_hom.size)
    builder.obs_hom += obs_hom
    builder.exp_hom += exp_hom
    builder.present += present
    for old_v, v in izip(builder.lower_v, lower_v):
      old_v += v
    for old_v, v in izip(builder.upper_v, upper_v):
      old_v += v
  k = builder.build()
  with hdfs.open(out_path, "w") as fo:
    fo.write(Array_to_msg(k))
  

def make_parser():
  parser = argparse.ArgumentParser(
    description="Compute the kinship matrix of a set of genotypes",
    epilog="NOTE: for input/output on local fs, use the file:/foo/bar format",
    )
  parser.add_argument('input', metavar="INPUT", help='input hdfs path')
  parser.add_argument('output', metavar="OUTPUT", help='output hdfs path')
  parser.add_argument('--log-level', metavar="STRING", choices=LOG_LEVELS,
                      help='logging level', default='INFO')
  parser.add_argument('--log-file', metavar="FILE", help='log file')
  parser.add_argument("--hadoop-home", metavar="STRING",
                      help="Hadoop home directory")
  parser.add_argument("--hadoop-conf-dir", metavar="STRING",
                      help="Hadoop configuration directory")

  return parser


def main(argv):
  parser = make_parser()
  args = parser.parse_args(argv[1:])
  logger = configure_logging(args.log_level, args.log_file)  
  logger.debug("command line args: %r" % (args,))
  configure_env(
    hadoop_home=args.hadoop_home, hadoop_conf_dir=args.hadoop_conf_dir
    )
  run_mr_app(args.input, args.output, logger)
  logger.info("all done")


if __name__ == "__main__":
  main(sys.argv)
