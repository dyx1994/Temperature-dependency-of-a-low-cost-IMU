"""
@ author: Yongxu Duan
e-mail: duanyongxu1994@gmail.com
"""

#!/usr/bin/env python3

import os
import time
import sys
import struct
import csv
import smbus2
from datetime import datetime
from mpu_i2c_test import MPU9250


def main():
    mpu = MPU9250()

    mpu.initialize(low_pass_filter_g=0x01, low_pass_filter_a=0x01)
    mpu.set_gyro_scale(0x08)
    mpu.set_acc_scale(0x08)

    sample_rate = input('Please input sample rate:')
    sample_rate_int = int(sample_rate)
    mpu.set_sample_rate(sample_rate_int)
    time.sleep(0.01)
    mpu.enable_fifo_mode(True)
    mpu.select_fifo_mode(True)
    mpu.enable_overflow_interrupt(True)
    mpu.enable_fifo(temp=True, accel=True, gyro=True)
    # time.sleep(0.01)

    # Test connection:
    if mpu.testConnection():
        print("Connection working...")
    else:
        print("Connection is faulty!")

    now = datetime.now().strftime('%d-%m-%Y_%H:%M:%S_')
    fname = '/home/pi/Codes/meas_data/mpu9250_data_' + now + sample_rate + r'Hz.txt'

    with open(fname, 'w', 1) as data_imu:
        # write headers to file
        data_imu.write('mpu_accel_1[m/^2], mpu_accel_2[m/^2], mpu_accel_3[m/^2], mpu_gyro_1[rad/s], mpu_gyro_2[rad/s], mpu_gyro_3[rad/s], temp[degC]\n')
        # print("----1----")
        # Main loop
        while True:
            mpudata_a, mpudata_g, mpudata_temp = mpu.read_fifo_data()
            # print("----2----")
            data = mpudata_a + mpudata_g + mpudata_temp
            print(data)
            data_imu.write(str(data).replace("[", "").replace("]", "") + "\n")
            # data_imu.flush()

            time.sleep(0.005)  # sleep time to restrict update rate
            # print("-----3-----")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Stop connection!')

