import allantools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math


def main():
    filename = '/Users/dyx/temperature-dependency-imus/Allan_Deviation/data/mpu9250_data_10-12-2019_17:04:23_20Hz.txt'
    data = pd.read_csv(filename, header=1).values
    accel_x = data[:, 0]
    temp = data[:, 6]
    # print(len(accel_x))
    m = len(accel_x)/36000
    n = int(len(accel_x)/36000)
    labels = []
    plt.figure(1)
    for i in range(0, n):
        accel_x_n = accel_x[36000*i:36000*i+36000]
        [tau2, ad, ade, ns] = allantools.oadev(accel_x_n, rate=20.0, data_type='freq', taus='all')
        plt.loglog(tau2, ad)
        labels.append(r'%i' % i)
    plt.legend(labels, bbox_to_anchor=(0.5, -0.3), ncol=7, loc='lower center', borderaxespad=0)
    plt.xlabel('Averaging time [s]')
    plt.ylabel('Allan deviation $\sigma$ [m/s^2]')
    plt.title('accelerometer x-axis allan plot')
    plt.grid(True, which='both', linestyle='-.', color='b', linewidth='0.25')
    plt.show()

    # temp_mean = np.zeros(n)
    # ad_min = np.zeros(n)
    # plt.figure(2)
    # for i in range(0, n):
    #     temp_n = temp[18000*i:18000*i+18000]
    #     temp_mean[i] = np.mean(temp_n)
    #     accel_x_n = accel_x[18000 * i:18000 * i + 18000]
    #     [tau2, ad, ade, ns] = allantools.oadev(accel_x_n, rate=20.0, data_type='freq', taus='all')
    #     ad_min[i] = np.min(ad)
    # plt.plot(temp_mean, ad_min)
    # plt.gca().invert_xaxis()
    # plt.xlabel('Average Temperature [$\circ$C]')
    # plt.ylabel('Minimum allan deviation $\sigma$ [m/s^2]')
    # plt.show()
    #
    # min_tau = np.zeros(n)
    # plt.figure(3)
    # for i in range(0, n):
    #     temp_n = temp[18000*i:18000*i+18000]
    #     temp_mean[i] = np.mean(temp_n)
    #     accel_x_n = accel_x[18000 * i:18000 * i + 18000]
    #     [tau2, ad, ade, ns] = allantools.oadev(accel_x_n, rate=20.0, data_type='freq', taus='all')
    #     ad_min[i] = np.min(ad)
    #     min_index = np.argmin(ad)
    #     min_tau[i] = tau2[min_index]
    # print(min_tau)
    # print(ad_min)
    # plt.plot(temp_mean, min_tau)
    # plt.gca().invert_xaxis()
    # plt.xlabel('Average Temperature [$\circ$C]')
    # plt.ylabel('tau value of bottom $\sigma$ [m/s^2]')
    # plt.show()







if __name__ == '__main__':
    main()