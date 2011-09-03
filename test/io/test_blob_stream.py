# BEGIN_COPYRIGHT
# END_COPYRIGHT

# FIXME: This is not really a test. Just checking that it is
# exporting the right interface.

import unittest, tempfile, os, random
import itertools as it

from bl.core.io.blob_stream import BlobStreamWriter, BlobStreamReader


class test_blob_stream(unittest.TestCase):

  def setUp(self):
    fd, self.fn = tempfile.mkstemp(prefix="bioland_")
    os.close(fd)

  def tearDown(self):
    os.remove(self.fn)

  def read_write(self):
    N = 100
    def data_blob():
      char = chr(random.randint(ord('A'), ord('Z')))
      return char * random.randint(10, 1000)
    data = [data_blob() for i in range(N)]
    bsw = BlobStreamWriter(self.fn)
    for b in data:
      bsw.write(b)
    bsw.close()

    bsr = BlobStreamReader(self.fn)
    for d in data:
      b = bsr.read()
      self.assertEqual(b, d)

    bsr = BlobStreamReader(self.fn)
    for b, d in it.izip(bsr, data):
      self.assertEqual(b, d)

    bsr = BlobStreamReader(self.fn)
    data2 = bsr.read(len(data))
    for b, d in it.izip(data2, data):
      self.assertEqual(b, d)


  def runTest(self):
    self.read_write()

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
