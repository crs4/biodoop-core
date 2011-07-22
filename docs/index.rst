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

Currently, Biodoop's core only contains a few modules for handling
FASTA streams on Hadoop and wrappers for BLAST.

Installation:

#. install `Pydoop <http://pydoop.sourceforge.net>`_

#. unpack the biodoop core tarball, move to the distribution directory
   and run::

     python setup.py install

   for a system-wide installation, or::

     python setup.py install --user

   for a local installation
