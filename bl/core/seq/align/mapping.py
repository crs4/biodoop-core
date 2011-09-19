# BEGIN_COPYRIGHT
# END_COPYRIGHT

import re, array
from itertools import izip

from sam_flags import *


class Mapping(object):
  """
  Abstract class defining an interface to describe sequence mapping. A
  concrete implementation needs to set the attributes to appropriate
  values and implement any abstract methods (e.g. get_seq_5).

  Attributes:
  self.flag: SAM flag bits
  self.isize: insert size
  self.mpos: mate's position, or 0
  self.mtid: mate's reference , or '=' if same as query's reference, or None
  self.m_ref_id: mate's reference id, or None
  self.pos: this hit's position, or 0
  self.qual: mapq value for this alignment
  self.tid: this hit's reference sequence, or None
  self.ref_id: this hit's reference id, or None
  """
  def __init__(self):
    self.flag = 0
    self.isize = 0
    self.mpos = 0
    self.mtid = None
    self.m_ref_id = None
    self.pos = 0
    self.qual = 0
    self.tid = None
    self.ref_id = None

  def get_name(self):
    raise NotImplementedError

  def get_seq_5(self):
    raise NotImplementedError

  def get_seq_len(self):
    return len(self.get_seq_5())

  def get_base_qualities(self):
    """
    If base qualities are available, return a byte array.array of
    Phred quality scores, one per base, 0-based. If base qualities
    aren't available, return None.
    """
    raise NotImplementedError

  def get_ascii_base_qual(self):
    """
    Return a string containing the Phred base quality score
    encoded in ASCII-33 (ASCII character corresponding to
    quality score + 33)
    """
    if not hasattr(self, '__ascii_base_qual'):
      self.__ascii_base_qual = ''.join([
        chr(q+33) for q in self.get_base_qualities()
        ])
    return self.__ascii_base_qual

  def get_cigar(self):
    """
    Return the cigar list for this mapping. Each element is a pair
    (length, action), where action is a letter for one of the
    alignment actions (e.g. M, I, D, S). If unmapped, return an empty
    list.
    """
    raise NotImplementedError

  def get_cigar_str(self):
    if not hasattr(self, '__cigar_str'):
      self.__cigar_str = "".join(['%d%s' % t for t in self.get_cigar()]) or "*"
    return self.__cigar_str

  def get_untrimmed_pos(self):
    """
    For a reversed, trimmed fragment, the 5' coordinate pos refers to
    a base somewhere within the fragment (not at its start or end).
    This method takes into account the trimming (if any) and
    calculates the pos of the 5'-most base of the untrimmed fragment.
    """
    if not hasattr(self, "__untrimmed_pos"):
      if self.is_unmapped():
        raise ValueError("sequence is not mapped")
      upos = self.pos
      if self.is_on_reverse():
        clip_len = self.tag_value("XC") or self.get_seq_len()
        upos = upos - (self.get_seq_len() - clip_len)
      self.__untrimmed_pos = upos
    return self.__untrimmed_pos

  ####################################
  # Tag methods
  ####################################
  def each_tag(self):
    """
    Generator for this mapping's tags. Each tag is a tuple (tag_name,
    value_type, value)
    """
    raise NotImplementedError

  def tag_value(self, tag_name):
    """
    Get the value for a tag, if present. Returns::
    
      - integer (if tag type is 'i')
      - float (if tag type is 'f')
      - string
      - None, if tag isn't present
    """
    for tag in self.each_tag():
      if tag[0] == tag_name:
        if tag[1] == 'i':
          value = int(tag[2])
        elif tag[1] == 'f':
          value = float(tag[2])
        else:
          value = tag[2]
        return value
    return None

  ####################################
  # Flag methods
  ####################################
  def flag_string(self):
    """
    Return a string indicating symbolically the flags set for this mapping.
    
    Symbol legend:
    
    p: paired                  FPD 0x001
    P: properly paired         FPP 0x002
    u: query unmapped          FSU 0x004
    U: mate unmapped           FMU 0x008
    r: query on reverse strand FSR 0x010
    R: mate on reverse strand  FMR 0x020
    1: first read in a pair    FR1 0x040
    2: second read in a pair   FR2 0x080
    s: not a primary alignment FSC 0x100
    f: fails quality checks    FQC 0x200
    d: duplicate               FDP 0x400
    """
    names = ['p', 'P', 'u', 'U', 'r', 'R', '1', '2', 's', 'f', 'd']
    values = [0x0001, 0x0002, 0x0004, 0x0008, 0x0010, 0x0020,
              0x0040, 0x0080, 0x0100, 0x0200, 0x0400]
    return ''.join([ n for n,v in izip(names, values) if self.flag & v != 0 ])

  def is_paired(self):
    return self.flag & SAM_FPD != 0

  def is_properly_paired(self):
    return self.flag & SAM_FPP != 0

  def is_mapped(self):
    return self.flag & SAM_FSU == 0

  def is_unmapped(self):
    return self.flag & SAM_FSU != 0

  def is_mate_mapped(self):
    return self.flag & SAM_FMU == 0

  def is_mate_unmapped(self):
    return self.flag & SAM_FMU != 0

  def is_on_reverse(self):
    return self.flag & SAM_FSR != 0

  def is_mate_on_reverse(self):
    return self.flag & SAM_FMR != 0

  def is_read1(self):
    return self.flag & SAM_FR1 != 0

  def is_read2(self):
    return self.flag & SAM_FR2 != 0

  def is_secondary_align(self):
    return self.flag & SAM_FSC != 0

  def is_failed_qc(self):
    return self.flag & SAM_FQC != 0

  def is_duplicate(self):
    return self.flag & SAM_FDP != 0

  def set_paired(self, value):
    self.__set_flag(value, SAM_FPD)

  def set_properly_paired(self, value):
    self.__set_flag(value, SAM_FPP)

  def set_mapped(self, value):
    self.__set_flag(not value, SAM_FSU)

  def set_mate_mapped(self, value):
    self.__set_flag(not value, SAM_FMU)

  def set_on_reverse(self, value):
    self.__set_flag(value, SAM_FSR)

  def set_mate_on_reverse(self, value):
    self.__set_flag(value, SAM_FMR)

  def set_read1(self, value):
    self.__set_flag(value, SAM_FR1)

  def set_read2(self, value):
    self.__set_flag(value, SAM_FR2)

  def set_secondary_align(self, value):
    self.__set_flag(value, SAM_FSC)

  def set_failed_qc(self, value):
    self.__set_flag(value, SAM_FQC)

  def set_duplicate(self, value):
    self.__set_flag(value, SAM_FDP)

  def __set_flag(self, new_value, flag_mask):
    if new_value:
      self.flag |= flag_mask
    else:
      self.flag &= ~flag_mask

  def remove_mate(self):
    """
    removes all info pertaining to this mapping's mate.
    """
    self.set_properly_paired(False)
    self.set_mate_mapped(True) # turns off the bit
    self.mpos = 0
    self.mtid = None
    self.m_ref_id = None
    self.isize = 0


class SimpleMapping(Mapping):
  """
  A mapping implementation with setters for attributes. Useful for testing.
  """
  def __init__(self):
    super(SimpleMapping, self).__init__()
    self.__name = ""
    self.__base_qualities = array.array('B')
    self.__cigar = []
    self.__tags = []
    self.__seq = ""

  def set_name(self, name):
    self.__name = name

  def set_base_qualities(self, bq):
    if bq is not None and not isinstance(bq, array.array):
      raise TypeError("Invalid type for base qualities (%s)" % str(type(bq)))
    self.__base_qualities = bq

  def set_cigar(self, cig):
    if cig is not None and not isinstance(cig, list):
      raise TypeError("Invalid type for cigar (%s)" % str(type(cig)))
    self.__cigar = cig

  def add_tag(self, tag):
    self.__tags.append(tag)

  def set_seq_5(self, s):
    self.__seq = s

  def get_name(self):
    return self.__name

  def get_base_qualities(self):
    return self.__base_qualities

  def get_cigar(self):
    return self.__cigar

  def each_tag(self):
    for t in self.__tags:
      yield t

  def get_seq_5(self):
    return self.__seq

  def get_seq_len(self):
    return len(self.__seq)


class SAMMapping(Mapping):
  """
  A mapping implementation for storing SAM data.

  A ``SAMMapping`` object is constructed from a list of SAM fields --
  see http://samtools.sourceforge.net
  """

  CIGAR_PATTERN = re.compile(r"(\d+)([MIDNSHP])")
  
  def __init__(self, sam_fields):
    super(SAMMapping, self).__init__()
    self.__name = sam_fields[0]
    self.flag = int(sam_fields[1])
    self.tid = sam_fields[2]
    self.pos = int(sam_fields[3]) - 1
    self.qual = int(sam_fields[4])
    self.__cigar = [(int(n), c) for (n, c) in
                    self.CIGAR_PATTERN.findall(sam_fields[5])]
    if sam_fields[6] == '*':  # is this BWA-specific?
      self.mtid = None
    else:
      self.mtid = sam_fields[6]
    self.mpos = int(sam_fields[7]) - 1
    self.isize = int(sam_fields[8])
    self.__seq = sam_fields[9]
    self.__ascii_base_qual = sam_fields[10]
    self.__tags = [tuple(t.split(":")) for t in sam_fields[11:]]

  def get_name(self):
    return self.__name

  def get_seq_5(self):
    return self.__seq

  def get_base_qualities(self):
    if not hasattr(self, '__base_qual'):
      self.__base_qual = array.array(
        'B', [ord(q) - 33 for q in self.__ascii_base_qual]
        )
    return self.__base_qual

  def get_cigar(self):
    return self.__cigar

  def each_tag(self):
    for t in self.__tags:
      yield t
