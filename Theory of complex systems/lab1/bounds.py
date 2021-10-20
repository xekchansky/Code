import matplotlib.pyplot as plt
import numpy as np
from numpy import ma

def xlog(x):
    '''
    Input:
        x - 1d array
    Output:
        xlogx - 1d array
    Description:
        Calculates xlogx with respect to continuity
    '''
    return x * ma.filled(ma.log(x), 0)

def bounds(n, Q_0):
    '''
    Input:
        n - size of the distribution
        Q_0 -normalization constant
    Output:
        lower_bound, upper_bound - numpy arrays of size (2, n) first row is entropy, second - complexity
    Definition:
        Constructs lower and upper bounds for distribution of size n on CH plane
    '''

    dots_indices = np.arange(1, n + 1, 1)
    normed_indices = dots_indices / n

    H_max = np.log(dots_indices) / np.log(n)
    H_min = -xlog(dots_indices / n) / np.log(n) - \
             xlog((1 - dots_indices / n) / (n - 1))  * (n - 1) / np.log(n) 

    Q_max = Q_0 * (np.log(2) - 0.5 * (xlog(1 + normed_indices) - xlog(normed_indices))) / np.log(n)
    C_max = Q_max * H_max

    Q_min = Q_0 * (np.log(2) + 0.5 * (xlog(normed_indices) + xlog(1 - normed_indices) - \
                                      xlog(normed_indices + 1 / n) - xlog(2 - normed_indices - 1 / n) +
                                      xlog(1 / n) + xlog(1 - 1 / n))) / np.log(n)
    C_min = Q_min * H_min
    
    return np.array([H_min, C_min]), np.array([H_max, C_max])
