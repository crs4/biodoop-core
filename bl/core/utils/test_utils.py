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


class map_context(object):

  def __init__(self, jc, input_split):
    self.job_conf = jc
    self.input_split = input_split
    self.counters = {}
    self.emitted = {}
    self.status_messages = []

  def getJobConf(self):
    return self.job_conf

  def getInputSplit(self):
    return self.input_split

  def getInputKey(self):
    return self.input_key

  def getInputValue(self):
    return self.input_value

  def getCounter(self, group, name):
    k = '%s:%s' % (group, name)
    self.counters[k] = 0
    return k

  def incrementCounter(self, counter, amount):
    self.counters[counter] += amount

  def emit(self, k, v):
    if not isinstance(k, str):
      raise TypeError("key must be a string (it's a %s)" % type(k))
    if not isinstance(v, str):
      raise TypeError("value must be a string (it's a %s)" % type(v))

    if not self.emitted.has_key(k):
      self.emitted[k] = []
    self.emitted[k].append(v)

  def progress(self):
    pass

  def setStatus(self, status):
    self.status_messages.append(status)


class reduce_context(object):
  """
  @param jc:  JobConf object
  @param values:  a list of dictionaries.  The first dictionary
    needs to have a 'key' and a 'value'.  Each subsequent one
    only needs a 'value'.
  """
  def __init__(self, jc, values):
    self.job_conf = jc
    self.counters = {}
    self.emitted = {}
    self.counter = -1
    self.values = values

  def nextValue(self):
    self.counter += 1
    return self.counter < len(self.values)

  def getJobConf(self):
    return self.job_conf

  def getInputKey(self):
    return self.values[0]['key']

  def getInputValue(self):
    return self.values[self.counter]['value']

  def emit(self, k, v):
    if not isinstance(k, str):
      raise TypeError("key must be a string (it's a %s)" % type(k))
    if not isinstance(v, str):
      raise TypeError("value must be a string (it's a %s)" % type(v))

    if not self.emitted.has_key(k):
      self.emitted[k] = []
    self.emitted[k].append(v)

  def progress(self):
    pass

  def setStatus(self, status):
    pass

  def getCounter(self, group, name):
    k = '%s:%s' % (group, name)
    self.counters[k] = 0
    return k

  def incrementCounter(self, counter, amount):
    self.counters[counter] += amount

  def add_value(self, key, value):
    """
    Convenience method to insert a (key, value) pair to the data that
    will be returned by this reduce_context.  
    It is recommended that this method be used in place of directly
    modifying the object's 'value' attribute so that in the future
    we may easily change the internals.
    """
    if self.values:
      if self.values[0]['key'] == key:
        self.values.append({'value': value })
      else:
        raise ValueError(
          "key %s doesn't match the key that's already been inserted (%s).  " +
          "Sorry, but for now we only support a single key value" %
          (key, self.values[0]['key'])
          )
    else: # empty values
      self.values.append({'key':key, 'value':value})
