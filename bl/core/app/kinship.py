# BEGIN_COPYRIGHT
# END_COPYRIGHT

"""
Compute the kinship matrix of a set of genotypes.

This is a MapReduce implementation of the ``ibs`` function from
`GenABEL <http://www.genabel.org>`_.
"""

import sys, os, logging, argparse

import pydoop.hdfs as hdfs
import pydoop.hadut as hadut

from bl.core.utils import random_str


def configure_env(args):
  must_reset = False
  for n in "HADOOP_HOME", "HADOOP_CONF_DIR":
    v = getattr(args, n.lower())
    if v:
      os.environ[n] = v
      must_reset = True
  if must_reset:
    hdfs.reset()


LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LOG_FORMAT = '%(asctime)s|%(levelname)-8s|%(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
MR_CONF = {
  "hadoop.pipes.java.recordreader": "true",
  "hadoop.pipes.java.recordwriter": "false",
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


def run_mr_app(args, logger):
  MR_CONF["bl.mr.loglevel"] = args.log_level
  if args.hdfs_user:
    MR_CONF["bl.hdfs.user"] = args.hdfs_user
  if args.mapred_child_opts:
    MR_CONF["mapred.child.java.opts"] = args.mapred_child_opts
  launcher_text = generate_launcher("bl.core.gt.mr.kinship")
  logger.debug("local LIBHDFS_OPTS: %r" % (os.getenv("LIBHDFS_OPTS"),))
  logger.debug("running MapReduce application")
  launcher_name = random_str()
  logger.debug("launcher_name: %r" % (launcher_name,))
  hdfs.dump(launcher_text, launcher_name)
  mr_conf = MR_CONF.copy()
  mr_conf["mapred.map.tasks"] = args.mappers
  mr_conf["mapred.compress.map.output"] = "true"
  mr_conf["mapred.reduce.tasks"] = "1"
  mr_conf["mapred.job.name"] = "kinship"
  hadut.run_pipes(launcher_name, args.input, args.output, properties=mr_conf)


def make_parser():
  parser = argparse.ArgumentParser(
    description="Compute the kinship matrix of a set of genotypes",
    )
  parser.add_argument('input', metavar="INPUT", help='input hdfs path')
  parser.add_argument('output', metavar="OUTPUT", help='output hdfs path')
  parser.add_argument('-m', '--mappers', type=int, metavar="INT",
                      help='number of mappers', default=2)
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


def main(argv):
  parser = make_parser()
  args = parser.parse_args(argv[1:])
  logger = configure_logging(args.log_level, args.log_file)
  logger.debug("command line args: %r" % (args,))
  configure_env(args)
  if args.mr_libhdfs_opts:
    old_libhdfs_opts = os.getenv("LIBHDFS_OPTS")
    os.environ["LIBHDFS_OPTS"] = args.mr_libhdfs_opts
  if args.mr_libhdfs_opts:
    os.environ["LIBHDFS_OPTS"] = old_libhdfs_opts
  run_mr_app(args, logger)
  logger.info("all done")


if __name__ == "__main__":
  main(sys.argv)
