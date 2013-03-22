# BEGIN_COPYRIGHT
# END_COPYRIGHT

from details.SampleSnpCall_pb2 import SampleSnpCall
from bl.core.messages.registry import message_codecs_registry


class Encoder(object):
  
  def encode(self, sample_id, snp_id, call, confidence, sig_A, sig_B,
             w_AA, w_AB, w_BB):
    m = SampleSnpCall()
    m.sample_id, m.snp_id = sample_id, snp_id
    m.call, m.confidence = call, confidence
    m.sig_A, m.sig_B = sig_A, sig_B
    m.w_AA, m.w_AB, m.w_BB = w_AA, w_AB, w_BB
    return m


class Decoder(object):
  
  def decode(self, m):
    assert isinstance(m, SampleSnpCall)
    return (m.sample_id, m.snp_id,
            m.call, m.confidence,
            m.sig_A, m.sig_B,
            m.w_AA, m.w_AB, m.w_BB)


message_codecs_registry.register('core.gt.messages.SampleSnpCall',
                                 SampleSnpCall,
                                 Encoder(), Decoder())
