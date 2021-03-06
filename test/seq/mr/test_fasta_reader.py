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
import unittest, os, itertools, logging, cStringIO, math, zlib

from pydoop.utils import split_hdfs_path, make_input_split
from pydoop.hdfs import hdfs
try:
  import pydoop._pipes as pp  # Pydoop pre-0.5.0
except ImportError:
  import pydoop
  pp = pydoop.import_version_specific_module('_pipes')

from bl.core.utils.test_utils import map_context
from bl.core.seq.mr.fasta_reader import record_reader


# FIXME: duplicate from test/seq/io/test_fasta.py -----------------------------
SEQ_TUPLES = [
  ("foo 0", "GGAGAATAGTAATTCAGTGAGCTTTTTTATCTTTGACCAGATGACCTTCTGG"),
  ("foo 1", "TCGATGTGCTTACAGAGAAGGTTATGCGTGGTGGTTCGTGAGGACAAAGCCT"),
  ("foo 2", "TTTCACATACACGCCGTGTTTGGGCGACTACGCACTAGGGTTTGAACCCACC"), 
  ("foo 3", "AGGAAAAATAGCAAAAGCAGGAGTTAATGGGCCTCCACGTTACTTGTCGAGA"), 
  ]

LINE_LEN = 10

def build_file(seq_tuples):
  f = cStringIO.StringIO()
  for hdr, s in seq_tuples:
    f.write(">%s\n" % hdr)
    seq_len = len(s)
    for i in xrange(0, seq_len, LINE_LEN):
      f.write("%s\n" % s[i:i+LINE_LEN])
  f.seek(0)
  record_len = len(hdr) + 2 + seq_len + int(math.ceil(float(seq_len)/LINE_LEN))
  return f, record_len
# FIXME: end duplicate from test/seq/io/test_fasta.py -------------------------


class TestFastaReader(unittest.TestCase):

  def setUp(self):
    self.libhdfs_opts = "-Xmx48m"
    self.log_level = 'WARNING'
    self.compress_header = "false"
    self.compress_seq = "true"
    self.compression_level = "6"
    
    os.environ["LIBHDFS_OPTS"] = self.libhdfs_opts

    self.f, self.l = build_file(SEQ_TUPLES)
    self.n = len(SEQ_TUPLES)
    
    self.data_file_name = 'file:/var/tmp/junk.fasta'
    self.bytes_written = 0
    self.opt_names = ['bl.libhdfs.opts',
                      'bl.mr.fasta-reader.log.level',
                      'bl.mr.fasta-reader.compress.header',
                      'bl.mr.fasta-reader.compress.seq',
                      'bl.mr.fasta-reader.compression.level']
    self.seq_counter_name = "%s:%s" % (record_reader.COUNTER_CLASS,
                                       record_reader.COUNTER_SEQS)
    d = dict(zip(self.opt_names, (self.libhdfs_opts, self.log_level,
                                  self.compress_header, self.compress_seq,
                                  self.compression_level)))
    self.jc = pp.get_JobConf_object(d)
    
    self.split_offset = 0
    self.split_size = self.n * self.l
    self.input_split = make_input_split(self.data_file_name, 0, self.split_size)
    self.map_ctx = map_context(self.jc, self.input_split)
    self.__create_data_file()

  def tearDown(self):
    self.__remove_data_file()

  def test_settable_parameters(self):
    offset, split_size = 0, 1024  # does not matter for this test
    # default
    _, rr = self.__make_rr({}, offset, split_size)
    self.assertEqual(rr.libhdfs_opts, "")
    self.assertEqual(rr.log_level, getattr(logging, rr.DEFAULT_LOG_LEVEL))
    self.assertEqual(rr.compress_header, False)
    self.assertEqual(rr.compress_seq, True)
    self.assertEqual(rr.compression_level, 6)
    # assigned
    libhdfs_opts = self.libhdfs_opts
    log_level = "CRITICAL"
    compress_header = "true"
    compress_seq = "false"
    compression_level = "1"
    d = dict(zip(self.opt_names, (libhdfs_opts, log_level,
                                  compress_header, compress_seq,
                                  compression_level)))
    _, rr = self.__make_rr(d, offset, split_size)
    self.assertEqual(rr.log_level, getattr(logging, log_level))
    self.assertEqual(rr.libhdfs_opts, libhdfs_opts)
    self.assertEqual(rr.compress_header, compress_header == "true")
    self.assertEqual(rr.compress_seq, compress_seq == "true")
    self.assertEqual(rr.compression_level, int(compression_level))
    # bad
    self.assertRaises(
      UserWarning, self.__make_rr,
      {'bl.mr.fasta-reader.log.level': "FOO"}, offset, split_size
      )

  def test_read_all(self):
    print
    self.split_size = self.n * self.l
    self.split_offset = 0
    self.__do_reads_on_split(self.n)

  def test_read_corner_cases(self):
    print
    corner_cases = [
      (0, 1, 1),
      (0, self.l, 1),
      (0, self.l+1, 2),
      (self.l-1, 1, 0),
      (self.l-1, 2, 1),
      (self.n*self.l-1, 1, 0),      
      ]
    for self.split_offset, self.split_size, n in corner_cases:
      self.__do_reads_on_split(n)

  def test_no_record(self):
    split_size = self.l - 1
    offset = self.n*self.l - split_size
    ctx, rr = self.__make_rr({}, offset, split_size)
    have_a_record, _, _ = rr.next()
    self.assertFalse(have_a_record)
    self.assertAlmostEqual(rr.getProgress(), 1.0)
    self.assertEqual(ctx.counters[self.seq_counter_name], 0)
  
  def __do_reads_on_split(self, n_seqs):
    print 'offset=%d, split_size=%d' % (self.split_offset, self.split_size)
    self.input_split = make_input_split(self.data_file_name,
                                        self.split_offset, self.split_size)
    self.map_ctx = map_context(self.jc, self.input_split)
    rr = record_reader(self.map_ctx)
    records = []
    while True:
      have_a_record, header, seq = rr.next()
      if not have_a_record:
        break
      if rr.compress_header:
        header = zlib.decompress(header)
      if rr.compress_seq:
        seq = zlib.decompress(seq)
      records.append((header, seq))      
    self.assertEqual(len(records), n_seqs)
    if n_seqs == len(SEQ_TUPLES):
      # running this check for arbitrary offset/split_size is nontrivial
      # you need a function that founds which seqs should be read
      # we skip it for now
      for (h, s), (exp_h, exp_s) in itertools.izip(records, SEQ_TUPLES):
        self.assertEqual(h, exp_h)
        self.assertEqual(s, exp_s)
    self.assertAlmostEqual(rr.getProgress(), 1.0)
    self.assertEqual(self.map_ctx.counters[self.seq_counter_name], n_seqs)

  def __create_data_file(self):
    host, port, path = split_hdfs_path(self.data_file_name)
    fs = hdfs(host, port)
    f = fs.open_file(path, os.O_WRONLY, 0, 0, 0)
    f.write(self.f.getvalue())
    f.close()
    fs.close()

  def __remove_data_file(self):
    host, port, path = split_hdfs_path(self.data_file_name)
    fs = hdfs(host, port)
    fs.delete(path)
    fs.close()

  def __make_rr(self, jc_dict, offset, split_size):
    jc = pp.get_JobConf_object(jc_dict)
    input_split = make_input_split(self.data_file_name, offset, split_size)
    map_ctx = map_context(jc, input_split)
    return map_ctx, record_reader(map_ctx)


def load_tests(loader, tests, pattern):
  test_cases = (TestFastaReader,)
  suite = unittest.TestSuite()
  for tc in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(tc))
  return suite


if __name__ == '__main__':
  suite = load_tests(unittest.defaultTestLoader, None, None)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
