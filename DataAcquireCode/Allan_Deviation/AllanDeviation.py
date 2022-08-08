"""
@author: Yongxu Duan
e-mail: duanyongxu1994@gmail.com
"""
import numpy as np
from numpy import matlib


def allan(omega, fs, pts):
    """
    Inputs:
           omega:   set of measurements (number of row is number of measurements)
           fs:      frequency of measurements
           pts:     numbers of points to plot Allan deviation
    Outputs:
           T:       time spans of allan variance points
           sigma:   Allan standard deviation
    """
    print('allan() is called...')
    [N, M] = np.shape(omega)                            # figure out how big the output data set is
    n = 2 ** np.arange(0, np.floor(np.log2(N / 2))+1)   # determine the largest bin size
    maxN = n[-1]
    endLogInc = np.log10(maxN)
    m = np.unique(np.ceil(np.logspace(0, endLogInc, pts))).T    # create log spaced vector average factor
    t0 = 1/fs    # sample interval
    T = m*t0     # length of time for each cluster
    theta = np.cumsum(omega, axis=0)/fs     # integration of samples over time to obtain output angle theta
    sigma2 = np.zeros((len(T), M))          # array of dimensions (cluster periods) X (# variables)
    m = m.astype(int)
    m_len = len(m)
    for i in range(0, m_len):          # loop over the various cluster sizes
        a = N-2*m[i]
        for k in range(0, a):    # implements the summation in the AV equation
            sigma2[i, :] = sigma2[i, :] + (theta[k+2*m[i], :] - 2*theta[k+m[i], :] + theta[k, :])**2
    sigma2 = sigma2/np.matlib.repmat((2*T**2*(N-2*m)), M, 1).T
    sigma = np.sqrt(sigma2)
    print('allan() is done...')
    return T, sigma






