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

import os
from bl.core.utils.pspawner import ProcessSpawner


class BlastnEngine(object):

    EXE = "/usr/bin/blastn"
    NAME = "blastn"
    TMP_DIR = os.environ.get("TMPDIR", "/var/tmp")
    FLAG_MAP = {
        "task": "-task",
        "database": "-db",
        "input.file": "-query",
        "output.file": "-out",
        "out.xml": "-outfmt 5",
        "out.tabular": "-outfmt 6",
        "evalue": "-evalue",
        "gap.cost": "-gapopen",
        "word.size": "-word_size",
        "filter": "-dust",
        }

    def __init__(self, exe_file=EXE, **kwargs):
        self.wrapper = ProcessSpawner(exe_file, **kwargs)
        for opt, flag in self.FLAG_MAP.iteritems():
            self.wrapper.add_opt_mapper("%s.%s" % (self.NAME, opt), flag)

    def run(self, args=[], opts={}):
        self.wrapper.run(args, opts)
