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

from itertools import izip


def longest_subs(seqs, reverse=False):
  """
  Find longest common leading (trailing if reverse is True) subsequence.
  """
  if not seqs:
    return None
  if len(seqs) == 1:
    return seqs[0]
  if not reverse:
    it = izip(*seqs)
  else:
    it = izip(*(reversed(s) for s in seqs))
  for i, chars in enumerate(it):
    if len(set(chars)) > 1:
      L = i
      break
  else:
    L = i + 1
  if L:
    return seqs[0][-L:] if reverse else seqs[0][:L]
  return seqs[0].__class__()
