.. _index:

Biodoop
=======

Biodoop is a suite of tools for computational biology that focuses on
the efficient, distributed implementation of the most computationally
demanding and/or data-intensive tasks. It consists of a core
component, which includes a set of general-purpose modules, plus a
number of application-specific components.

Current applications focus on sequence alignment and manipulation of
alignment records. Applications generally run on the `Pydoop
<http://pydoop.sourceforge.net>`_ API for `Hadoop
<http://hadoop.apache.org>`_ and are built to scale well in both the
number of computing nodes available and the amount of data to process,
making them particularly well suited for processing large data sets.


Core
----

Currently, Biodoop's core contains a few modules for handling FASTA
streams, wrappers for BLAST, I/O modules for some bio formats, a
module for converting sequences to the `nib format
<http://genome.ucsc.edu/FAQ/FAQformat.html#format8>`_ and protobuf
serializers for several objects.

Release Notes
^^^^^^^^^^^^^
.. include:: ../CHANGES

Installation
^^^^^^^^^^^^

#. install prerequisites:

  * `NumPy <http://numpy.scipy.org>`_

  * `SciPy <http://www.scipy.org/scipylib/index.html>`

  * `Protocol Buffers <http://code.google.com/p/protobuf>`_

  * `Pydoop <http://pydoop.sourceforge.net>`_

#. get biodoop-core from the `download page <https://sourceforge.net/projects/biodoop/files/>`_

#. unpack the biodoop-core tarball

#. build the protobuf code in ``bl/core/messages`` and ``bl/core/gt/messages``

#. move to the distribution's root directory and run::

     python setup.py install

   for a system-wide installation, or::

     python setup.py install --user

   for a local installation


BLAST
-----

The BLAST package provides a wrapper-based MapReduce implementation of
BLAST for Hadoop. See the `Biodoop-BLAST
<http://biodoop.sourceforge.net/blast>`_ documentation for details.
