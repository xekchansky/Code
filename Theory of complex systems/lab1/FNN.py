import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

from scipy.spatial import cKDTree as KDTree
import sys
from scipy.spatial import distance

import rosenstein

def dist_func(x, y, metric='chebyshev'):
    '''
    Compute the distance between all sequential pairs of points.
    Computes the distance between all sequential pairs of points from
    two arrays using scipy.spatial.distance.
    Input:
        x : ndarray
            Input array.
        y : ndarray
            Input array.
        metric : string, optional (default = 'chebyshev')
            Metric to use while computing distances.
    Output:
        d : ndarray
            Array containing distances.
    '''
    
    func = getattr(distance, metric)
    return np.asarray([func(i, j) for i, j in zip(x, y)])

def find_neighbours(z_vectors, num_neighbours=1):
    '''
    Find indexes of nearest neighbours and distances to them
    Input:
        z_vectors : ndarray
            z_vectors of time series.
        num_neighbours : int
            number of neighbours to find.
    Output:
        neighbours_ids : ndarray
            Ids of nearest neighbours.
        dists : ndarray
            distances to nearest neighbours.
    '''
    tree = KDTree(z_vectors)
    n = len(z_vectors)

    num_neighbours = max(1, num_neighbours)

    if num_neighbours >= n:
        raise ValueError('num_neighbours is bigger than array length.')

    dists = np.empty(n)
    neighbours_ids = np.empty(n, dtype=int)

    for i, z_vector in enumerate(z_vectors):
        for k in range(2, num_neighbours + 2):
            dist, index = tree.query(z_vector, k=k, p=2)
            valid = (np.abs(index - i) > 0) & (dist > 0)

            if np.count_nonzero(valid):
                dists[i] = dist[valid][0]
                neighbours_ids[i] = index[valid][0]
                break

            if k == (num_neighbours + 1):
                raise Exception('Could not find any near neighbor with a '
                                'nonzero distance.  Try increasing the '
                                'value of num_neighbours.')

    return np.squeeze(neighbours_ids), np.squeeze(dists)

def count_FNN(time_series, m, num_neighbours=1, A=10, B=2.0):
    '''
    Calculate False nearest neighbours metrics with dimension m
    Input:
        time_series : ndarray
            time series.
        m : int
            z vectors dimension.
        num_neighbours : int
            number of neighbours to find.
        A, B : float
            algorithm parameters
    Output:
        f1,f2,f3,f4,f5 : float
            metrics of number of false nearest neighbours.
    '''
    sys.stdout.write('\r' + str(m))
    y1 = rosenstein.make_z_vectors(time_series[:-1], m)
    y2 = rosenstein.make_z_vectors(time_series, m + 1)
    #y1 = z_vectors[:-1]
    #y2 = np.asarray([np.append(z_vectors[i], z_vectors[i+1][-1]) for i in range(len(z_vectors)-1)])

    # Find near neighbors in dimension d.
    index1, dist = find_neighbours(y1, num_neighbours=num_neighbours)
    index2, dist = find_neighbours(y2, num_neighbours=num_neighbours)

    # Find all potential false neighbors using Kennel et al.'s tests.
    f1 = np.abs(y2[:, -1] - y2[index1, -1]) / dist > A
    f2 = dist_func(y2, y2[index1], metric='chebyshev') / np.std(time_series) > B
    f3 = f1 | f2
    
    # Find false nearest neighbours using pure method from lecture
    f4 = np.count_nonzero(index1 - index2)
    
    # normalized
    f5 = f4 / (len(time_series)-m+1)

    return np.mean(f1), np.mean(f2), np.mean(f3), f4, f5

def FNN(time_series, ms, num_neighbours=1, A=1, B=1):
    '''
    Calculate False nearest neighbours metrics for every dimension m
    Input:
        time_series : ndarray
            time series.
        ms : list
            z vectors dimensions.
        num_neighbours : int
            number of neighbours to find.
        A, B : float
            algorithm parameters
    Output:
       [[. ,. ,. ,. ,. ]
        [f1,f2,f3,f4,f5]
        [. ,. ,. ,. ,. ]] : nparray
            metrics of number of false nearest neighbours for every dimension m.
    '''
    return np.asarray([count_FNN(time_series, m, num_neighbours, A, B) for m in ms])