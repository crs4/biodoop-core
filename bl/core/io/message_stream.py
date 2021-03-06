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

"""
..code-block:: python

    payload_msg_type = 'core.messages.Dummy'
    header = {'foo' : 'hello', 'bar' : [1,2,3]}
    stream = MessageStreamWriter(fname, payload_msg_type, header)
    for d in data:
      stream.write(d)
    stream.close()
    stream = MessageStreamReader(fname)
    datax = [stream.read() for i in range(len(data))]
    stream.close()

FIXME: it should be possible to pass an open stream instead of a file name.
"""

import collections
from blob_stream import BlobStreamWriter, BlobStreamReader
from bl.core.messages.registry import message_codecs_registry as CDSREG


HEADER_MSG_TYPE  = 'core.messages.MessageStreamHeader'


class MessageStreamWriter(BlobStreamWriter):

  def __init__(self, fname, payload_msg_type, header={}):
    super(MessageStreamWriter, self).__init__(fname)
    self.payload_msg_type = payload_msg_type
    self.hc_info = CDSREG.lookup(HEADER_MSG_TYPE)
    self.pc_info = CDSREG.lookup(payload_msg_type)
    self.header = header
    header = self.header.copy()
    header['payload_msg_type'] = self.payload_msg_type
    header_msg = self.hc_info.encoder.encode(header)
    super(MessageStreamWriter, self).write(header_msg.SerializeToString())

  def write(self, payload):
    if isinstance(payload, collections.Mapping):
      msg = self.pc_info.encoder.encode(**payload)
    elif isinstance(payload, collections.Sequence):
      msg = self.pc_info.encoder.encode(*payload)
    else:
      raise TypeError("payload must be either a sequence or a mapping")
    super(MessageStreamWriter, self).write(msg.SerializeToString())


class MessageStreamReader(BlobStreamReader):

  def __init__(self, fname):
    super(MessageStreamReader, self).__init__(fname)
    self.hc_info = CDSREG.lookup(HEADER_MSG_TYPE)
    hmsg_s = super(MessageStreamReader, self).read(1)
    hmsg = self.hc_info.klass()
    hmsg.ParseFromString(hmsg_s)
    header = self.hc_info.decoder.decode(hmsg)
    self.pc_info = CDSREG.lookup(header['payload_msg_type'])
    if self.pc_info is None:
      raise ValueError("unknown payload msg type %r" %
                       (header['payload_msg_type'],))
    del(header['payload_msg_type'])
    self.header = header

  @property
  def payload_msg_type(self):
    return self.pc_info.name

  def read(self, n=1):
    payload = self.pc_info.klass()
    if n == 1:
      blob = super(MessageStreamReader, self).read(n)
      if blob:
        payload.ParseFromString(blob)
        res = self.pc_info.decoder.decode(payload)
      else:
        res = None
    else:
      res = []
      for blob in super(MessageStreamReader, self).read(n):
        payload.ParseFromString(blob)
        res.append(self.pc_info.decoder.decode(payload))
    return res
