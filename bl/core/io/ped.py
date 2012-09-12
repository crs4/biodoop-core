# BEGIN_COPYRIGHT
# END_COPYRIGHT

"""
Tools for dealing with pedigree files.

http://www.sph.umich.edu/csg/abecasis/merlin/tour/input_files.html
"""

from bl.core.individual import Individual


def read_ped(f, sep=None):
  """
  Read only the pedigree part (first 5 columns) of a PED file.

  Return a dictionary that maps IDs (assumed unique) to individuals.
  Needs no special ordering of PED lines (i.e., children may be listed
  before their parents); unknown father/mother IDs (columns 3-4) can
  be coded as anything that's not part of the set of individual IDs
  (column 2).
  """
  ped = {}
  unresolved = {}  # ID -> (role, children_IDs)
  for line in f:
    _, id_, father_id, mother_id, gender = line.strip().split(sep, 5)[:5]
    if id_ in ped:
      raise RuntimeError("Duplicate ID: %s" % id_)
    parents = []
    for role, pid in ("father", father_id), ("mother", mother_id):
      try:
        p = ped[pid]
      except KeyError:
        p = None
        unresolved.setdefault(pid, (role, set()))[1].add(id_)
      parents.append(p)
    father, mother = parents
    ped[id_] = Individual(id_, gender, father, mother)
    try:
      role, children_ids = unresolved[id_]
    except KeyError:
      pass
    else:
      for cid in children_ids:
        setattr(ped[cid], role, ped[id_])
      del unresolved[id_]
  return ped
