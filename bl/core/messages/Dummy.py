from details.Dummy_pb2 import Dummy as Dummy
from registry import message_codecs_registry
import json

class Encoder(object):
  def encode(self, a_string, a_int, a_float):
    """
    Will encode the tuple (a_string, a_int, a_float) to a Dummy msg.
    """
    m = Dummy()
    m.a_string, m.a_int, m.a_float = a_string, a_int, a_float
    return m

class Decoder(object):
  def decode(self, m):
    """
    Will decode a Dummy to the tuple (a_string, a_int, a_float)
    """
    assert isinstance(m, Dummy)
    return m.a_string, m.a_int, m.a_float

message_codecs_registry.register('core.messages.Dummy',
                                 Dummy,
                                 Encoder(), Decoder())

