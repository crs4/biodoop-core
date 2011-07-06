# BEGIN_COPYRIGHT
# END_COPYRIGHT

"""
shell1 $ python try_guardian.py
shell2 $ ps aux | grep 'python\|sleep' | grep -v grep
"""

import sys, os, subprocess


try:
  opt = sys.argv[1]
except IndexError:
  pass
else:
  if sys.argv[1] == "--clean":
    os.system("rm -fv *.log *.out *.err")
    sys.exit(0)


guardian_exe = "../../bl/core/utils/guardian.py"
for i in xrange(5):
  stdout = open("p%d.out" % i, "w")
  stderr = open("p%d.err" % i, "w")
  proc = subprocess.Popen(["sleep", "10"], bufsize=1,
                          stdout=stdout, stderr=stderr)
  master_pid = os.getpid()
  slave_pid = proc.pid
  print "launched process %d" % slave_pid
  guardian_cmd_line = ["python", guardian_exe,
                       "-d", "g%d.log" % i,
                       str(master_pid), str(slave_pid)]
  guardian = subprocess.Popen(guardian_cmd_line, bufsize=1)
  retcode = proc.wait()
  print "process %d exited with status %d" % (slave_pid, retcode)
