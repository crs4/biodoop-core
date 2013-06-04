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
