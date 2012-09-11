# BEGIN_COPYRIGHT
# END_COPYRIGHT

"""
Gender encoding.
"""

from collections import defaultdict

UNKNOWN = 0
MALE = 1
FEMALE = 2

MALE_LABELS = ["MALE", "Male", "male", "M", "m", "1"]
FEMALE_LABELS = ["FEMALE", "Female", "female", "F", "f", "2"]

MAP = defaultdict.fromkeys(MALE_LABELS, MALE)
MAP.update(dict.fromkeys(FEMALE_LABELS, FEMALE))
# anything that's not either male or female is unknown
MAP.default_factory = int
