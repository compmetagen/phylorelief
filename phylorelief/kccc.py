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


import numpy as np

def _expand(x, y):
    K = np.unique(np.concatenate((x, y)))
    X = np.zeros((x.shape[0], K.shape[0]), dtype=np.int)
    Y = np.zeros((y.shape[0], K.shape[0]), dtype=np.int)
    for i, k in enumerate(K):
        X[x==k, i] = 1
        Y[y==k, i] = 1
    return X, Y

def KCCC(x, y):
    """ K-category correlation coefficient.
    """

    EPS = np.finfo(np.float).eps
    k = x.shape[1]

    xn = x - np.mean(x, axis=0)
    yn = y - np.mean(y, axis=0)
    cov_xy = np.sum(xn * yn) / k
    cov_xx = np.sum(xn * xn) / k
    cov_yy = np.sum(yn * yn) / k

    cov_xxyy = cov_xx * cov_yy
    if cov_xxyy > EPS:
        rk = cov_xy / np.sqrt(cov_xx * cov_yy)
    else:
        rk = 0.0

    return rk

def KCCC_discrete(x, y):
    X, Y = _expand(x, y)
    return KCCC(X, Y)
