Example
=======

This very simple example is located in the ``example/`` directory. The directory contains three files. A rooted tree in newick format:

.. literalinclude:: ../example/tree.tre

.. image:: images/input_tree_example.png

An OTU table in tab-delimited format:

.. literalinclude:: ../example/otu_table.txt

A sample table with sample information:

.. literalinclude:: ../example/sample_data.txt

To to run example, open a terminal, go into the example (examples/) folder and run::

    $ phylorelief otu_table.txt tree.tre sample_data.txt Status -k 1

Two files, ``out_phylorelief.txt`` and ``tree_phylorelief.tre`` will be generated.
``out_phylorelief.txt`` contains the clade/OTU ranking:

.. literalinclude:: ../example/out_phylorelief.txt

``tree_phylorelief.tre`` is the nexus annotated file:

.. literalinclude:: ../example/tree_phylorelief.tre

Now you can navigate the annotated tree with an external progam such as FigTree:

.. image:: images/figtree_example.png
