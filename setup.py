# BEGIN_COPYRIGHT
# END_COPYRIGHT
"""BioLand -- Tools for computational biology.

BioLand is a collection of tools for computational biology.
"""
from distutils.core import setup
from distutils.errors import DistutilsSetupError


NAME = 'bl'
DESCRIPTION, LONG_DESCRIPTION = __doc__.split("\n", 1)
LONG_DESCRIPTION = LONG_DESCRIPTION.strip()
URL = "http://biodoop.sourceforge.net"
# DOWNLOAD_URL = ""
LICENSE = 'GPL'
CLASSIFIERS = [
  "Programming Language :: Python",
  "License :: OSI Approved :: GNU General Public License (GPL)",
  "Operating System :: POSIX :: Linux",
  "Topic :: Scientific/Engineering :: Bio-Informatics",
  "Intended Audience :: Science/Research",
  ]
PLATFORMS = ["Linux"]
try:
  with open("VERSION") as f:
    VERSION = f.read().strip()
except IOError:
  raise DistutilsSetupError("failed to read version info")
AUTHOR_INFO = [
  ("Simone Leo", "simone.leo@crs4.it"),
  ("Gianluigi Zanetti", "gianluigi.zanetti@crs4.it"),
  ]
MAINTAINER_INFO = [
  ("Simone Leo", "simone.leo@crs4.it"),
  ]
AUTHOR = ", ".join(t[0] for t in AUTHOR_INFO)
AUTHOR_EMAIL = ", ".join("<%s>" % t[1] for t in AUTHOR_INFO)
MAINTAINER = ", ".join(t[0] for t in MAINTAINER_INFO)
MAINTAINER_EMAIL = ", ".join("<%s>" % t[1] for t in MAINTAINER_INFO)


def write_authors(filename="AUTHORS"):
  with open(filename, "w") as f:
    f.write("%s is developed by:\n" % NAME)
    for name, email in AUTHOR_INFO:
      f.write(" * %s <%s>\n" % (name, email))
    f.write("and maintained by:\n")
    for name, email in MAINTAINER_INFO:
      f.write(" * %s <%s>\n" % (name, email))


write_authors()

setup(
  name=NAME,
  description=DESCRIPTION,
  long_description=LONG_DESCRIPTION,
  url=URL,
  ## download_url=DOWNLOAD_URL,
  license=LICENSE,
  classifiers=CLASSIFIERS,
  author=AUTHOR,
  author_email=AUTHOR_EMAIL,
  maintainer=MAINTAINER,
  maintainer_email=MAINTAINER_EMAIL,
  platforms=PLATFORMS,
  version=VERSION,
  packages=[
    'bl',
    'bl.seq',
    'bl.seq.engines',
    'bl.seq.io',
    'bl.seq.mr',
    'bl.seq.mr.fasta2tab',
    'bl.seq.stats',
    'bl.utils',
    ]
  )
