"""
What  we would like to do is::

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

**FIXME:** obviously we are not doing this right, it should be
  possible to pass an already opened stream instead of only a fname.

"""

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
    msg = self.pc_info.encoder.encode(payload)
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
    del(header['payload_msg_type'])
    self.header = header

  @property
  def payload_msg_type(self):
    return self.pc_info.name

  def read(self, n=1):
    payload = self.pc_info.klass()
    if n == 1:
      blob = super(MessageStreamReader, self).read(n)
      payload.ParseFromString(blob)
      res = self.pc_info.decoder.decode(payload)
    else:
      res = []
      for blob in super(MessageStreamReader, self).read(n):
        payload.ParseFromString(blob)
        res.append(self.pc_info.decoder.decode(payload))
    return res




