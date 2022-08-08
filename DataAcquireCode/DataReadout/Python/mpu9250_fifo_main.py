#!/usr/bin/env python3

import os
import time
import sys
import struct
import csv
from datetime import datetime
from mpu9250_FIFO import MPU9250
from navio.leds import Led


def main():

    # Initialize MPU9250
    mpu = MPU9250()
    # Set maximum SPI bus speed in Hz, default=10000000
    # MPU8250 features:
    # -- 1MHz SPI serial interface for communicating with all registers
    # -- 20MHz SPI serial interface for reading sensor and interrupt registers
    mpu.bus_open(max_speed_hz=10000000)  # Hz

    # Initialize sensors
    # samle_rate unit is Hz
    # low_pass_filter_gt is the low pass filter for gyroscope and temperature sensors. possible values are:
    #           Gyroscope Sensor              |           Temperature Sensor          |        Bits
    #               250 Hz                    |                4000 Hz                |        0x00   NO_DLPF
    #               184 Hz                    |                 188 Hz                |        0x01
    #                92 Hz                    |                  98 Hz                |        0x02
    #                41 Hz                    |                  42 Hz                |        0x03
    #                20 Hz                    |                  20 Hz                |        0x04
    #                10 Hz                    |                  10 Hz                |        0x05
    #                 5 Hz                    |                   5 Hz                |        0x06
    #              3600 Hz                    |                4000 Hz                |        0x07   NO_DLPF
    # low_pass_filter_accel is the low pass filter for accelerometer, possible values are:
    #           Accelerometer Sensor          |                 Bits
    #             218.1 Hz                    |                 0x00
    #             218.1 Hz                    |                 0x01
    #                99 Hz                    |                 0x02
    #              44.8 Hz                    |                 0x03
    #              21.2 Hz                    |                 0x04
    #              10.2 Hz                    |                 0x05
    #              5.05 Hz                    |                 0x06
    #               420 Hz                    |                 0x07       NO_DLPF
    sampleRate = 50
    sampleRateDiv = int(1000 / sampleRate - 1)
    mpu.initialize(sample_rate_div=sampleRateDiv, low_pass_filter_gt=0x01, low_pass_filter_a=0x01)

    # Set accelerometer scale, default is 16G
    # BITS_FS_2G = 0x00
    # BITS_FS_4G = 0x08
    # BITS_FS_8G = 0x10
    # BITS_FS_16G = 0x18
    mpu.set_acc_scale(0x08)       # +/-4G

    # Set gyroscope scale, default is 2000DPS
    # BITS_FS_250DPS = 0x00
    # BITS_FS_500DPS = 0x08
    # BITS_FS_1000DPS = 0x10
    # BITS_FS_2000DPS = 0x18
    mpu.set_gyro_scale(0x08)      # +/-500dps

    # Enable FIFO to collect data
    mpu.enableFIFO(True)


    # Test connection:
    if mpu.testConnection():
        print("Connection working.")
    else:
        print("Connection to one of the sensors is faulty.")


    # find new filename
    # fileending = 1
    # while True:
    #     if os.path.isfile('/home/pi/Duan/Python/meas_data/mpufile_{}_IMU.txt'.format(fileending)) is True:
    #         fileending += 1
    #     else:
    #         break

    # open('', '', 1) enables line buffering
    # with open('/home/pi/Duan/Python/meas_data/mpufile_{}_IMU.txt'.format(fileending), 'w', 1) as dat_imu:

    now = datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
    fname = '/home/pi/Duan/Python/meas_data/mpu9250_data_' + now + r'.txt'

    with open(fname, 'w', 1) as data_imu:
        # write headers to file
        data_imu.write('Sample Rate: %d Hz\n' % sampleRate)
        data_imu.write('mpu_accel_1, mpu_accel_2, mpu_accel_3, mpu_gyro_1, mpu_gyro_2, mpu_gyro_3, temp\n')
        #print("----1----")
        # Main loop
        while True:
            mpudata_a, mpudata_g, mpudata_temp = mpu.getFIFOData()
            #print("----2----")
            data = mpudata_a + mpudata_g + mpudata_temp
           # print(data)
            data_imu.write(str(data).replace("[", "").replace("]", "") + "\n")
            # dat_imu.flush()

            time.sleep(0.005)  # sleep time to restrict update rate
            #print("-----3-----")


if __name__ == "__main__":

    led = Led()
    led.setColor('Green')

    errfile = "/home/pi/Duan/Python/errorfile.txt"

    with open(errfile, 'w', 1) as efile:
        try:
            main()
        except KeyboardInterrupt:
            led.setColor('Yellow')
        except Exception as e:
            led.setColor('Red')
            efile.write("Some error occured:\n{}".format(e))
