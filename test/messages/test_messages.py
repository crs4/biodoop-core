# BEGIN_COPYRIGHT
# END_COPYRIGHT

# FIXME: This is not really a test. Just checking that it is
# exporting the right interface.

import unittest
import numpy as np

from bl.core.messages.registry import message_codecs_registry
from bl.core.messages.MessageStreamHeader import MessageStreamHeader
from bl.core.messages.Dummy import Dummy


class TestMessages(unittest.TestCase):

  def test_dummy(self):
    msg_name = 'core.messages.Dummy'
    codec_info = message_codecs_registry.lookup(msg_name)
    v = 'fooo', 10, 0.34
    msg = codec_info.encoder.encode(*v)
    self.assertTrue(isinstance(msg, Dummy))
    new_v = codec_info.decoder.decode(msg)
    self.assertEqual(v, new_v)

  def test_message_stream_header(self):
    msg_name = 'core.messages.MessageStreamHeader'
    codec_info = message_codecs_registry.lookup(msg_name)
    header = {'foo' : 333, 'bar' : [1,2,3], 'fu' : {'a' : 2, 'b' : 3}}
    msg = codec_info.encoder.encode(header)
    self.assertTrue(isinstance(msg, MessageStreamHeader))
    new_header = codec_info.decoder.decode(msg)
    self.assertEqual(header, new_header)


def load_tests(loader, tests, pattern):
  test_cases = (TestMessages,)
  suite = unittest.TestSuite()
  for tc in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(tc))
  return suite


if __name__ == '__main__':
  suite = load_tests(unittest.defaultTestLoader, None, None)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
