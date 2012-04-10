# BEGIN_COPYRIGHT
# END_COPYRIGHT

import uuid

from null_logger import NullLogger
from longest_subs import longest_subs


def random_str(prefix="bl_tmp_", suffix=""):
  return "%s%s%s" % (prefix, uuid.uuid4().hex, suffix)
