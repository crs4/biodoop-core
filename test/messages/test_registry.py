# BEGIN_COPYRIGHT
# END_COPYRIGHT

# FIXME: This is not really a test. Just checking that it is
# exporting the right interface.

import unittest, tempfile, os, random
import itertools as it

from bl.core.messages.registry import message_codecs_registry

class test_registry(unittest.TestCase):

  def setUp(self):
    pass

  def tearDown(self):
    pass

  def register_codec(self):
    args = {'name' : 'foo',
            'klass' : 'klassy',
            'encoder': 'foo_encoder',
            'decoder' : 'foo_decoder'}
    self.assertFalse(message_codecs_registry.lookup(args['name']))
    message_codecs_registry.register(args['name'], args['klass'],
                                     args['encoder'], args['decoder'])
    self.assertTrue(message_codecs_registry.lookup(args['name']))
    codec_info = message_codecs_registry.lookup(args['name'])
    self.assertEqual(codec_info.name, args['name'])
    self.assertEqual(codec_info.klass, args['klass'])
    self.assertEqual(codec_info.encoder, args['encoder'])
    self.assertEqual(codec_info.decoder, args['decoder'])

  def runTest(self):
    self.register_codec()

def load_tests(loader, tests, pattern):
  test_cases = (test_registry,)
  suite = unittest.TestSuite()
  for tc in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(tc))
  return suite

if __name__ == '__main__':
  suite = load_tests(unittest.defaultTestLoader, None, None)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
