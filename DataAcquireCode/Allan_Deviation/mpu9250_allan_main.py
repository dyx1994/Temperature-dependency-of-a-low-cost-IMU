"""
@author: Yongxu Duan
e-mail: duanyongxu1994@gmail.com
"""
import os, sys
import math
import numpy as np
from MPU9250_DataLoad import DataImport
from AllanDeviation import allan
from Plot import *


def main():
    # path = '/Users/dyx/temperature-dependency-imus/Plots'
    # os.makedirs(path)
    # f = os.getcwd()
    # f = '/home/dyx/MasterThesisCodes/temperature-dependency-imus/Allan_Deviation/Plots'
    f = '/Users/dyx/temperature-dependency-imus/Allan_Deviation/Plots'
    # print('Plots path is created...')
    filename = '/Users/dyx/temperature-dependency-imus/Allan_Deviation/Duan/mpu9250_data_10-12-2019_17:04:23_20Hz.txt'
    data, data_shape, mpu = DataImport(filename).data_load()
    # print('data is successfully loaded...')
    fs = 20  # Hz
    T = mpu['mpu_temperature']
    print(np.mean(T))
    t = 0.05 * np.arange(0, len(T))
    plt.figure(1)
    plt.plot(t, T)
    plt.xlabel('t [s]')
    plt.ylabel('$\circ$C')
    plt.show()
    print(t)
    print(data_shape)

    # Compute and plot the mpu_accel allan deviation
    mpu_accel_data = mpu['mpu_accel']
    plt.figure(2)
    plt.subplot(311)
    plt.plot(mpu_accel_data[:, 0])
    plt.title('x-axis')
    plt.subplot(312)
    plt.plot(mpu_accel_data[:, 1])
    plt.title('y-axis')
    plt.subplot(313)
    plt.plot(mpu_accel_data[:, 2])
    plt.title('z-axis')
    plt.show()
    [A1, B1] = allan(mpu_accel_data, fs, 100)
    name1 = 'MPU Accelerometer Allan Deviation'
    PlotAllan(name1, A1, B1, f).accel_plot(3)
    #
    # fs = 20
    #
    # mpu_accel_data = mpu['mpu_accel']
    # [L, W] = np.shape(mpu_accel_data)
    # accel_1 = mpu_accel_data[0:int(L/3), :]
    # accel_2 = mpu_accel_data[int(L/3):int(2*L/3), :]
    # accel_3 = mpu_accel_data[int(2*L/3):-1, :]
    # [T1, S1] = allan(accel_1, fs, 100)
    # [T2, S2] = allan(accel_2, fs, 100)
    # [T3, S3] = allan(accel_3, fs, 100)
    # #
    # plt.figure()
    # plt.loglog(T1, S1[:, 1])
    # plt.loglog(T2, S2[:, 1])
    # plt.loglog(T3, S3[:, 1])
    # plt.xlabel('Averaging time [s]')
    # plt.ylabel('Allan deviation $\sigma$ [m/s^2]')
    # plt.title('accelerometer x-axis allan plot')
    # plt.legend(['1st time series', '2nd time series', '3rd time series'], loc='upper right')
    # plt.grid(True, which='both', linestyle='-.', color='b', linewidth='0.25')
    # plt.show()

    # accel_x = mpu_accel_data[:, 0]
    # i = len(accel_x)
    # accel_x_1 = accel_x[0:int(i/3)]
    # accel_x_2 = accel_x[int(i/3):int(2*i/3)]
    # accel_x_3 = accel_x[int(2*i/3):-1]


    # compute and plot the mpu_gyro allan deviation
    # mpu_gyro_data = mpu['mpu_gyro']
    # mpu_gyro_data = mpu_gyro_data * 180 / math.pi   # transform from [rad/s] to [deg/s]
    # [A2, B2] = allan(mpu_gyro_data, fs, 100)
    # name2 = 'MPU Gyro Allan Deviation'
    # PlotAllan(name2, A2, B2, f).gyro_plot(4)
    # print('mpu_gyro is plotted...')


if __name__ == '__main__':
    main()
