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

import sys, subprocess, logging, optparse, urllib2, zlib, time
logging.basicConfig(level=logging.DEBUG)

from bl.core.seq.engines.blastall_2_2_21 import Engine


DB = "hg18.fa"
OPTS = {
  "blastall.program": "blastn",
  "blastall.database": DB,
  "blastall.out.tabular": True
  }


class ZStream(object):
  """
  Enables streaming gzip decompression. Inspired by:

  http://rationalpie.wordpress.com/2010/06/02/python-streaming-gzip-decompression
  """
  CHUNK_SIZE = 4096

  def __init__(self, f):
    self.f = f
    self.reset()

  def reset(self):
    self.d = zlib.decompressobj(16+zlib.MAX_WBITS)

  def read(self, size=-1):
    """
    FIXME: if size < header length, the empty string is returned.
    """
    if size >= 0:
      return self.d.decompress(self.f.read(size))
    data = []
    while 1:
      zipped = self.f.read(self.CHUNK_SIZE)
      if zipped == "":
        break
      data.append(self.d.decompress(zipped))
    return "".join(data)

  def seek(self, offset, whence=0):
    self.f.seek(offset, whence)
    self.reset()

  def close(self):
    self.f.close()
      

def get_db():
  logger = logging.getLogger("get_db")
  logger.setLevel(logging.DEBUG)
  site = "hgdownload.cse.ucsc.edu"
  outf = open(DB, "wb")
  for chr_id in map(str, range(1,23)) + list("XYM"):
    url = "ftp://%s/goldenPath/hg18/chromosomes/chr%s.fa.gz" % (site, chr_id)
    f = ZStream(urllib2.urlopen(url))
    logger.info("getting chromosome %s" % chr_id)
    while 1:
      data = f.read(4096)
      if not data:
        break
      outf.write(data)
  outf.close()
  return outf.name


def format_db():
  poll_interval = 5
  logger = logging.getLogger("format_db")
  logger.setLevel(logging.DEBUG)
  cmd = "formatdb -i %s -p F -o T" % DB
  logger.info('running "%s" (can take a while...)' % cmd)
  p = subprocess.Popen(cmd, shell=True)
  while True:
    p.poll()
    if p.returncode is None:
      sys.stderr.write(".")
      sys.stderr.flush()
      time.sleep(poll_interval)
    else:
      sys.stderr.write("\n")
      return p.returncode

def make_parser():
    usage = "%prog [OPTIONS] IN_F OUT_F"
    parser = optparse.OptionParser(usage)
    parser.add_option("--get-db", action="store_true", help="get db")
    parser.add_option("--format-db", action="store_true", help="format db")
    return parser


def main(argv):

  logger = logging.getLogger("main")
  logger.setLevel(logging.DEBUG)
  
  parser = make_parser()
  opt, args = parser.parse_args(argv)
  
  try:
    input_fn = args[1]
    output_fn = args[2]
  except IndexError:
    parser.print_help()
    sys.exit(2)
  if opt.get_db:
    get_db()
  if opt.format_db:
    retcode = format_db()
    if retcode:
      logging.warn("formatdb returned %d" % retcode)

  OPTS["blastall.input.file"] = input_fn
  OPTS["blastall.output.file"] = output_fn
  engine = Engine(logger=logger)
  engine.blastall(opts=OPTS)


if __name__ == "__main__":
  main(sys.argv)
