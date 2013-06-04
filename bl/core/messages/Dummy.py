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
