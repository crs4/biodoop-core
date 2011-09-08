## .nib format 	
  	

## The .nib format pre-dates the .2bit format and is less compact. It describes a DNA sequence by packing two bases into each byte. Each .nib file contains only a single sequence. The file begins with a 32-bit signature that is 0x6BE93D3A in the architecture of the machine that created the file (or possibly a byte-swapped version of the same number on another machine). This is followed by a 32-bit number in the same format that describes the number of bases in the file. Next, the bases themselves are listed, packed two bases to the byte. The first base is packed in the high-order 4 bits (nibble); the second base is packed in the low-order four bits:

##     byte = (base1<<4) + base2 

## The numerical representations for the bases are:

##     * 0 - T
##     * 1 - C
##     * 2 - A
##     * 3 - G
##     * 4 - N (unknown) 

## The most significant bit in a nibble is set if the base is masked.

## http://genome.ucsc.edu/FAQ/FAQformat.html#format8

import struct
from ctypes import create_string_buffer


SIGNATURE = 0x6BE93D3A
BYTE_SWAPPED_SIGNATURE = 0x3A3DE96B
ENCODING = {"T": 0, "C": 1, "A": 2, "G": 3, "N": 4,
            "t": 0, "c": 1, "a": 2, "g": 3, "n": 4}


def seq2nib(seq):
  buf_len = 8 + len(seq)/2 + len(seq)%2
  nib = create_string_buffer(buf_len)
  struct.pack_into('@i', nib, 0, SIGNATURE)
  struct.pack_into('@i', nib, 4, len(seq))
  for i in xrange(0, len(seq), 2):
    offset = 8 + i/2
    value = (ENCODING[seq[i]] << 4)
    if seq[i].islower():
      value |= 128
    try:
      value += ENCODING[seq[i+1]]
      if seq[i+1].islower():
        value |= 8
    except IndexError:
      pass
    try:
      struct.pack_into('@B', nib, offset, value)
    except struct.error:
      print i, seq[i-10:i+10]
      raise
  return nib.raw


def nib2seq(nib):
  sig = struct.unpack_from('@i', nib, 0)
  if sig != SIGNATURE and sig != BYTE_SWAPPED_SIGNATURE:
    raise ValueError("bad signature: 0x%x" % sig)
  seq_len = struct.unpack_from('@i', nib, 4)
  
  

if __name__ == "__main__":
  chrom = "22"
  from bl.core.seq.io.fasta import RawFastaReader
  with open("chr%s.fa" % chrom) as f:
    reader = RawFastaReader(f)
    records = [r for r in reader]
  assert len(records) == 1
  header, seq = records[0]
  nib = seq2nib(seq)
  ## with open("try_chrM.nib", 'w') as outf:
  ##   outf.write(nib)
  with open("chr%s.nib" % chrom) as f:
    exp_nib = f.read()
  print "nib == exp_nib:", (nib == exp_nib)
