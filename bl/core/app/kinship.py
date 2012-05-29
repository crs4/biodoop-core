# BEGIN_COPYRIGHT
# END_COPYRIGHT

"""
Compute the kinship matrix of a set of genotypes.

This is a MapReduce implementation of the ``ibs`` function from
`GenABEL <http://www.genabel.org>`_.
"""

import sys, os, logging, argparse
from itertools import izip

import pydoop.hdfs as hdfs
import pydoop.hadut as hadut

from bl.core.utils import random_str
from bl.core.messages.KinshipVectors import msg_to_KinshipVectors
from bl.core.messages.Array import Array_to_msg
from bl.core.gt.kinship import KinshipBuilder


def configure_env(args):
  must_reload = False
  for n in "HADOOP_HOME", "HADOOP_CONF_DIR":
    v = getattr(args, n.lower())
    if v:
      os.environ[n] = v
      must_reload = True
  if must_reload:
    reload(hdfs)


LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LOG_FORMAT = '%(asctime)s|%(levelname)-8s|%(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
MR_CONF = {
  "hadoop.pipes.java.recordreader": "true",
  "hadoop.pipes.java.recordwriter": "false",
  "mapred.reduce.tasks.speculative.execution": "false",
  "mapred.job.name": "kinship",
  }


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


def run_mr_app(in_path, out_path, launcher_text, logger):
  launcher_name = random_str()
  logger.debug("launcher_name: %r" % (launcher_name,))
  logger.debug("local LIBHDFS_OPTS: %r" % (os.getenv("LIBHDFS_OPTS"),))
  hdfs.dump(launcher_text, launcher_name)
  if in_path.startswith("file:"):
    hdfs_in_path = random_str()
    logger.debug("hdfs_in_path: %r" % (hdfs_in_path,))
    logger.info("copying input to hdfs")
    hdfs.cp(in_path, hdfs_in_path)
    in_path = hdfs_in_path
  mr_out_path = random_str()
  logger.debug("mr_out_path: %r" % (mr_out_path,))
  logger.info("running MapReduce application")
  hadut.run_pipes(launcher_name, in_path, mr_out_path, properties=MR_CONF)
  logger.info("collecting output")
  collect_output(mr_out_path, out_path)


def collect_output(mr_out_path, out_path):
  builder = None
  for fn in hdfs.ls(mr_out_path):
    if not hdfs.path.basename(fn).startswith("kinship-"):
      continue
    msg = hdfs.load(fn)
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
  parser.add_argument('-m', '--mappers', type=int, metavar="INT",
                      help='number of mappers', default=1)
  parser.add_argument('-r', '--reducers', type=int, metavar="INT",
                      help='number of reducers', default=1)
  parser.add_argument('--log-level', metavar="STRING", choices=LOG_LEVELS,
                      help='logging level', default='INFO')
  parser.add_argument('--log-file', metavar="FILE", help='log file')
  parser.add_argument("--hadoop-home", metavar="STRING",
                      help="Hadoop home directory")
  parser.add_argument("--hadoop-conf-dir", metavar="STRING",
                      help="Hadoop configuration directory")
  parser.add_argument("--hdfs-user", metavar="STRING",
                      help="user name for connecting to HDFS")
  parser.add_argument("--mr-libhdfs-opts", metavar="STRING",
                      help="JVM options for the libhdfs used by mr tasks")
  parser.add_argument("--mapred-child-opts", metavar="STRING",
                      help="JVM options for MapReduce child tasks")
  return parser


def update_mr_conf(args):
  MR_CONF["bl.mr.loglevel"] = args.log_level
  if args.hdfs_user:
    MR_CONF["bl.hdfs.user"] = args.hdfs_user
  if args.mapred_child_opts:
    MR_CONF["mapred.child.java.opts"] = args.mapred_child_opts
  MR_CONF["mapred.map.tasks"] = str(args.mappers)
  MR_CONF["mapred.reduce.tasks"] = str(args.reducers)


def main(argv):
  parser = make_parser()
  args = parser.parse_args(argv[1:])
  logger = configure_logging(args.log_level, args.log_file)
  logger.debug("command line args: %r" % (args,))
  configure_env(args)
  update_mr_conf(args)
  if args.mr_libhdfs_opts:
    old_libhdfs_opts = os.getenv("LIBHDFS_OPTS")
    os.environ["LIBHDFS_OPTS"] = args.mr_libhdfs_opts
  launcher_text = generate_launcher("bl.core.gt.mr.kinship")
  if args.mr_libhdfs_opts:
    os.environ["LIBHDFS_OPTS"] = old_libhdfs_opts
  run_mr_app(args.input, args.output, launcher_text, logger)
  logger.info("all done")


if __name__ == "__main__":
  main(sys.argv)
