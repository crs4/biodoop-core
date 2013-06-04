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
import unittest, cStringIO, math, itertools, tempfile, os, textwrap
import bl.core.seq.io.fasta as faio


# All record titles must be the same size for the seq_size trick to work
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


def dump_tuples(seq_tuples):
  fd, fn = tempfile.mkstemp()
  for hdr, s in seq_tuples:
    line_len = len(s) / 3
    os.write(fd, ">%s\n%s\n" % (hdr, textwrap.fill(s, line_len)))
  os.close(fd)
  return fn


class MinimalStream(object):

  def __init__(self, seq_tuples):
    self.f = sum([[">%s\n" % t[0], "%s\n" % t[1]] for t in seq_tuples], [])


class StreamWithReadline(MinimalStream):

  def readline(self):
    try:
      return self.f.pop(0)
    except IndexError:
      return ""

class StreamWithNext(MinimalStream):

  def __init__(self, seq_tuples):
    super(StreamWithNext, self).__init__(seq_tuples)
    self.f = iter(self.f)

  def next(self):
    return self.f.next()


class TestFindFirstRecord(unittest.TestCase):

  def setUp(self):
    self.f, l = build_file(SEQ_TUPLES)
    n = len(SEQ_TUPLES)
    self.cases = [  # (offset, split_size, expected_pos)
      (0, 1, 0), (0, l+1, 0),
      (1, 1, -1), (1, l-1, -1), (1, l, l),
      (l-1, 1, -1), (l-1, 2, l),
      (l, 1, l), (l, l+1, l),
      (l+1, 1, -1), (l+1, l+1, 2*l),
      ((n-1)*l, 1, (n-1)*l), ((n-1)*l, l, (n-1)*l),
      ((n-1)*l+1, 1, -1), ((n-1)*l+1, l-1, -1)
      ]
    self.l = l
    self.n = n

  def runTest(self):
    for bufsize in 1, 15, self.n*self.l:
      faio.BUFSIZE = bufsize
      for offset, split_size, exp_p in self.cases:
        p = faio.find_first_record(self.f, offset, split_size)
        self.assertEqual(p, exp_p, "case (%d, %d, %d): %d != %d" %
                         (offset, split_size, exp_p, p, exp_p))
        self.f.seek(0)


class CommonReaderTests(unittest.TestCase):

  READER_CLASS = None

  def _check_f(self, f, seq_tuples):
    reader = self.READER_CLASS(f)
    for (hdr, s), (exp_hdr, exp_s) in itertools.izip(reader, seq_tuples):
      self.assertEqual(hdr, exp_hdr)
      self.assertEqual(s, exp_s)

  def test_regular_file(self):
    fn = dump_tuples(SEQ_TUPLES)
    with open(fn) as f:
      self._check_f(f, SEQ_TUPLES)
    os.unlink(fn)



class TestRawFastaReader(CommonReaderTests):

  READER_CLASS = faio.RawFastaReader

  def setUp(self):
    self.f, self.l = build_file(SEQ_TUPLES)
    self.n = len(SEQ_TUPLES)
    #self.offset = 0  # offset != 0 is covered by TestFindFirstRecord
    
  def __run_test(self, offset, split_size, exp_tuples):
    for bufsize in 1, 15, self.n*self.l:
      faio.BUFSIZE = bufsize
      reader = self.READER_CLASS(self.f, offset, split_size)
      tuples = []
      for i, t in enumerate(reader):
        tuples.append(t)
        self.assertEqual(reader.bytes_read, (i+1)*self.l)
      self.assertEqual(len(tuples), len(exp_tuples))
      for seq, exp_seq in itertools.izip(tuples, exp_tuples):
        self.assertEqual(seq, exp_seq)
      self.f.seek(0)

  def test_all(self):
    self.__run_test(0, self.l*self.n, SEQ_TUPLES)

  def test_partial(self):
    for i in xrange(self.n):
      self.__run_test(0, int((i+0.5)*self.l), SEQ_TUPLES[:i+1])
    self.__run_test(0, 1, SEQ_TUPLES[:1])

  def test_bad(self):
    f = cStringIO.StringIO()
    content = ">abc>def"
    f.write(content)
    f.seek(0)    
    reader = self.READER_CLASS(f, 0, len(content))
    self.assertRaises(faio.FastaError, reader.next)


class TestSimpleFastaReader(CommonReaderTests):

  READER_CLASS = faio.SimpleFastaReader

  def test_minimal_next(self):
    f = StreamWithNext(SEQ_TUPLES)
    self._check_f(f, SEQ_TUPLES)

  def test_minimal_readline(self):
    f = StreamWithReadline(SEQ_TUPLES)
    self._check_f(f, SEQ_TUPLES)


def load_tests(loader, tests, pattern):
  test_cases = (TestFindFirstRecord, TestRawFastaReader, TestSimpleFastaReader)
  suite = unittest.TestSuite()
  for tc in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(tc))
  return suite


if __name__ == '__main__':
  suite = load_tests(unittest.defaultTestLoader, None, None)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
