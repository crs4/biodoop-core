from details.MessageStreamHeader_pb2 import MessageStreamHeader as MessageStreamHeader
from registry import message_codecs_registry
import json

class Encoder(object):
  def encode(self, h):
    """
    Converts a dict of key values into a MessageStreamHeader object.
    It expects keys to be strings and values to be encodable by json.
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
    Will decode a MessageStreamHeader to a dict.
    """
    assert isinstance(m, MessageStreamHeader)
    h = {}
    for kv in m.key_value:
      h[kv.key] = json.loads(kv.value)
    return h


message_codecs_registry.register('core.messages.MessageStreamHeader',
                                 MessageStreamHeader,
                                 Encoder(), Decoder())

