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
A simple facility for message codec management.
"""

class MessageCodecInfo(object):
  
  def __init__(self, name, klass, encoder, decoder):
    self.name = name
    self.klass = klass
    self.encoder = encoder
    self.decoder = decoder


class MessageCodecsRegistry(object):
  
  def __init__(self):
    self.known_codecs = {}

  def register(self, name, klass, encoder, decoder):
    self.known_codecs[name] = MessageCodecInfo(name, klass, encoder, decoder)

  def lookup(self, name):
    return self.known_codecs.get(name, None)

  def deregister(self, name):
    if name not in self.known_codecs:
      raise ValueError('no codecs for %s message type' % name)
    del self.known_codecs[name]


message_codecs_registry = MessageCodecsRegistry()
