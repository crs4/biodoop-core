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

COMPLEMENT = {  # http://www.chem.qmul.ac.uk/iubmb/misc/naseq.html
    'G' : 'C',
    'A' : 'T',
    'T' : 'A',
    'C' : 'G',
    'R' : 'Y',
    'Y' : 'R',
    'M' : 'K',
    'K' : 'M',
    'S' : 'S',
    'W' : 'W',
    'H' : 'D',
    'B' : 'V',
    'V' : 'B',
    'D' : 'H',
    'N' : 'N',
    'X' : 'X',
    'g' : 'c',
    'a' : 't',
    't' : 'a',
    'c' : 'g',
    'r' : 'y',
    'y' : 'r',
    'm' : 'k',
    'k' : 'm',
    's' : 's',
    'w' : 'w',
    'h' : 'd',
    'b' : 'v',
    'v' : 'b',
    'd' : 'h',
    'n' : 'n',
    'x' : 'x'
    }


def reverse_complement(seq):
  rc_it = (COMPLEMENT.get(c, c) for c in reversed(seq))
  if isinstance(seq, basestring):
    return "".join(rc_it)
  elif isinstance(seq, tuple):
    return tuple(rc_it)
  else:
    return list(rc_it)
