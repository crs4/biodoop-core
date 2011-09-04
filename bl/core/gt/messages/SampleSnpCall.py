from details.SampleSnpCall_pb2 import SampleSnpCall as SampleSnpCall
from details.SampleSnpCall_pb2 import SnpCall as SnpCall
from bl.core.messages.registry import message_codecs_registry


class Encoder(object):
  def encode(self, sample_id, snp_id, call, confidence, sig_A, sig_B,
             weight_AA, weight_AB, weight_BB)
    """
    Will encode  to a SampleSnpCall msg.
    """
    m = SampleSnpCall()
    m.sample_id, m.snp_id, m.call, m.confidence = \
                 sample_id, snp_id, call, confidence
    m.sig_A, m.sig_B = sig_A, sig_B
    m.weight_AA, m.weight_AB, m.weight_BB = weight_AA, weight_AB, weight_BB
    return m

class Decoder(object):
  def decode(self, m):
    """
    Will decode a SampleSnpCall mgs.
    """
    assert isinstance(m, SampleSnpCall)
    return (m.sample_id, m.snp_id, m.call, m.confidence,
            m.sig_A, m.sig_B,
            m.weight_AA, m.weight_AB, m.weight_BB)


message_codecs_registry.register('core.gt.messages.SampleSnpCall',
                                 SampleSnpCall,
                                 Encoder(), Decoder())

