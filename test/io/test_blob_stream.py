# BEGIN_COPYRIGHT
# END_COPYRIGHT

import unittest, tempfile, os, random
import itertools as it

from bl.core.io.blob_stream import BlobStreamWriter, BlobStreamReader


def data_blob():
  char = chr(random.randint(ord('A'), ord('Z')))
  return char * random.randint(10, 1000)


class test_blob_stream(unittest.TestCase):

  N = 100

  def setUp(self):
    fd, self.fn = tempfile.mkstemp(prefix="bioland_")
    os.close(fd)
    self.data = [data_blob() for i in xrange(self.N)]

  def tearDown(self):
    os.remove(self.fn)

  def test_read_write_fname(self):
    with BlobStreamWriter(self.fn) as bsw:
      for b in self.data:
        bsw.write(b)
    with BlobStreamReader(self.fn) as bsr:
      for d in self.data:
        b = bsr.read()
        self.assertEqual(b, d)
    with BlobStreamReader(self.fn) as bsr:
      for b, d in it.izip(bsr, self.data):
        self.assertEqual(b, d)
    with BlobStreamReader(self.fn) as bsr:
      data2 = bsr.read(len(self.data))
      for b, d in it.izip(data2, self.data):
        self.assertEqual(b, d)

  def test_read_write_fobj(self):
    with open(self.fn, "w") as f:
      bsw = BlobStreamWriter(f)
      for b in self.data:
        bsw.write(b)
    with open(self.fn) as f:
      bsr = BlobStreamReader(f)
      for d in self.data:
        b = bsr.read()
        self.assertEqual(b, d)
    with open(self.fn) as f:
      bsr = BlobStreamReader(f)
      for b, d in it.izip(bsr, self.data):
        self.assertEqual(b, d)
    with open(self.fn) as f:
      bsr = BlobStreamReader(f)
      data2 = bsr.read(len(self.data))
      for b, d in it.izip(data2, self.data):
        self.assertEqual(b, d)


def load_tests(loader, tests, pattern):
  test_cases = (test_blob_stream,)
  suite = unittest.TestSuite()
  for tc in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(tc))
  return suite


if __name__ == '__main__':
  suite = load_tests(unittest.defaultTestLoader, None, None)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
