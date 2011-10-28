# BEGIN_COPYRIGHT
# END_COPYRIGHT

# FIXME: This is not really a test. Just checking that it is
# exporting the right interface.

import unittest, tempfile, os
import itertools as it

from bl.core.io.message_stream import MessageStreamWriter, MessageStreamReader


class test_message_stream(unittest.TestCase):

  def setUp(self):
    fd, self.fn = tempfile.mkstemp(prefix="bioland_")
    os.close(fd)

  def tearDown(self):
    os.remove(self.fn)

  def do_check_header(self, expected_header, header):
    for k, v in header.iteritems():
      self.assertEqual(v, expected_header[k])
    for k, v in expected_header.iteritems():
      self.assertEqual(v, header[k])

  def header(self):
    payload_msg_type = 'core.messages.Dummy'
    header = {'foo' : 'hello',
              'bar' : [1,2,3],
              'foobar' : {'a' : 1, 'b' : 'ww', 'c' : 0.33}}
    stream = MessageStreamWriter(self.fn, payload_msg_type, header)
    self.do_check_header(header, stream.header)
    stream.close()

    stream = MessageStreamReader(self.fn)
    self.assertEqual(stream.payload_msg_type, payload_msg_type)
    self.do_check_header(header, stream.header)

  def generate_payload_dataset(self, N):
    data = []
    for i in range(N):
      d = ('data-item-%04d' % i, i, 0.5*i + 0.01)
      data.append(d)
    return data

  def do_check_data(self, expected_data, data):
    for dx, d in it.izip(expected_data, data):
      self.assertEqual(d[0], dx[0])
      self.assertEqual(d[1], dx[1])
      self.assertAlmostEqual(d[2], dx[2], 5)

  def payload_1(self):
    payload_msg_type = 'core.messages.Dummy'
    header = {'foo' : 'hello', 'bar' : [1,2,3]}
    stream = MessageStreamWriter(self.fn, payload_msg_type, header)
    self.assertEqual(stream.payload_msg_type, payload_msg_type)
    self.do_check_header(header, stream.header)

    N = 10
    data = self.generate_payload_dataset(N)
    for d in data:
      stream.write(d)
    stream.close()

    stream = MessageStreamReader(self.fn)
    self.assertEqual(stream.payload_msg_type, payload_msg_type)
    self.do_check_header(header, stream.header)

    datax = [stream.read() for i in range(N)]
    stream.close()
    self.do_check_data(data, datax)

  def payload_2(self):
    payload_msg_type = 'core.messages.Dummy'
    header = {'foo' : 'hello', 'bar' : [1,2,3]}
    stream = MessageStreamWriter(self.fn, payload_msg_type, header)
    self.assertEqual(stream.payload_msg_type, payload_msg_type)
    self.do_check_header(header, stream.header)

    N = 10
    data = self.generate_payload_dataset(N)
    for d in data:
      stream.write(d)
    stream.close()

    stream = MessageStreamReader(self.fn)
    self.assertEqual(stream.payload_msg_type, payload_msg_type)
    self.do_check_header(header, stream.header)

    datax = stream.read(N)
    stream.close()
    self.do_check_data(data, datax)

  def runTest(self):
    self.header()
    self.payload_1()
    self.payload_2()


def load_tests(loader, tests, pattern):
  test_cases = (test_message_stream,)
  suite = unittest.TestSuite()
  for tc in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(tc))
  return suite


if __name__ == '__main__':
  suite = load_tests(unittest.defaultTestLoader, None, None)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
