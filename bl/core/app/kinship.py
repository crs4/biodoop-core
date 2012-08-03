# BEGIN_COPYRIGHT
# END_COPYRIGHT

"""
Compute the kinship matrix of a set of genotypes.

This is a MapReduce implementation of the ``ibs`` function from
`GenABEL <http://www.genabel.org>`_.
"""

import sys, os, logging, argparse, zlib

import pydoop.hdfs as hdfs
import pydoop.hadut as hadut

from bl.core.utils import random_str
from bl.core.gt.kinship import KinshipVectors, KinshipBuilder


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
  "hadoop.pipes.java.recordwriter": "true",
  "mapred.output.key.class": "org.apache.hadoop.io.NullWritable",
  "mapred.output.compress": "true",
  "mapred.reduce.tasks": "0",
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


def update_mr_conf(args):
  MR_CONF["bl.mr.loglevel"] = args.log_level
  MR_CONF["bl.hdfs.user"] = args.hdfs_user
  if args.mapred_child_opts:
    MR_CONF["mapred.child.java.opts"] = args.mapred_child_opts


def run_phase_one(args, logger):
  launcher_text = generate_launcher("bl.core.gt.mr.kinship.phase_one")
  launcher_name, mr_out_dir = random_str(), random_str()
  logger.debug("launcher_name: %r" % (launcher_name,))
  logger.debug("mr_out_dir: %r" % (mr_out_dir,))
  hdfs.dump(launcher_text, launcher_name)
  mr_conf = MR_CONF.copy()
  mr_conf["mapred.map.tasks"] = args.mappers[0]
  mr_conf["mapred.job.name"] = "kinship_phase_one"
  hadut.run_pipes(launcher_name, args.input, mr_out_dir, properties=mr_conf)
  return mr_out_dir


def run_phase_two(mappers, input_, logger):
  launcher_text = generate_launcher("bl.core.gt.mr.kinship.phase_two")
  launcher_name, mr_out_dir = random_str(), random_str()
  logger.debug("launcher_name: %r" % (launcher_name,))
  logger.debug("mr_out_dir: %r" % (mr_out_dir,))
  hdfs.dump(launcher_text, launcher_name)
  mr_conf = MR_CONF.copy()
  mr_conf["mapred.map.tasks"] = mappers
  mr_conf["mapred.job.name"] = "kinship_phase_two"
  hadut.run_pipes(launcher_name, input_, mr_out_dir, properties=mr_conf)
  return mr_out_dir


def run_mr_app(args, logger):
  logger.debug("local LIBHDFS_OPTS: %r" % (os.getenv("LIBHDFS_OPTS"),))
  logger.info("running MapReduce application")
  mr_out_dir = run_phase_one(args, logger)
  for nm in args.mappers[1:]:
    input_ = random_str()
    logger.info("running consolidation step, input=%r" % (input_,))
    with hdfs.open(input_, "w", user=args.hdfs_user) as fo:
      ls = [_ for _ in hdfs.ls(mr_out_dir, user=args.hdfs_user)
            if hdfs.path.basename(_).startswith("part")]
      logger.debug("found %d data files in %r" % (len(ls), mr_out_dir))
      for fn in ls:
        fo.write("%s\n" % hdfs.path.abspath(fn, user=args.hdfs_user))
    mr_out_dir = run_phase_two(nm, input_, logger)
  return mr_out_dir


def collect_output(mr_out_dir, logger):
  builder = None
  for fn in hdfs.ls(mr_out_dir):
    if not hdfs.path.basename(fn).startswith("part"):
      continue
    logger.info("processing %r" % (fn,))
    with hdfs.open(fn) as f:
      s = zlib.decompress(f.read())
    vectors = KinshipVectors.deserialize(s)  # ignores trailing newline char
    if builder is None:
      builder = KinshipBuilder(vectors)
    else:
      builder.vectors += vectors
  logger.info("building kinship matrix")
  return builder.build()


def write_output(k, args, logger):
  logger.debug("kinship matrix: shape=%r" % (k.shape,))
  logger.info("serializing output")
  s = KinshipBuilder.serialize(k)
  logger.debug("serialized matrix: %d bytes" % len(s))
  logger.info("writing output to %r" % (args.output,))
  hdfs.dump(s, args.output, user=args.hdfs_user)


def list_of_int(s):
  return map(int, s.split(","))


def make_parser():
  parser = argparse.ArgumentParser(
    description="Compute the kinship matrix of a set of genotypes",
    )
  parser.add_argument('input', metavar="INPUT", help='input hdfs path')
  parser.add_argument('output', metavar="OUTPUT", help='output hdfs file path')
  parser.add_argument('-m', '--mappers', type=list_of_int, default=[2],
                      metavar="INT[,INT...]", help='number of mappers')
  parser.add_argument('--log-level', metavar="STRING", choices=LOG_LEVELS,
                      help='logging level', default='INFO')
  parser.add_argument('--log-file', metavar="FILE", help='log file')
  parser.add_argument("--hadoop-home", metavar="STRING",
                      help="Hadoop home directory")
  parser.add_argument("--hadoop-conf-dir", metavar="STRING",
                      help="Hadoop configuration directory")
  parser.add_argument("--hdfs-user", metavar="STRING", default="",
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
  # it makes no sense to use less mappers in subsequent phases
  args.mappers.sort(reverse=True)
  configure_env(args)
  if args.mr_libhdfs_opts:
    old_libhdfs_opts = os.getenv("LIBHDFS_OPTS")
    os.environ["LIBHDFS_OPTS"] = args.mr_libhdfs_opts
  if args.mr_libhdfs_opts:
    os.environ["LIBHDFS_OPTS"] = old_libhdfs_opts
  update_mr_conf(args)
  mr_out_dir = run_mr_app(args, logger)
  k = collect_output(mr_out_dir, logger)
  write_output(k, args, logger)
  logger.info("all done")


if __name__ == "__main__":
  main(sys.argv)
