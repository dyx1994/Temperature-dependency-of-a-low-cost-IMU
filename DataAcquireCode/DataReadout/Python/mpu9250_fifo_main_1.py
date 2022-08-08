#!/usr/bin/env python3

import os
import time
from datetime import datetime
import sys
import struct
import csv
from mpu9250_FIFO_1 import MPU9250
from navio.leds import Led


def main():
    # Initialize sensors
    #   Initialize IMUs
    mpu = MPU9250()
    mpu.initialize(low_pass_filter=1)
    mpu.set_acc_scale(0x08)       # +/-4G
    mpu.set_gyro_scale(0x08)      # +/-500dps
    mpu.enableFIFO(True)


    # Test connection:
    if mpu.testConnection():
        print("Connection working.")
    else:
        print("Connection to one of the sensors is faulty.")


    # find new filename
    fileending = 1
    while True:
        if os.path.isfile('/home/pi/Navio2/Duan/Python/meas_data/mpufile_{}_IMU.txt'.format(fileending)) is True:
            fileending += 1
        else:
            break


    now = time.strftime("%d-%m-%Y_%H:%M:%S", time.localtime(time.time()))
    fname = "/home/pi/Duan/Python/meas_data/" + now + r"report.txt"

    # open('', '', 1) enables line buffering
    with open('/home/pi/Navio2/Duan/Python/meas_data/mpufile_{}_IMU.txt'.format(fileending), 'w', 1) as dat_imu:

        # write headers to file
        dat_imu.write('mpu_accel_1 [m/s^2], mpu_accel_2 [m/s^2], mpu_accel_3 [m/s^2], mpu_gyro_1 [rad/s], mpu_gyro_2 [rad/s], mpu_gyro_3 [rad/s], temp [degC]\n')


        # Main loop
        while True:
            mpudata_a, mpudata_g, mpudata_temp = mpu.getFIFOData()
            data = mpudata_a + mpudata_g + mpudata_temp
           # print(data)
            dat_imu.write(str(data).replace("[", "").replace("]", "") + "\n")
            # dat_imu.flush()

            time.sleep(0.005)  # sleep time to restrict update rate


if __name__ == "__main__":

    led = Led()
    led.setColor('Green')

    errfile = "/home/pi/Navio2/Duan/Python/errorfile.txt"

    with open(errfile, 'w', 1) as efile:
        try:
            main()
        except KeyboardInterrupt:
            led.setColor('Yellow')
        except Exception as e:
            led.setColor('Red')
            efile.write("Some error occured:\n{}".format(e))
