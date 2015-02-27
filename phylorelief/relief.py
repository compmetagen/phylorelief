## This code is written by Davide Albanese, <davide.albanese@fmach.it> 
## <davide.albanese@gmail.com>
## Copyright (C) 2013 Fondazione Edmund Mach
## Copyright (C) 2013 Davide Albanese

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


from __future__ import division
import sys
import numpy as np
from numpy.random import RandomState
import pandas as pd
import dendropy
from scipy.stats import kruskal
from statsmodels.sandbox.stats.multicomp import multipletests
from uf import convert, unifrac_matrix, unifrac_all_nodes


def prelief(otu_table, tree, target, k=3, m=None, equal_priors=False,
            seed=0, variant="unweighted", alpha=0.5, verbose=True):
    
    def knn(distance, target, sample, c, k):
        distance_sample = distance[sample]
        distance_c = distance_sample[distance_sample.index != sample]
        distance_c = distance_c[target == c]
        distance_c.sort()
        return distance_c[:k].index

    prng = RandomState(seed)

    samples = list(otu_table.columns)
    classes = list(target.unique())
    n_samples = otu_table.shape[1]
    n_classes = len(classes)

    node_table, edge_length = convert(otu_table, tree)
    if verbose:
        sys.stdout.write('Computing distance matrix...\n')
        sys.stdout.flush()
    distance = unifrac_matrix(node_table, edge_length, tree, variant, alpha)

    # prior probabilities
    priors = {}
    if equal_priors:
        for c in classes:
            priors[c] = (1 / n_classes)
    else:
        for c in classes:
            priors[c] = (target == c).sum() / n_samples

    # m randomly selected samples
    selected_list = samples[:]
    prng.shuffle(selected_list)
    if m is not None:
        m = np.min([n_samples, m])
        selected_list = selected_list[:m]
    m = len(selected_list)

    # Relief-F
    weight = pd.Series(index=[node.oid for node in tree.preorder_node_iter()])
    weight = weight.fillna(0.0)
    for i, selected in enumerate(selected_list):
        if verbose:
            sys.stdout.write('\r')
            sys.stdout.write("Computing weights... %d%%" % int(((i+1)/m)*100))
            sys.stdout.flush()
        
        neighbors = knn(distance, target, selected, target[selected], k)

        for neighbor in neighbors:
            d = unifrac_all_nodes(selected, neighbor, node_table,
                                  edge_length, tree, variant, alpha)
            weight -= d / (m * k)

        classes_m = [c for c in classes if c != target[selected]]
        for c in classes_m:
            a = priors[c] / (1 - priors[target[selected]])
            neighbors = knn(distance, target, selected, c, k)
            for neighbor in neighbors:
                d = unifrac_all_nodes(selected, neighbor, node_table,
                                      edge_length, tree, variant, alpha)
                weight += (a * d) / (m * k)

    if verbose:
        sys.stdout.write('\n')
        sys.stdout.flush()

    sample_classes = []
    for c in classes:
         sample_classes.append(target[target == c].index.tolist())
        
    # OTU ranking
    rank = []
    weight_copy = pd.Series(weight, copy=True)
    while weight_copy.shape[0] > 0:
        node_oid = weight_copy.idxmax()
        node = tree.find_node(lambda node: node.oid == node_oid)
        leaf_taxa_labels = [leaf_node.taxon.label for leaf_node in \
                            node.leaf_nodes() if leaf_node.taxon]
        
        # remove internal nodes from the weight list
        internal_node_oids = [internal_node.oid for internal_node \
                              in node.postorder_iter()]
        weight_copy = weight_copy.reindex(weight_copy.index - internal_node_oids)

        # remove parent nodes from the weight list
        parent_node_oids = []
        parent_node = node.parent_node
        while parent_node:
            parent_node_oids.append(parent_node.oid)
            parent_node = parent_node.parent_node
        weight_copy = weight_copy.reindex(weight_copy.index - parent_node_oids)

        groups = []
        for sc in sample_classes:
            groups.append(node_table.loc[node_oid, sc].tolist())

        try:
            kw_stat, kw_p = kruskal(*groups)
        except ValueError:
            kw_stat, kw_p = np.nan, np.nan 
            
        rank.append((node_oid, leaf_taxa_labels, kw_stat, kw_p))
        
    _, kw_padj, _, _ = multipletests([elem[3] for elem in rank], method="fdr_bh")
    for i in range(len(rank)):
        rank[i] += (kw_padj[i],)
    
    return weight, rank
