# BEGIN_COPYRIGHT
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
