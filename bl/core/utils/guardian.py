# BEGIN_COPYRIGHT
# END_COPYRIGHT
"""
This script is used to ensure that subprocesses (call them slave
processes) launched with the subprocess module (specifically, in our
case, with the process_spawner), are killed if the parent (or master)
process (i.e., process_spawner, in our case) dies for any reason.
"""

from optparse import OptionParser
import sys, os, signal, time

POLL_INTERVAL = 5


def get_cmdline(pid):
  try:
    f = open("/proc/%d/cmdline" % pid)
    cmdline = f.read()
    f.close()
  except IOError:
    cmdline = None
  return cmdline

def setup_option_parser():
  global parser
  parser = OptionParser('usage: python %prog [OPTIONS] MASTER_PID SLAVE_PID')
  parser.add_option('-p', '--poll-interval', type='int', dest='poll_interval',
                    help='polling interval for the guardian in seconds',
                    metavar='INT')
  parser.add_option('-d', '--debug_file', type='string', dest='debug_file',
                    help='debug file path', metavar='STRING')

def main(master, slave, poll, dbg_file=None):
  master_id = int(master)
  slave_id = int(slave)
  guardian_id = int(os.getpid())
  sys.stderr.write("guardian (%d): master pid: %d; slave pid: %d\n" %
                   (guardian_id, master_id, slave_id))
  original_master_cmdline = get_cmdline(master_id)
  original_slave_cmdline = get_cmdline(slave_id)
  guardian_cmdline = get_cmdline(guardian_id)

  if dbg_file:
    f = open(dbg_file, 'w')
    f.write('MASTER: %d %r\n' %
            (master_id, original_master_cmdline.replace("\x00", " ")))
    f.write('SLAVE: %d %r\n' %
            (slave_id, original_slave_cmdline.replace("\x00", " ")))
    f.write('GUARDIAN: %d %r\n' %
            (guardian_id, guardian_cmdline.replace("\x00", " ")))
    f.close()
  
  while True:
    master_cmdline = get_cmdline(master_id)
    slave_cmdline = get_cmdline(slave_id)
    if slave_cmdline != original_slave_cmdline:
      # None: slave is dead; != : slave pid has been recycled
      sys.stderr.write("guardian (%d): slave (pid %d) is dead, exiting\n"
                       % (guardian_id, slave_id))
      break
    elif master_cmdline != original_master_cmdline:
      # None: master is dead; != : master pid has been recycled
      sys.stderr.write("guardian (%d): killing slave (pid %d)\n" %
                       (guardian_id, slave_id))
      try:
        os.kill(slave_id, signal.SIGKILL)
      except OSError, e:
        if e.errno != 3:  # 3=no such process: died after we checked cmdline
          raise
      break
    else:
      time.sleep(poll)


if __name__ == "__main__":
  setup_option_parser()
  options, args = parser.parse_args()

  try:
    master = int(args[0])
    slave  = int(args[1])
  except IndexError:
    parser.print_help()
    sys.exit(2)
  
  if options.poll_interval:
    poll_int = options.poll_interval
  else:
    poll_int = POLL_INTERVAL

  if options.debug_file:
    dbg_file_path = options.debug_file
  else:
    dbg_file_path = None

  main(master, slave, poll_int, dbg_file=dbg_file_path)
