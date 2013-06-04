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


guardian_exe = os.path.join(os.path.dirname(__file__),
                            "../../bl/core/utils/guardian.py")
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
