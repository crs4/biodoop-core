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
