# BEGIN_COPYRIGHT
# END_COPYRIGHT
import sys, subprocess, time, imp, os, signal
from null_logger import NullLogger


class ChildTerminationError(Exception):
  pass

def handler(signum, frame):
  raise ChildTerminationError


def find_guardian_exe():
  D = os.path.dirname(os.path.abspath(__file__))
  return os.path.join(D, "guardian.py")


class OptMapper(object):

  def __init__(self, name, flag, sep=" "):
    self.name = name
    self.flag = flag
    self.sep = sep

  def map(self, opts):
    value = opts.get(self.name)
    if value is None:
      return []
    if type(value) is not list and type(value) is not tuple:
      value = [value]
    cl_fragment = []
    for v in value:
      mapped_opt = []
      if type(v) is not bool or v:
        mapped_opt.append(self.flag)
      if type(v) is not bool:
        mapped_opt.append(str(v))
      if self.sep == " ":
        cl_fragment.extend(mapped_opt)
      elif mapped_opt:
        cl_fragment.append(self.sep.join(mapped_opt))
    return cl_fragment


class ProcessSpawner(object):
  
  POLL_DELTA = 5  # seconds between two subsequent subprocess polls
  CALLBACK_FREQ = 1  # wait this number of polls before invoking the callback
  OUT_FREQ = 10  # wait this number of polls before updating sys.stdout
  ERR_FREQ = 10  # wait this number of polls before updating sys.stderr

  def __init__(self, exe_file,
               logger=None,
               poll_delta=POLL_DELTA,
               update_callback=None,
               create_guardian=True,
               callback_freq=CALLBACK_FREQ):
    self.logger = logger or NullLogger()
    self.exe_file = exe_file
    self.poll_delta = poll_delta
    self.update_callback = update_callback
    self.create_guardian = create_guardian
    self.callback_freq = callback_freq
    self.proc = None
    self.opt_mappers = []
    self.poll_counter = 0

  def __del__(self):
    if self.proc:
      try:
        if self.proc.returncode is None:
          self.proc.kill()
      except OSError, e:
        self.logger.warn('__del__[%s] raised: %s' % (self, e))

  def add_opt_mapper(self, name, flag, sep=" "):
      self.opt_mappers.append(OptMapper(name, flag, sep=sep))

  def build_cmd_line(self, args, opts):
    cmd_line = [self.exe_file]
    for om in self.opt_mappers:
      cmd_line.extend(om.map(opts))
    cmd_line.extend(args)
    return cmd_line

  def spawn_guardian(self):
    guardian_exe = find_guardian_exe()
    master_pid = os.getpid()
    slave_pid = self.proc.pid
    guardian_cmd_line = ["python", guardian_exe,
                         str(master_pid), str(slave_pid)]
    guardian = subprocess.Popen(guardian_cmd_line, bufsize=1)
    self.logger.debug('Created guardian process with pid: %d' % guardian.pid)

  def run(self, args=[], opts={},
          stdout=None, stderr=None,
          sysout=False, syserr=False,
          out_freq=OUT_FREQ, err_freq=ERR_FREQ):
    """
    sysout/err: also write data sent to stdout/err to sys.stdout/err
    """
    outf, outsize = self.__get_size(stdout) if sysout else (None, None)
    errf, errsize = self.__get_size(stderr) if syserr else (None, None)
    cmd_line = self.build_cmd_line(args, opts)
    self.logger.debug("cmd_line: '%s'" % " ".join(cmd_line))
    self.proc = subprocess.Popen(cmd_line, bufsize=1,
                                 stdout=stdout, stderr=stderr)
    if self.create_guardian:
      self.spawn_guardian()

    msg = "pid=%d" % self.proc.pid + "; return code=%r"
    while True:
      self.proc.poll()
      self.poll_counter += 1
      self.logger.debug(msg % self.proc.returncode)
      if self.proc.returncode is not None:
        if outsize is not None:
          outsize += self.__update_stream(outf, outsize, sys.stdout)
        if errsize is not None:
          errsize += self.__update_stream(errf, errsize, sys.stderr)
        return self.proc.returncode
      else:
        try:
          signal.signal(signal.SIGCHLD, handler)
          time.sleep(self.poll_delta)
        except ChildTerminationError:
          self.logger.debug("caught SIGCHLD")
          continue
        finally:
          signal.signal(signal.SIGCHLD, signal.SIG_DFL)
        if self.update_callback and not self.poll_counter % self.callback_freq:
          self.update_callback(self.proc.pid)
        if outsize is not None and not self.poll_counter % out_freq:
          outsize += self.__update_stream(outf, outsize, sys.stdout)
        if errsize is not None and not self.poll_counter % err_freq:
          errsize += self.__update_stream(errf, errsize, sys.stderr)

  def __get_size(self, f):
    if hasattr(f, "fileno"):
      fd = f.fileno()
    else:
      fd = f
    if fd is not None and fd > 2:
      try:
        size = os.fstat(fd).st_size
        name = os.readlink("/proc/self/fd/%d" % fd)
        f = open(f.name, "rb")
      except OSError, IOError:
        self.logger.warn("couldn't get handle to file, sysout/err disabled" % f)
        f, size = None, None
    return f, size
  
  def __update_stream(self, f, old_size, output_stream):
    size = os.stat(f.name).st_size
    f.seek(old_size)
    chunk = f.read(size-old_size)
    output_stream.write(chunk)
    return len(chunk)
