import numpy as np
from numpy import linalg as LA
import sys

from scipy.spatial import cKDTree as KDTree
from scipy.spatial import distance

def make_z_vectors(time_series, m):
    '''
    Input:
        x - 1d array of size n
    Output:
        z-vectors - 2d array of size n x (n-m+1)
    Description:
        Calculates z-vectors
    '''
    z_vectors = []
    for i in range(len(time_series)-m+1):
        z_vectors.append(time_series[i:i+m])
    return np.asarray(z_vectors)


#def closest_neighbour(z_vectors, i):
    '''
    Input:
        z_vectors - 2d array of size n x (n-m+1)
        i - index of z-vector that needs closest neighbour to be found
    Output:
        min_index - index of min neighbour
        z-vector - 1d array of size n-m+1
    Description:
        Returns closest neighbour
    '''
    '''
    target_z_vector = z_vectors[i]
    start_id = 0
    if i == 0: start_id = 1
    neighbour = z_vectors[start_id]
    min_norm = LA.norm(neighbour - target_z_vector)
    min_index = start_id
    for index, z_vector in enumerate(z_vectors):
        if index == i:
            continue
        norm = LA.norm(z_vector - target_z_vector)
        if norm < min_norm:
            min_norm = norm
            neighbour = z_vector
            min_index = index
    return min_index, neighbour, min_norm
    '''

#def find_neighbours(z_vectors, num_neighbours=1):
    '''
    Input:
        z_vectors - 2d array of size n x (n-m+1)
        num_neighbours - number of closest neighbours to be found
    Output:
        neighbours_ids - 1d array of size n
        norms - 1d array of size n
    Description:
        Returns array of indexes of closest neighbours and array of norms||z_j - z_j*||
    '''
    '''
    if num_neighbours > 1:
        return -1 #not implemented
    print("finding neighbours")
    neighbours = []
    neighbours_ids = []
    norms = []
    for index, z_vector in enumerate(z_vectors):
        neighbour_id, neighbour, norm = closest_neighbour(z_vectors, index)
        neighbours_ids.append(neighbour_id)
        neighbours.append(neighbour)
        norms.append(norm)
        sys.stdout.write('\r' + str(float(index + 1)/len(z_vectors) // 0.01) + '%')
    print()
    return np.asarray(neighbours_ids), np.asarray(norms)
    '''

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

def make_lapunov_estimation(z_vectors, k=1, num_neighbours=1):
    '''
    Input:
        z_vectors - 2d array of size n x (n-m+1)
        k - parameter
    Output:
        lapunov - float
    Description:
        Calculates estimation of lapunov parameter
    '''
    neighbours_ids, norms = find_neighbours(z_vectors, num_neighbours=num_neighbours)
    estimations = []
    print("making lapunov estimation")
    for i in range(len(z_vectors)):
        lapunov_j = (1/k) * np.log((LA.norm(z_vectors[(i + k) % len(z_vectors)] - z_vectors[(neighbours_ids[i] + k) % len(z_vectors)]))/norms[i])
        estimations.append(lapunov_j)
        sys.stdout.write('\r' + str(float(i+1)/len(z_vectors) // 0.01) + '%')
    print()
    return np.mean(estimations)

def rosenstein_method(time_series, z_vector_size, num_neighbours=1):
    z_vectors = make_z_vectors(time_series, z_vector_size)
    lapunov = make_lapunov_estimation(z_vectors, num_neighbours=num_neighbours)
    return lapunov