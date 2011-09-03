import csv
import cStringIO
from datetime import datetime

class SDSReader(csv.DictReader):
  """
  A simple ABI SDS 2.3 AD (txt) reader.

  .. code-block:: python

    >>> sds = SDSReader(open('foo.txt'))
    >>> for m,v in sds.header['markers_info'].iteritems():
          print 'marker %s: %s' % (m, v)
    >>> for r in sds:
          if r['HMD'] or r['FOS'] or r['LME'] or r['EW'] or r['BPR']:
             print r
          else:
             print 'Well %s:  %s' % (r['Well'], r['Call'])


  FIXME
  As described in "Applied Biosystems 7900HT Fast Real-Time PCR System
  Allelic Discrimination Getting Started Guide (PN 4364015D)", this is
  the list of fields that are present in a record

    * Well position

    * Flags: HMD (the well has missing data), FOS (fluorescence is
      off-scale), LME (large mean squared error), EW (the well is
      empty), BPR (bad passive reference)

    * Sample

    * Marker

    * Task: Unknown, NTC

    * Call: Allele Y, Allele X, Both, NTC, Undetermined

    * Quality Value

    * Call Type

    * Allele X Rn

    * Allele Y Rn

    * Passive Reference Rn

   where Rn stands for The ratio of the fluorescence intensity of the
   reporter dye signal to the fluorescence intensity of the passive
   reference dye signal.
  """
  def __init__(self, file_object, swap_sample_well_columns=False):
    """
    FIXME
    """
    magic = file_object.readline()
    if not magic.startswith('SDS 2.3\tAD Results\t1.0'):
      raise ValueError('%s is not an SDS 2.3 AD file' % file_object.name)

    header = []
    mark = file_object.tell()
    l = file_object.readline()
    self.swap_sample_well_columns = swap_sample_well_columns

    while not l.startswith('Well\tSample Name\tMarker Name'):
      mark = file_object.tell()
      header.append(l)
      l = file_object.readline()
    else:
      self.header = self.__process_header(''.join(header))
      file_object.seek(mark)
    csv.DictReader.__init__(self, file_object, delimiter='\t')

  @property
  def datetime(self):
    date, time = self.header['params']['Run DateTime'].split(' ')
    day, month, year = map(int, date.split('/'))
    hour, minute, sec = map(int, time.split('.'))
    return datetime(year + 2000, month, day, hour, minute, sec)


  def __process_header(self, header_txt):
    # FIXME this is ms-dos sanitation
    header_txt = header_txt.replace('\r','')
    header = {}
    p_info, tail = header_txt.split('Sample Information\n')
    s_info, m_info = tail.split('Marker Setting Information\n')
    params = {}
    for l in p_info.split('\n'):
      if not l:
        continue
      key, value = l.split('\t')
      params[key] = value
    header['params'] = params

    #FIXME no idea of what this could look like
    header['sample_information'] = s_info
    f = csv.DictReader(cStringIO.StringIO(m_info), delimiter='\t')
    markers_info = {}
    for r in f:
      name = r['Marker Name'].strip()
      del r['Marker Name']
      for k in ['NOC', 'HW', 'SNS', 'DCN']:
        r[k] = r[k] == 'True'
      markers_info[name] = r
    header['markers_info'] = markers_info
    return header

  def next(self):
    r = csv.DictReader.next(self)
    # filter out the 'per SNP header'
    if r['Well'] == 'Well':
      return self.next()
    if self.swap_sample_well_columns:
      r['Well'], r['Sample Name'] = r['Sample Name'].strip(), r['Well'].strip()
    if '' in r:
      del r['']
    for k in ['Quality Value', 'Allele X Rn', 'Allele Y Rn',
              'Passive Ref']:
      r[k] = float(r[k])
    return r
