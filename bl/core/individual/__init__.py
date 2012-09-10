# BEGIN_COPYRIGHT
# END_COPYRIGHT

"""
Tools for handling experimental subjects.
"""

class Individual(object):

  GENDER_MAP = dict.fromkeys(["FEMALE", "female", "Female", "F", "f"], "F")
  GENDER_MAP.update(dict.fromkeys(["MALE", "male", "Male", "M", "m"], "M"))

  def __init__(self, id_, gender, father=None, mother=None):
    self.id = id_
    self.__gender = self.__father = self.__mother = None
    self.gender, self.father, self.mother = gender, father, mother
    self.children = set()

  def set_gender(self, gender):
    self.__gender = self.GENDER_MAP[gender]

  def get_gender(self):
    return self.__gender

  def del_gender(self):
    del self.__gender

  gender = property(get_gender, set_gender, del_gender)

  def set_father(self, father):
    self.__father = father
    try:
      self.__father.children.add(self)
    except AttributeError:
      pass

  def get_father(self):
    return self.__father

  def del_father(self):
    del self.__father

  father = property(get_father, set_father, del_father)

  def set_mother(self, mother):
    self.__mother = mother
    try:
      self.__mother.children.add(self)
    except AttributeError:
      pass

  def get_mother(self):
    return self.__mother

  def del_mother(self):
    del self.__mother

  mother = property(get_mother, set_mother, del_mother)

  def is_male(self):
    return self.gender == "M"

  def is_female(self):
    return self.gender == "F"

  def is_founder(self):
    return self.father is None and self.mother is None

  def __hash__(self):
    return hash(self.id)

  def __eq__(self, obj):
    return hash(self) == hash(obj)

  def __ne__(self, obj):
    return not self.__eq__(obj)

  def __str__(self):
    fid = self.father.id if self.father else "None"
    mid = self.mother.id if self.mother else "None"
    return '%s (%s) [%s, %s] {%s}' % (
      self.id, self.gender, fid, mid, ", ".join(_.id for _ in self.children)
      )
