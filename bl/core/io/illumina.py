import csv, re

class GenomeStudioFinalReport(object):
  """

  FIXME

  .. code-block:: python

    r = GenomeStudioFinalReport(sample_id, block)
    r.sample_id

  """

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
  A simple Illumina Genome Studio final report reader.

  .. code-block:: python

   from bl.core.io.illumina import GenomeStudioFinalReportReader as GSReader
   reader = GSReader(open('report.txt'))

   print reader.header.keys()

   for b in reader.get_sample_iterator():
     print b.sample_id
     for k in b.snp_names():
        print b.snp[k]

  """


  def __init__(self, file_object):
    """
    FIXME
    """
    magic = file_object.readline()
    if not magic.startswith('[Header]'):
      raise ValueError('%s is not a Genome Studio Final Report'
                       % file_object.name)

    header = []
    l = file_object.readline()

    while not l.startswith('[Data]'):
      # FIXME this is ms-dos sanitation
      header.append(l.strip())
      l = file_object.readline()
    else:
      self.header = self.__process_header(header)
    csv.DictReader.__init__(self, file_object, delimiter='\t')

  def __process_header(self, records):
    # FIXME this is ms-dos sanitation
    header = dict(re.split('\t+', r) for r in records)
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


