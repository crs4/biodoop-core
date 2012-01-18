# BEGIN_COPYRIGHT
# END_COPYRIGHT

from details.Dummy_pb2 import Dummy
from registry import message_codecs_registry


class Encoder(object):
  
  def encode(self, a_string, a_int, a_float):
    m = Dummy()
    m.a_string, m.a_int, m.a_float = a_string, a_int, a_float
    return m

class Decoder(object):
  
  def decode(self, m):
    assert isinstance(m, Dummy)
    return m.a_string, m.a_int, m.a_float


message_codecs_registry.register('core.messages.Dummy',
                                 Dummy,
                                 Encoder(), Decoder())
