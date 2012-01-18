import csv, re


class GenomeStudioFinalReport(object):

  def __init__(self, sample_id, block):
    self.sample_id = sample_id
    snp = {}
    for l in block:
      snp_name = l['SNP Name']
      [l.pop(k) for k in ['Sample ID', 'Sample Name']]
      snp[snp_name] = l
    self.snp = snp

  def snp_names(self):
    return self.snp.keys()


class GenomeStudioFinalReportReader(csv.DictReader):
  """
  A simple Illumina Genome Studio Final Report reader.

  .. code-block:: python

   from bl.core.io.illumina import GenomeStudioFinalReportReader as GSReader
   reader = GSReader(open('report.txt'))
   print reader.header.keys()
   for b in reader.get_sample_iterator():
     print b.sample_id
     for k in b.snp_names():
        print b.snp[k]
  """
  def __init__(self, f):
    magic = f.readline()
    if not magic.startswith('[Header]'):
      raise ValueError('%s is not a Genome Studio Final Report' % f.name)
    header = []
    l = f.readline()
    while not l.startswith('[Data]'):
      header.append(l.strip())  # ms-dos sanitation
      l = f.readline()
    else:
      self.header = self.__process_header(header)
    csv.DictReader.__init__(self, f, delimiter='\t')

  def __process_header(self, records):
    header = dict(re.split('\t+', r) for r in records)  # ms-dos sanitation
    return header

  def get_sample_iterator(self):
    sample_id_key = 'Sample ID'

    class sample_iterator(object):

      def __init__(self, reader):
        self.reader = reader
        self.sample_id = None
        self.last_line = self.reader.next()

      def __iter__(self):
        return self

      def next(self):
        if not self.last_line:
          raise StopIteration
        block = []
        r = self.last_line
        try:
          sample_id = r[sample_id_key]
          while r[sample_id_key] == sample_id:
            block.append(r)
            r = self.reader.next()
          else:
            self.last_line = r
            return GenomeStudioFinalReport(sample_id, block)
        except StopIteration:
          if len(block) > 0:
            self.last_line = None
            return GenomeStudioFinalReport(sample_id, block)

    return sample_iterator(self)


class IllSNPReader(csv.DictReader):
  """
  Reads Illumina SNP annotation files.
  """
  def __init__(self, f):
    def ill_filter(f):
      open = False
      for line in f:
        if line.startswith('[Assay]'):
          open = True
          continue
        elif line.startswith('[Controls]'):
          open = False
        if open:
          yield line
    csv.DictReader.__init__(self, ill_filter(f))
