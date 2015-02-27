.. PhyloRelief documentation master file, created by
   sphinx-quickstart on Mon Dec 16 10:15:02 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PhyloRelief's documentation!
=======================================

PhyloRelief implements an algorithm that introduces the Relief
strategy of feature weighting in a phylogenetic context to identify
those OTUs or groups of OTUs that are correlated for the
differentiation between classes of samples (i.e. healthy vs. disease,
lean vs. obese etc.) in a metagenomic dataset. By integrating the
phylogenetic relationships amongst taxa into the framework of
statistical learning, the method is able to unambiguously group the
taxa into lineages without relying on a precompiled taxonomy, and
accomplishes a ranking of the lineages according to their contribution
to the sample differentiation.

.. toctree::
   :maxdepth: 2
   
   install
   usage
   example
   details


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

