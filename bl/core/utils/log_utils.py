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
Utilities for logging.
"""
import logging


LOG_FORMAT = "%(asctime)s|%(levelname)-8s|%(message)s"
LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class _NullHandler(logging.Handler):
  def emit(self, record):
    pass


class NullLogger(logging.Logger):
  def __init__(self):
    logging.Logger.__init__(self, "null")
    self.propagate = 0
    self.handlers = [_NullHandler()]


def get_logger(name, level="WARNING", filename=None, mode="a"):
  logger = logging.getLogger(name)
  if not isinstance(level, int):
    try:
      level = getattr(logging, level)
    except AttributeError:
      raise ValueError("unsupported literal log level: %s" % level)
    logger.setLevel(level)
  if filename:
    handler = logging.FileHandler(filename, mode=mode)
  else:
    handler = logging.StreamHandler()
  formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATEFMT)
  handler.setFormatter(formatter)
  logger.addHandler(handler)
  return logger
