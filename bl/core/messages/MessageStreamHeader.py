# BEGIN_COPYRIGHT
# END_COPYRIGHT

import json

from details.MessageStreamHeader_pb2 import MessageStreamHeader
from registry import message_codecs_registry


class Encoder(object):
  
  def encode(self, h):
    """
    Converts a dict into a MessageStreamHeader object. It expects
    keys to be strings and values to be encodable by json.
    """
    assert isinstance(h, dict)
    m = MessageStreamHeader()
    for k, v in h.iteritems():
      kv = m.key_value.add()
      kv.key, kv.value = k, json.dumps(v, separators=(',',':'))
    return m


class Decoder(object):
  
  def decode(self, m):
    """
    Converts a MessageStreamHeader to a dict.
    """
    assert isinstance(m, MessageStreamHeader)
    h = {}
    for kv in m.key_value:
      h[kv.key] = json.loads(kv.value)
    return h


message_codecs_registry.register('core.messages.MessageStreamHeader',
                                 MessageStreamHeader,
                                 Encoder(), Decoder())
