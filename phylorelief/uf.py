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
import itertools
import dendropy
import numpy as np
import pandas as pd


def convert(otu_table, tree):

    node_oid = [node.oid for node in tree.postorder_node_iter()]
    node_table = pd.DataFrame(index=node_oid, columns=otu_table.columns,
                              dtype=np.int)
    edge_length = pd.Series(index=node_oid, dtype=np.float)
    
    for node in tree.postorder_node_iter():
        if node.is_leaf():
            node_table.loc[node.oid] = otu_table.loc[node.taxon.label]
        else:
            node_table.loc[node.oid] = 0
            for child_node in node.child_nodes():
                node_table.loc[node.oid] += node_table.loc[child_node.oid]

        if node.edge_length:
            edge_length[node.oid] = node.edge_length
        else:
            edge_length[node.oid] = 0.0
            
    return node_table, edge_length


def unifrac_core(A, B, node_table, edge_length, tree, variant="unweighted",
                 alpha=0.5):

    def unweighted(Ai, Bi, bi, At, Bt):
        Ni = bi * (Ai.astype(np.bool) - Bi.astype(np.bool)).abs()
        return Ni, bi

    def weighted(Ai, Bi, bi, At, Bt):
        pa = (Ai / At).fillna(0.0)
        pb = (Bi / Bt).fillna(0.0)
        Ni = bi * (pa - pb).abs()
        Di = bi * (pa + pb)
        return Ni, Di

    def generalized(Ai, Bi, bi, At, Bt):
        pa = (Ai / At).fillna(0.0)
        pb = (Bi / Bt).fillna(0.0)
        s = pa + pb
        Di = bi * s**alpha
        snz = s > 0.0
        Ni = pd.Series(index=Di.index).fillna(0.0)
        Ni[snz] = (Di[snz] * ((pa-pb).abs()[snz] / s[snz]))
        return Ni, Di

    if variant == "unweighted":
        fun = unweighted
    elif variant == "weighted":
        fun = weighted
    elif variant == "generalized":
        fun = generalized
    else:
        raise ValueError("parameter 'variant' %s is not valid" % variant)

    Ai, Bi = node_table[A], node_table[B]
    bi = edge_length
    At, Bt = Ai.sum(), Bi.sum()
    Ni, Di = fun(Ai, Bi, bi, At, Bt)

    return Ni, Di


def unifrac_all_nodes(A, B, node_table, edge_length, tree, variant="unweighted",
                      alpha=0.5):

    Ni, Di = unifrac_core(A, B, node_table, edge_length, tree, variant, alpha)

    Nt = pd.Series(index=node_table.index, dtype=np.float).fillna(0.0)
    Dt = pd.Series(index=node_table.index, dtype=np.float).fillna(0.0)
    for node in tree.postorder_node_iter():
        if node.is_leaf():
            Nt[node.oid] = Ni[node.oid]
            Dt[node.oid] = Di[node.oid]
        else:
            Nt[node.oid] = Ni[node.oid]
            Dt[node.oid] = Di[node.oid]
            for child_node in node.child_nodes():
                Nt[node.oid] += Nt[child_node.oid]
                Dt[node.oid] += Dt[child_node.oid]
    return (Nt / Dt).fillna(0.0)

    
def unifrac(A, B, node_table, edge_length, tree, variant="unweighted",
            alpha=0.5):
    Ni, Di = unifrac_core(A, B, node_table, edge_length, tree, variant, alpha)
    Nt, Dt = Ni.sum(), Di.sum()
    if Dt != 0:
        return Nt / Dt
    else:
        return 0.0

    
def unifrac_matrix(node_table, edge_length, tree, variant="unweighted",
                   alpha=0.5):
   
    pairs = list(itertools.combinations(node_table.columns, 2))
    distance = pd.DataFrame(index=node_table.columns, columns=node_table.columns)
    distance = distance.fillna(0.0)
    for i, (A, B) in enumerate(pairs):
        d = unifrac(A, B, node_table, edge_length, tree, variant, alpha)
        distance.loc[A, B] = d
        distance.loc[B, A] = d
    
    return distance
