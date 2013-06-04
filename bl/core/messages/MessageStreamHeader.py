# BEGIN_COPYRIGHT
# 
# Copyright (C) 2009-2013 CRS4.
# 
# This file is part of biodoop-core.
# 
# biodoop-core is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
# 
# biodoop-core is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
# 
# You should have received a copy of the GNU General Public License along with
# biodoop-core.  If not, see <http://www.gnu.org/licenses/>.
# 
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
