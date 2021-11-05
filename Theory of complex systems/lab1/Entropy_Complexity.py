import bounds
import numpy as np

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

def make_ordinal_structures(z_vectors):
    ordinal_structures = dict()
    for z_vector in z_vectors:
        new_arr = [z_vector, []]
        for i in range(len(z_vector)):
            new_arr[1].append(i)
        new_arr = np.asarray(new_arr).T
        ordinal_structure = str(new_arr[new_arr[:, 0].argsort()].T[1])
        
        #ordinal_vector = ""
        #for i in range(len(z_vector) - 1):
        #    if z_vector[i] <= z_vector[i+1]:
        #        ordinal_structure += "1"
        #    else:
        #        ordinal_structure += "0"
        if ordinal_structure in ordinal_structures.keys():
            ordinal_structures[ordinal_structure] += 1
        else:
            ordinal_structures[ordinal_structure] = 1
    print("N =", len(ordinal_structures.keys()))
    return ordinal_structures

def make_Ps(ordinal_structures, n, m):
    Ps = []
    for ordinal_structure in ordinal_structures.keys():
        P = ordinal_structures[ordinal_structure]/(n-m+1)
        Ps.append(P)
    return Ps


def Entropy(Ps):
    H = 0
    N = len(Ps)
    for i in range(N):
        P = Ps[i]
        H -= P * np.log(P)
    return H

def KL_divergence(P, Q):
    """ Compute KL divergence of two vectors, K(p || q)."""
    return sum(P[x] * np.log((P[x]) / (Q[x])) for x in range(len(P)) if (P[x] != 0.0) and (P[x] != 0) and (P[x] is not None))

def JSD(P, Q):
    """ Returns the Jensen-Shannon divergence. """
    JSD = 0.0
    weight = 0.5
    average = np.zeros(len(P)) #Average
    for x in range(len(P)):
        average[x] = weight * P[x] + (1 - weight) * Q[x]
        JSD = (weight * KL_divergence(np.array(P), average)) + ((1 - weight) * KL_divergence(np.array(Q), average))
    return 1-(JSD/((2 * np.log(2))**0.5))

def make_D(Ps, H_P):
    N = len(Ps)
    Pe = [1/N]*N
    #H_Pe = Entropy(Pe)
    #print("H_P = ", H_P)
    #print("H_Pe =", H_Pe)
    #D = (H_P / 2) - (H_Pe / 2)
    
    D = JSD(Ps, Pe)
    
    return(D)
    
def MPR_Complexity(H, Ps):
    N = len(Ps)
    Ps = np.asarray(Ps)
    alpha = 0.5
    p00 = 1./N
    pp0 = N
    pp1 = N - 1
    aaa = ( 1. - alpha ) / pp0
    bbb = alpha + aaa
    aux1= bbb * np.log( bbb )
    aux2= pp1 * aaa * np.log( aaa )
    aux3= ( 1. - alpha ) * np.log( pp0 )
    Q_0 = -1. / ( aux1 + aux2 + aux3 )
    
    Ps2 = alpha * Ps  + (1 - alpha) * p00
    S_p_pe = Entropy(Ps2)
    S_p = Entropy(Ps)
    S_pe = np.log(N)
    H_s = S_p/S_pe
    C = Q_0 * (S_p_pe - 0.5 * S_p - 0.5 * S_pe) * H_s

    #D = make_D(Ps, H)
    #print("D =", D)
    #C = Q_0 * H * D
    return Q_0, C
    
def solution(time_series, z_vector_size):
    print("making z-vectors")
    z_vectors = make_z_vectors(time_series, z_vector_size)
    print("making ordinal vectors")
    ordinal_vectors = make_ordinal_structures(z_vectors)
    #print(ordinal_vectors)
    print("calc Probabilities")
    Ps = make_Ps(ordinal_vectors, len(time_series), z_vector_size)
    print("calc Entropy")
    H = Entropy(Ps)
    print("calc Complexity")
    Q_0, C = MPR_Complexity(H, Ps)
    print("Q_0 =", Q_0)
    print("C =", C)
    N = len(Ps)
    b = bounds.bounds(N, Q_0 * np.log(N))
    H /= np.log(N)
    return H, C, b