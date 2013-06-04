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
logging.basicConfig(level=logging.DEBUG)
from bl.core.utils.pspawner import ProcessSpawner


EXE = "./subprocess.sh"
OPT_MAPPER_ARGS = [("some.option", "-o")]
SUBPROC_CODE = """#!/bin/bash

DEFAULT_FREQ=1

echo "DEBUG:subprocess.sh:args = $@" >&2

# discard leading options (very brittle)
for (( i=0; i < $#; i++ )); do
    [ "${1:0:1}" == '-' ] && shift 2
done

minargs=1
if [[ $# -lt $minargs ]]; then
    echo "Usage: $0 DURATION [FREQ]"
    exit 2
fi
DURATION=$1
FREQ=$2
[[ -z "${FREQ}" ]] && FREQ=${DEFAULT_FREQ}    

counter=0
while (( $counter < $DURATION )); do
    counter=$(( $counter + 1 ))
    if ! (( $counter % $FREQ )); then
	echo "subprocess: ${counter}"
    fi
    sleep 1
done
"""


def _try_template(test_name, kwargs, run_kwargs):
  test_name = test_name.upper()
  print " *** %s -- START ***" % test_name
  spawner = ProcessSpawner(EXE, **kwargs)
  for name, flag in OPT_MAPPER_ARGS:
    spawner.add_opt_mapper(name, flag)
  spawner.run(**run_kwargs)
  print " *** %s -- END ***" % test_name
  

class test_container(object):

  LOGGER = logging.getLogger("try_ps")
  LOGGER.setLevel(logging.DEBUG)
  PS_LOGGER = logging.getLogger("pspawner")
  PS_LOGGER.setLevel(logging.DEBUG)
  
  @staticmethod
  def try_minimal(tag):
    kwargs = {}
    run_kwargs = {"args": ["5", "1"]}
    _try_template(tag, kwargs, run_kwargs)

  @staticmethod
  def try_logger(tag):
    kwargs = {"logger": test_container.PS_LOGGER}
    run_kwargs = {"args": ["5", "1"]}
    _try_template(tag, kwargs, run_kwargs)

  @staticmethod
  def try_sudden_death(tag):
    kwargs = {"logger": test_container.PS_LOGGER}
    run_kwargs = {"args": ["0", "1"]}
    _try_template(tag, kwargs, run_kwargs)

  @staticmethod
  def try_options(tag):
    kwargs = {"logger": test_container.PS_LOGGER}
    run_kwargs = {"args": ["5", "1"], "opts": {OPT_MAPPER_ARGS[0][0]: "foo"}}
    _try_template(tag, kwargs, run_kwargs)

  @staticmethod
  def try_callback(tag):
    def callback(pid):
      print "callback: pid = %d" % pid
    kwargs = {"logger": test_container.PS_LOGGER, "poll_delta": 2,
              "callback_freq": 2, "update_callback": callback}
    run_kwargs = {"args": ["10", "1"]}
    _try_template(tag, kwargs, run_kwargs)

  @staticmethod
  def try_redirect(tag):
    out, err = [open(fn, "w+") for fn in ("/tmp/tps.out", "/tmp/tps.err")]
    kwargs = {"logger": test_container.PS_LOGGER}
    run_kwargs = {"args": ["5", "1"], "stdout":out, "stderr":err}
    _try_template(tag, kwargs, run_kwargs)
    for f in out, err:
      test_container.LOGGER.debug("OUT:" if f is out else "ERR:")
      f.seek(0)
      for line in f:
        test_container.LOGGER.debug(line.rstrip())
      f.close()

  @staticmethod
  def try_redirect_dupe(tag):
    out, err = [open(fn, "w+") for fn in ("/tmp/tps.out", "/tmp/tps.err")]
    kwargs = {"logger": test_container.PS_LOGGER}
    run_kwargs = {"args": ["5", "1"], "stdout":out, "stderr":err,
                  "sysout": True, "syserr": True,
                  "out_freq": 2, "err_freq": 2}
    _try_template(tag, kwargs, run_kwargs)
    for f in out, err:
      test_container.LOGGER.debug("OUT:" if f is out else "ERR:")
      f.seek(0)
      for line in f:
        test_container.LOGGER.debug(line.rstrip())
      f.close()

  @staticmethod
  def try_redirect_dupe_progressive(tag):
    out, err = [open(fn, "w+") for fn in ("/tmp/tps.out", "/tmp/tps.err")]
    kwargs = {"logger": test_container.PS_LOGGER, "poll_delta": 1}
    run_kwargs = {"args": ["5", "1"], "stdout":out, "stderr":err,
                  "sysout": True, "syserr": True,
                  "out_freq": 2, "err_freq": 2}
    _try_template(tag, kwargs, run_kwargs)
    for f in out, err:
      test_container.LOGGER.debug("OUT:" if f is out else "ERR:")
      f.seek(0)
      for line in f:
        test_container.LOGGER.debug(line.rstrip())
      f.close()


def print_help(all_tests):
  print "USAGE: python %s [TEST_NAME] [TEST_NAME] ..." % \
        os.path.basename(sys.argv[0])
  print
  print "where TEST_NAME is one of:"
  for t in all_tests:
    print "  %r" % t.func_name[4:]
  print
  print "The default is to run all tests."


def main(argv):
  # don't auto-fetch them from test_container, we want to preserve order
  all_tests = [
    test_container.try_minimal,
    test_container.try_logger,
    test_container.try_sudden_death,
    test_container.try_options,
    test_container.try_callback,
    test_container.try_redirect,
    test_container.try_redirect_dupe,
    test_container.try_redirect_dupe_progressive
    ]
  if len(argv) <= 1:
    tests = all_tests
  elif argv[1] in ("-h", "-help", "--help"):
    print_help(all_tests)
    sys.exit(2)
  else:
    test_names = argv[1:]
    tests = []
    for tn in test_names:
      try:
        tests.append(getattr(test_container, "try_"+tn.lower()))
      except AttributeError:
        sys.exit("%r is not a valid test name. Try running with -h" % tn)
  try:
    with open(EXE, "w") as f:
      f.write(SUBPROC_CODE)
    os.chmod(EXE, 0755)
    for t in tests:
      print
      t(t.func_name)
  finally:
    if os.path.exists(EXE):
      os.remove(EXE)


if __name__ == "__main__":
  main(sys.argv)
