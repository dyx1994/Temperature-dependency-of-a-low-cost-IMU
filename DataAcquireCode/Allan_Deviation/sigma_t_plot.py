import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def allan_compute(omega, fs, tau):
    """
    Compute allan deviation at certain tau, only return one value
    """
    theta = np.cumsum(omega)/fs
    tau0 = 1/fs
    N = len(omega)
    m = int(tau/tau0)
    sigma2 = 0
    for i in range(0, N-2*m):
        sigma2 += (theta[i+2*m]-2*theta[i+m]+theta[i])**2
    sigma2 = 1/(2*tau**2)*1/(N-2*m)*sigma2
    sigma = np.sqrt(sigma2)

    return sigma


def dynamic_allan(x, t, N, fs, tau):
    """
    INPUT
    x:  data
    t:  time index array
    N:  length of moving window
    fs: frequency of data
    tau:the averaging time point of allan deviation

    OUTPUT
    S:  allan deviation series at certain tau value
    """
    Nx = len(x)
    Nt = len(t)
    S = []

    if N % 2==0:
        print('N must be odd')
        raise ValueError

    L1 = int(t[0]-1-(N-1)/2)
    if L1 < 0:
        x = np.pad(x, (-L1, 0), mode='constant', constant_values=0.0)
        print('zero padding at the beginning of data array')
    else:
        L1 = 0

    L2 = int(t[Nt-1]+(N-1)/2-Nx)
    if L2 > 0:
        x = np.pad(x, (0, L2), mode='constant', constant_values=0.0)
        print('zero padding at the end of data array')
    else:
        L2 = 0

    for n in range(0, Nt):

        xN = x[-L1+t[n]-int((N-1)/2):-L1+t[n]+int((N-1)/2)]
        S.append(allan_compute(xN, fs, tau))

    return S


def main():
    filename = '/Users/dyx/temperature-dependency-imus/Allan_Deviation/data/mpu9250_data_10-12-2019_17:04:23_20Hz.txt'
    data = pd.read_csv(filename, header=1).values
    gyro_x = data[:, 3]*180/math.pi
    accel_x = data[:, 0]
    L = len(gyro_x)
    fs = 20
    t_index = np.arange(18001, L-18000, 2000, dtype=int)
    win_len = 36001
    tau = 1
    S = dynamic_allan(accel_x, t_index, win_len, fs, tau)
    t = 0.05*t_index
    plt.figure()
    plt.plot(t[1: -1], S[1: -1])
    plt.axis('tight')
    plt.xlabel('t [s]')
    # plt.ylabel('$\sigma$ [$\circ$/s]')
    plt.ylabel('m/s^2')
    plt.title('accel_x $\sigma$ - t plot')
    plt.grid()
    plt.show()


if __name__ == '__main__':
    main()
