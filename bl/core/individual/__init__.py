# BEGIN_COPYRIGHT
# END_COPYRIGHT

"""
Tools for handling experimental subjects.
"""

import gender as gender_


class Individual(object):

  def __init__(self, id_, gender=gender_.UNKNOWN, father=None, mother=None):
    self.id = id_
    self.__gender = self.__father = self.__mother = None
    self.gender, self.father, self.mother = gender, father, mother
    self.children = set()

  def set_gender(self, gender):
    self.__gender = gender_.MAP[gender]

  def get_gender(self):
    return self.__gender

  gender = property(get_gender, set_gender)

  def set_father(self, father):
    self.__father = father
    try:
      self.__father.children.add(self)
    except AttributeError:
      pass

  def get_father(self):
    return self.__father

  father = property(get_father, set_father)

  def set_mother(self, mother):
    self.__mother = mother
    try:
      self.__mother.children.add(self)
    except AttributeError:
      pass

  def get_mother(self):
    return self.__mother

  mother = property(get_mother, set_mother)

  @property
  def father_id(self):
    return self.father.id if self.father else None

  @property
  def mother_id(self):
    return self.mother.id if self.mother else None

  def is_male(self):
    return self.gender == gender_.MALE

  def is_female(self):
    return self.gender == gender_.FEMALE

  def is_founder(self):
    return self.father is None and self.mother is None

  def __hash__(self):
    return hash(self.id)

  def __eq__(self, obj):
    return hash(self) == hash(obj)

  def __ne__(self, obj):
    return not self.__eq__(obj)

  def __repr__(self):
    return '%s (%s) [%s, %s] {%s}' % (
      self.id, self.gender,
      self.father_id, self.mother_id,
      ", ".join(_.id for _ in sorted(self.children))
      )
