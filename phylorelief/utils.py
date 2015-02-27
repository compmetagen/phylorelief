## This code is written by Davide Albanese, <davide.albanese@fmach.it>
## <davide.albanese@gmail.com>
## Copyright (C) 2014 Fondazione Edmund Mach
## Copyright (C) 2014 Davide Albanese

## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

import csv

import numpy as np
import scipy as sp
import pandas as pd
import dendropy
    

def import_otutable(filename):
    """ Returns a pandas DataFrame.
    """
    handler = open(filename, 'rU')
    reader = csv.reader(handler, delimiter='\t')
    columns = reader.next()[1:]
    index, data = [], []
    for row in reader:
        index.append(row[0])
        data.append(row[1:])
    otutable = pd.DataFrame(data=data, index=index, columns=columns,
                            dtype=np.float)
    return otutable

def import_tree(filename):
    """Returns a dendropy Tree.
    """
    tree = dendropy.Tree.get_from_path(filename, schema='newick',
                                       preserve_underscores=True,
                                       as_rooted=False)
    return tree

def import_sampledata(filename):
    """Returns a pandas DataFrame.
    """
    handler = open(filename, 'rU')
    reader = csv.reader(handler, delimiter='\t')
    columns = reader.next()[1:]
    index, data = [], []
    for row in reader:
        index.append(row[0])
        data.append(row[1:])
    sampledata = pd.DataFrame(data=data, index=index, columns=columns)
    return sampledata
    
def import_data(otutable_filename, tree_filename, sampledata_filename):
    otutable = import_otutable(otutable_filename)
    tree = import_tree(tree_filename)
    sampledata = import_sampledata(sampledata_filename)

    # common samples between sampledata and and otutable
    common_samples = list(set(otutable.columns) & set(sampledata.index))
    otutable = otutable.loc[:, common_samples]
    sampledata = sampledata.loc[common_samples]
    
    # align otutable and sampledata
    otutable = otutable.loc[:, sampledata.index]

    # prune the OTU table
    otutable = otutable.loc[otutable.sum(axis=1) > 0]
    
    # common otus between tree and otutable
    otutable_otus = set(otutable.index)
    tree_otus = set([node.taxon.label for node in tree.leaf_iter()])
    common_otus = list(tree_otus & otutable_otus)
    tree.retain_taxa_with_labels(common_otus)
    otutable = otutable.loc[common_otus]

    # tree rooting
    tree.reroot_at_midpoint()

    return otutable, tree, sampledata
