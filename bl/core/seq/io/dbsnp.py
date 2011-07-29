# BEGIN_COPYRIGHT
# END_COPYRIGHT

import re

from fasta import RawFastaReader
from bl.core.utils import NullLogger


class BadSnpPosError(Exception): pass
class BadDbSnpHeader(Exception): pass


class DbSnpReader(RawFastaReader):
  """
  Iterates through an NCBI dbSNP file, yielding an (rs_id, left_flank,
  alleles, right_flank) tuple for each SNP entry. See::

    ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606/rs_fasta
  
  NOTE: dbSNP dumps downloaded from NCBI can have a trailing 'comment'::

    # ================ 
    # File created at: 
    # `date` 
    # ================

  Such 'comments' are not legal in FASTA files and this reader does
  not handle them in any special way (i.e., if present, they will be
  included in the last sequence).
  """
  def __init__(self, f, offset=0, split_size=None, logger=None):
    super(DbSnpReader, self).__init__(f, offset, split_size)
    self.logger = logger or NullLogger()

  def next(self):
    self.header, self.seq = super(DbSnpReader, self).next()
    try:
      self.rs_id, self.pos, alleles = self.__parse_header()
    except BadDbSnpHeader:
      self.logger.error("bad header %r" % (self.header))
      return self.next()      
    try:
      left_flank, right_flank = self.__parse_seq()
    except BadSnpPosError:
      self.logger.error("%r: seq[%d] does not exist -- skipping"
                        % (self.rs_id, self.pos))
      return self.next()
    return self.rs_id, left_flank, alleles, right_flank

  def __parse_header(self):
    try:
      rs_id = re.search(r'rs\d+', self.header).group()
      pos = int(re.search(r'pos\s*=\s*(\d+)', self.header).groups()[0]) - 1
      alleles = re.search(r'alleles\s*=\s*"([^"]+)', self.header).groups()[0]
    except AttributeError:
      raise BadDbSnpHeader
    return rs_id, pos, alleles

  def __parse_seq(self):
    seq = self.seq.replace(" ", "").upper()
    try:
      snp = seq[self.pos]
    except IndexError:
      raise BadSnpPosError
    if snp in "ACGT":
      self.logger.warn("%r: seq[%d] has unexpected value %r"
                       % (self.rs_id, self.pos, seq[self.pos]))
    return seq[:self.pos], seq[self.pos+1:]
