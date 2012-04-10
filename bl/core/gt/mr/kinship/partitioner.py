# BEGIN_COPYRIGHT
# END_COPYRIGHT

import random
import pydoop.pipes as pp


class Partitioner(pp.Partitioner):

  def partition(self, key, numOfReduces):
    return random.randint(0, numOfReduces-1)
