"""
In oder to evaluate the performance of lsm9ds1 by applying allan deviation, it is better to have the same
sampling interval tau for computing allan deviation. The readout method that navio2 provided can hardly
write the data we need at sample rate, here we play the state of art with FIFO buffer to readout the date
at the sample rate.
@ author: Yongxu Duan
e-mail: duanyongxu1994@gmail.com
"""

import spidev
import time
import array
import struct


class LSM9DS1(object):
    __DEVICE_ACC_GYRO = 3


    G_SI = 9.80665
    PI = 3.14159

    # who am I values
    __WHO_AM_I_ACC_GYRO = 0x68

    # Accelerometer and Gyroscope registers
    __LSM9DS1XG_ACT_THS = 0x04
    __LSM9DS1XG_ACT_DUR = 0x05
    __LSM9DS1XG_INT_GEN_CFG_XL = 0x06
    __LSM9DS1XG_INT_GEN_THS_X_XL = 0x07
    __LSM9DS1XG_INT_GEN_THS_Y_XL = 0x08
    __LSM9DS1XG_INT_GEN_THS_Z_XL = 0x09
    __LSM9DS1XG_INT_GEN_DUR_XL = 0x0A
    __LSM9DS1XG_REFERENCE_G = 0x0B
    __LSM9DS1XG_INT1_CTRL = 0x0C
    __LSM9DS1XG_INT2_CTRL = 0x0D
    __LSM9DS1XG_WHO_AM_I = 0x0F  # should return = 0x68
    __LSM9DS1XG_CTRL_REG1_G = 0x10
    __LSM9DS1XG_CTRL_REG2_G = 0x11
    __LSM9DS1XG_CTRL_REG3_G = 0x12
    __LSM9DS1XG_ORIENT_CFG_G = 0x13
    __LSM9DS1XG_INT_GEN_SRC_G = 0x14
    __LSM9DS1XG_OUT_TEMP_L = 0x15
    __LSM9DS1XG_OUT_TEMP_H = 0x16
    __LSM9DS1XG_STATUS_REG = 0x17
    __LSM9DS1XG_OUT_X_L_G = 0x18
    __LSM9DS1XG_OUT_X_H_G = 0x19
    __LSM9DS1XG_OUT_Y_L_G = 0x1A
    __LSM9DS1XG_OUT_Y_H_G = 0x1B
    __LSM9DS1XG_OUT_Z_L_G = 0x1C
    __LSM9DS1XG_OUT_Z_H_G = 0x1D
    __LSM9DS1XG_CTRL_REG4 = 0x1E
    __LSM9DS1XG_CTRL_REG5_XL = 0x1F
    __LSM9DS1XG_CTRL_REG6_XL = 0x20
    __LSM9DS1XG_CTRL_REG7_XL = 0x21
    __LSM9DS1XG_CTRL_REG8 = 0x22
    __LSM9DS1XG_CTRL_REG9 = 0x23
    __LSM9DS1XG_CTRL_REG10 = 0x24
    __LSM9DS1XG_INT_GEN_SRC_XL = 0x26
    __LSM9DS1XG_OUT_X_L_XL = 0x28
    __LSM9DS1XG_OUT_X_H_XL = 0x29
    __LSM9DS1XG_OUT_Y_L_XL = 0x2A
    __LSM9DS1XG_OUT_Y_H_XL = 0x2B
    __LSM9DS1XG_OUT_Z_L_XL = 0x2C
    __LSM9DS1XG_OUT_Z_H_XL = 0x2D
    __LSM9DS1XG_FIFO_CTRL = 0x2E
    __LSM9DS1XG_FIFO_SRC = 0x2F
    __LSM9DS1XG_INT_GEN_CFG_G = 0x30
    __LSM9DS1XG_INT_GEN_THS_XH_G = 0x31
    __LSM9DS1XG_INT_GEN_THS_XL_G = 0x32
    __LSM9DS1XG_INT_GEN_THS_YH_G = 0x33
    __LSM9DS1XG_INT_GEN_THS_YL_G = 0x34
    __LSM9DS1XG_INT_GEN_THS_ZH_G = 0x35
    __LSM9DS1XG_INT_GEN_THS_ZL_G = 0x36
    __LSM9DS1XG_INT_GEN_DUR_G = 0x37

    # Configuration bits Accelerometer and Gyroscope
    __BITS_XEN_G = 0x08
    __BITS_YEN_G = 0x10
    __BITS_ZEN_G = 0x20
    __BITS_XEN_XL = 0x08
    __BITS_YEN_XL = 0x10
    __BITS_ZEN_XL = 0x20
    __BITS_ODR_G_14900mHZ = 0x20
    __BITS_ODR_G_59500mHZ = 0x40
    __BITS_ODR_G_119HZ = 0x60
    __BITS_ODR_G_238HZ = 0x80
    __BITS_ODR_G_476HZ = 0xA0
    __BITS_ODR_G_952HZ = 0xC0
    __BITS_ODR_XL_10HZ = 0x20
    __BITS_ODR_XL_50HZ = 0x40
    __BITS_ODR_XL_119HZ = 0x60
    __BITS_ODR_XL_238HZ = 0x80
    __BITS_ODR_XL_476HZ = 0xA0
    __BITS_ODR_XL_952HZ = 0xC0
    __BITS_FS_G_MASK = 0xE3
    __BITS_FS_G_245DPS = 0x00
    __BITS_FS_G_500DPS = 0x08
    __BITS_FS_G_2000DPS = 0x18
    __BITS_FS_XL_MASK = 0xE7
    __BITS_FS_XL_2G = 0x00
    __BITS_FS_XL_4G = 0x10
    __BITS_FS_XL_8G = 0x18
    __BITS_FS_XL_16G = 0x08


    __READ_FLAG = 0x80
    __MULTIPLE_READ = 0x40

    def __init__(self, spi_bus_number=0):
        self.bus = spidev.SpiDev()
        self.spi_bus_number = spi_bus_number
        self.gyro_scale = None
        self.acc_scale = None
        self.gyroscope_data = [0.0, 0.0, 0.0]
        self.accelerometer_data = [0.0, 0.0, 0.0]
        self.temperature = 0.0

    def bus_open(self, dev_number):
        self.bus.open(self.spi_bus_number, dev_number)
        self.bus.max_speed_hz = 10000000

    def testConnection(self):
        responseXG = self.readReg(self.__DEVICE_ACC_GYRO, self.__LSM9DS1XG_WHO_AM_I)
        if responseXG == self.__WHO_AM_I_ACC_GYRO:
            return True
        else:
            return False

    def writeReg(self, dev_number, reg_address, data):
        self.bus_open(dev_number)
        tx = [reg_address, data]
        rx = self.bus.xfer2(tx)
        self.bus.close()
        return rx

    def readReg(self, dev_number, reg_address):
        self.bus_open(dev_number)
        tx = [reg_address | self.__READ_FLAG, 0x00]
        rx = self.bus.xfer2(tx)
        self.bus.close()
        return rx[1]

    def readRegs(self, dev_number, reg_address, length):
        self.bus_open(dev_number)
        tx = [0] * (length + 1)
        tx[0] = reg_address | self.__READ_FLAG
        rx = self.bus.xfer2(tx)
        self.bus.close()
        return rx[1:len(rx)]

    def initialize(self):
        # --------Accelerometer and Gyroscope---------
        # enable the 3-axes of the gyroscope
        self.writeReg(self.__DEVICE_ACC_GYRO, self.__LSM9DS1XG_CTRL_REG4,
                      self.__BITS_XEN_G | self.__BITS_YEN_G | self.__BITS_ZEN_G)
        # configure the gyroscope
        self.writeReg(self.__DEVICE_ACC_GYRO, self.__LSM9DS1XG_CTRL_REG1_G,
                      self.__BITS_ODR_G_952HZ | self.__BITS_FS_G_2000DPS)
        time.sleep(0.1)

        # enable the three axes of the accelerometer
        self.writeReg(self.__DEVICE_ACC_GYRO, self.__LSM9DS1XG_CTRL_REG5_XL,
                      self.__BITS_XEN_XL | self.__BITS_YEN_XL | self.__BITS_ZEN_XL)
        # configure the accelerometer-specify bandwidth selection with Abw
        self.writeReg(self.__DEVICE_ACC_GYRO, self.__LSM9DS1XG_CTRL_REG6_XL,
                      self.__BITS_ODR_XL_952HZ | self.__BITS_FS_XL_16G)
        time.sleep(0.1)

        self.set_gyro_scale(self.__BITS_FS_G_2000DPS)
        self.set_acc_scale(self.__BITS_FS_XL_16G)

    def set_gyro_scale(self, scale):
        reg = self.__BITS_FS_G_MASK & self.readReg(self.__DEVICE_ACC_GYRO, self.__LSM9DS1XG_CTRL_REG1_G)
        self.writeReg(self.__DEVICE_ACC_GYRO, self.__LSM9DS1XG_CTRL_REG1_G, reg | scale)
        if scale == self.__BITS_FS_G_245DPS:
            self.gyro_scale = 0.00875
        elif scale == self.__BITS_FS_G_500DPS:
            self.gyro_scale = 0.0175
        elif scale == self.__BITS_FS_G_2000DPS:
            self.gyro_scale = 0.07
        else:
            raise ValueError("Not allowed gyro scale")

    def set_acc_scale(self, scale):
        reg = self.__BITS_FS_XL_MASK & self.readReg(self.__DEVICE_ACC_GYRO, self.__LSM9DS1XG_CTRL_REG6_XL)
        self.writeReg(self.__DEVICE_ACC_GYRO, self.__LSM9DS1XG_CTRL_REG6_XL, reg | scale)
        if scale == self.__BITS_FS_XL_2G:
            self.acc_scale = 0.000061
        elif scale == self.__BITS_FS_XL_4G:
            self.acc_scale = 0.000122
        elif scale == self.__BITS_FS_XL_8G:
            self.acc_scale = 0.000244
        elif scale == self.__BITS_FS_XL_16G:
            self.acc_scale = 0.000732
        else:
            raise ValueError("Not allowed accelerometer scale")

#   FIFO read out method

#   The LSM9DS1 embeds 32 slots of 16-bits data FIFO for each of the gyroscope's three output channels and 16-bits
#   data FIFO for each of the accelerometer's three output channels. It can wake up only when needed and burst the
#   significant data out from the FIFO. This buffer can work accordingly to five different modes: Bypass mode,
#   FIFO-MODE, Continuous mode, Continuous-to-FIFO mode and Bypass-to-Continuous. Each mode is selected by the
#   FMODE[2:0] bits in the FIFO_CTRL register. Programmable FIFO threshold status, FIFO overrun events and the
#   number of unread samples stored are available in the FIFO_SRC register and on the INT2_A/G pin in the INT2_CTRL
#   register.

#   The FIFO feature is enabled by writing "1" in CTRL_REG9 (FIFO_EN)
#   To guarantee the correct acquisition of data during the switching into and out of FIFO mode,
#   the first sample acquired must be discarded.

#   Bypass-mode: the FIFO is not operational and it remains empty. It is also used to reset the FIFO when in FIFO mode
#   FIFO-mode: data from the output channels are stored in the FIFO until it is overwritten
#   Continuous-mode: provides continuous FIFO update: as new data arrives the older is discarded.
#   Continuous-to-FIFO mode: FIFO behavior changes according to the INT_GEN_SRC_XL bit. When it is equal to '1',
#                            FIFO operates in FIFO-mode, when it is equal to '0', FIFO operates in Continuous-mode.
#   Bypass-to-Continuous mode: data measurement storage inside FIFO operates in Continuous mode when
#                              INT_GEN_SRC_XL is equal to '1', otherwise FIFO content is reset (Bypass mode).

    def read_FIFO(self):
        fifoSrc = self.readFifoSrc()

        if (fifoSrc & 0x40):
            print("lsm FIFO is overflowed!")
            self.resetFIFO()
        elif fifoSrc == 0:
            print("lsm FIFO is empty")
            return False
        else:

            # Read temperature
            response = self.readRegs(self.__DEVICE_ACC_GYRO, self.__LSM9DS1XG_OUT_TEMP_L, 2)
            self.temperature = self.byte_to_float_le(response) / 256.0 + 25.0

            # Read accelerometer
            response = self.readRegs(self.__DEVICE_ACC_GYRO, self.__LSM9DS1XG_OUT_X_L_XL, 6)
            for i in range(3):
                self.accelerometer_data[i] = self.G_SI * (self.byte_to_float_le(response[2 * i:2 * i + 2]) * self.acc_scale)

            # Read gyroscope
            response = self.readRegs(self.__DEVICE_ACC_GYRO, self.__LSM9DS1XG_OUT_X_L_G, 6)
            for i in range(3):
                self.gyroscope_data[i] = (self.PI / 180.0) * (self.byte_to_float_le(response[2 * i:2 * i + 2]) * self.gyro_scale)


    def readFifoSrc(self):
        return self.readReg(self.__DEVICE_ACC_GYRO, self.__LSM9DS1XG_FIFO_SRC)

    def overrunInterrupt(self):
        return self.writeReg(self.__DEVICE_ACC_GYRO, self.__LSM9DS1XG_INT2_CTRL, 0x10)     # Overrun interrupt

    def resetFIFO(self):
        self.writeReg(self.__DEVICE_ACC_GYRO, self.__LSM9DS1XG_CTRL_REG9, 0x00)     # disable all sets
        pass
        self.writeReg(self.__DEVICE_ACC_GYRO, self.__LSM9DS1XG_CTRL_REG9, 0x12)     # enable FIFO_TEMP_EN and FIFO_EN
        pass

    def enableFIFO(self, flag):
        self.writeReg(self.__DEVICE_ACC_GYRO, self.__LSM9DS1XG_FIFO_CTRL, 0x00)     # Bypass mode, FIFO turned off
        if flag:
            self.resetFIFO()
            self.writeReg(self.__DEVICE_ACC_GYRO, self.__LSM9DS1XG_FIFO_CTRL, 0xC0)     # activate continuous-mode FIFO

    def getFifoData(self):
        self.read_FIFO()
        m6a = self.accelerometer_data
        m6g = self.gyroscope_data
        temp = self.temperature

        return m6a, m6g, temp

    def byte_to_float(self, input_buffer):
        byte_array = array.array("B", input_buffer)
        signed_16_bit_int, = struct.unpack(">h", byte_array)
        return float(signed_16_bit_int)

    def byte_to_float_le(self, input_buffer):
        byte_array = array.array("B", input_buffer)
        signed_16_bit_int, = struct.unpack("<h", byte_array)
        return float(signed_16_bit_int)

    def rotate(self):
        self.accelerometer_data = [-self.accelerometer_data[1], -self.accelerometer_data[0], self.accelerometer_data[2]]

        self.gyroscope_data = [-self.gyroscope_data[1], -self.gyroscope_data[0], self.gyroscope_data[2]]

