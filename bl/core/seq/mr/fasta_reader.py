# BEGIN_COPYRIGHT
# END_COPYRIGHT
import os, logging, zlib
logging.basicConfig(level=logging.DEBUG)

from pydoop.pipes import RecordReader, InputSplit
from pydoop.hdfs import hdfs

from pydoop.utils import split_hdfs_path, raise_pydoop_exception, \
     jc_configure, jc_configure_bool, jc_configure_int

from bl.core.seq.io.fasta import RawFastaReader


class record_reader(RecordReader):
  """
  Reads sequences from FASTA text files.

  U{http://en.wikipedia.org/wiki/FASTA}

  @output-record: C{key} is the FASTA header, C{value} is the sequence.

  @jobconf-param: C{bl.libhdfs.opts} Options for the jvm embedded into
  libhdfs. This is especially useful to control hdfs memory usage
  (setting, for instance, -Xmx48m).

  @jobconf-param: C{bl.mr.fasta-reader.log.level} Debug level, output
  will be collected on stderr. Default value 'WARNING'

  @jobconf-param: C{bl.mr.fasta-reader.compress.header} Compress
  header with zlib. A quick test (take a look at
  bin/compress_stats.py) shows that headers are generally too small to
  get a compression rate greater than one: for this reason, this
  defaults to False.

  @jobconf-param: C{bl.mr.fasta-reader.compress.seq} Compress sequence
  with zlib.

  @jobconf-param: C{bl.mr.fasta-reader.compression.level} zlib
  compression level. zlib's default of 6 looks good.

  @counter-class: C{FASTA_READER}
  @counter-name:  C{FASTA_READER.SEQS_READ} The total number of items read.

  """
  COUNTER_CLASS = "FASTA_READER"
  COUNTER_SEQS = "SEQS_READ"
  DEFAULT_LOG_LEVEL = 'WARNING'

  def __get_configuration(self, jc):
    jc_configure(self, jc, 'bl.mr.fasta-reader.log.level', 'log_level',
                 self.DEFAULT_LOG_LEVEL)
    try:
      self.log_level = getattr(logging, self.log_level)
    except AttributeError:
      raise_pydoop_exception("Unsupported log level: %r" % self.log_level)    
    jc_configure(self, jc, "bl.libhdfs.opts", "libhdfs_opts", "")
    if self.libhdfs_opts:
      os.environ["LIBHDFS_OPTS"] = self.libhdfs_opts
    jc_configure_bool(self, jc, 'bl.mr.fasta-reader.compress.header',
                      'compress_header', False)
    jc_configure_bool(self, jc, 'bl.mr.fasta-reader.compress.seq',
                      'compress_seq', True)
    jc_configure_int(self, jc, 'bl.mr.fasta-reader.compression.level',
                      'compression_level', 6)

  def __init__(self, ctx):
    super(record_reader, self).__init__(ctx)
    self.fs = self.file = None  # ensure these always exist, for __del__
    self.__get_configuration(ctx.getJobConf())
    self.logger = logging.getLogger("fasta_reader")
    self.logger.setLevel(self.log_level)
    self.ctx = ctx
    self.isplit = InputSplit(self.ctx.getInputSplit())
    self.logger.debug(
      "InputSplit: filename = %s, offset = %d, length = %d" %
      (self.isplit.filename, self.isplit.offset, self.isplit.length)
      )
    host, port, fpath = split_hdfs_path(self.isplit.filename)
    self.fs = hdfs(host, port)
    self.file = self.fs.open_file(fpath, os.O_RDONLY)
    self.input_seqs_counter = self.ctx.getCounter(
      record_reader.COUNTER_CLASS,
      record_reader.COUNTER_SEQS
      )
    self.reader = RawFastaReader(self.file, self.isplit.offset,
                                 self.isplit.length)

  def __del__(self):
    if self.file:
      self.file.close()
    if self.fs:
      self.fs.close()

  def next(self):
    """
    @return tuple(bool have_a_record, str record_key, str record_value)
    """
    try:
      header, seq = self.reader.next()
    except StopIteration:
      return (False, "", "")
    self.ctx.incrementCounter(self.input_seqs_counter, 1)
    if self.compress_header:
      header = zlib.compress(header, self.compression_level)
    if self.compress_seq:
      seq = zlib.compress(seq, self.compression_level)
    return (True, header, seq)

  def getProgress(self):
    return min(float(self.reader.bytes_read)/self.isplit.length, 1.0)
