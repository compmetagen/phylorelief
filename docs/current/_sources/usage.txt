Usage
=====

PhyloRelief is distributed as a command line application.
You can run ``phylorelief --help`` in order to show a summary of options:

.. command-output:: phylorelief --help

``phylorelief`` application takes four required inputs, three files and 
a target name:

 ``tree``
     A (rooted) tree in ``newick`` format.

     .. note::

         Note that all the leaf nodes should have univocal names.

 ``otu_table``
     An OTU table (containing the number of sequences observed in each OTU 
     for each sample) in **tab-delimited** format, OTU (rows) x sample 
     (columns) orientation:
     
     +------+-------------+-------------+-------------+-----+
     | OTU  | SampleName1 | SampleName2 | SampleName3 | ... |
     +------+-------------+-------------+-------------+-----+
     | OTU1 | 22          | 3           | 6           | ... |
     +------+-------------+-------------+-------------+-----+
     | OTU2 | 10          | 45          | 340         | ... |
     +------+-------------+-------------+-------------+-----+
     | ...  | ...         | ...         | ...         | ... |
     +------+-------------+-------------+-------------+-----+
     
     OTU names must correspond to the leaf names in the tree. 

     .. note::

         A rarefied OTU table should be used in order to remove sample 
    	 heterogeneity.


 ``sample_table``
     A **tab-delimited** file containing sample information and metadata (e.g.
     health status):
     
     +-------------+---------+---------+-----+
     | Sample      | Status  | Treated | ... |
     +-------------+---------+---------+-----+
     | SampleName1 | Case    | Yes     | ... |
     +-------------+---------+---------+-----+
     | SampleName2 | Control | No      | ... |
     +-------------+---------+---------+-----+
     | SampleName3 | Case    | No      | ... |
     +-------------+---------+---------+-----+
     | ...         | ...     | ...     | ... |
     +-------------+---------+---------+-----+
      
     Sample names must correspond to the sample names in the OTU table.
 
 ``target``
     A ``sample_table`` column to be used as class label (e.g. 'Status' or 
     'Treated' in the example above)

The application outputs two files, a clade ranking file and a annotated tree
in nexus format:

 Clade ranking file    
     
     A clade ranking file is a tab-delimited file with five
     columns. The clades are ranked in decreasing order according the
     weight assigned by the algorithm. The first column contains the
     PhyloRelief weights, the 2nd, 3rd and 4th columns contain the
     statistics, the p-values and the FDR corrected p-values of the
     Kruskal-Wallis test and the last column contains the OTU names
     (comma separated) forming the corresponding clade:

     +--------------------+----------+--------+---------+-----------------+
     | phylorelief_weight | kw_stats | kw_p   | kw_padj | OTUs            |
     +--------------------+----------+--------+---------+-----------------+
     | 0.8633             | 0.8597   | 0.0225 | 0.0589  | OTU34,OTU2,OTU8 |
     +--------------------+----------+--------+---------+-----------------+
     | 0.6402             | 6.2530   | 0.0012 | 0.0242  | OTU12,OTU11     |
     +--------------------+----------+--------+---------+-----------------+
     | ...                | ...      | ...    | ...     | ...             |
     +--------------------+----------+--------+---------+-----------------+

 Annotated tree file
     An annotated tree (BEAST/FigTree style) in nexus format. 
     In this file **each node** in the tree is annotated with two metadata:
     ``phylorelief_weight`` and ``phylorelief_rank``. ``phylorelief_weight``
     contains the weights assigned by phylorelief to the clade starting from
     the node and ``phylorelief_rank`` contains the clade ranking position.
