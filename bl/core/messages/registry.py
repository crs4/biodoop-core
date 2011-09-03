"""
A naive facility for Message Codecs management
==============================================

FIXME...

"""

class MessageCodecInfo(object):
  def __init__(self, name, klass, encoder, decoder):
    self.name = name
    self.klass = klass
    self.encoder = encoder
    self.decoder = decoder

class MessageCodecsRegistry(object):
  def __init__(self):
    self.known_codecs = {}

  def register(self, name, klass, encoder, decoder):
    self.known_codecs[name] = MessageCodecInfo(name, klass, encoder, decoder)

  def lookup(self, name):
    return self.known_codecs.get(name, None)

  def deregister(self, name):
    if name not in self.known_codecs:
      raise ValueError('no codecs for %s message type' % name)
    del self.known_codecs[name]


message_codecs_registry = MessageCodecsRegistry()
