# BEGIN_COPYRIGHT
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
