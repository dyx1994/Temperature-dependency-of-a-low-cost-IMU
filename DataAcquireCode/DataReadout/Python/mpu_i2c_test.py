"""MPU9250 I2C communication"""

import array
import time
import struct
import smbus2



class MPU9250:

    G_SI = 9.80665
    PI = 3.14159

    # MPU9250 Default I2C slave address
    __SLAVE_ADDRESS     = 0x68
    # Device id
    __DEVICE_ID         = 0x71
    # Registers
    __SMPLRT_DIV       = 0x19
    __CONFIG            = 0x1A
    __GYRO_CONFIG       = 0x1B
    __ACCEL_CONFIG      = 0x1C
    __ACCEL_CONFIG_2    = 0x1D
    __LP_ACCEL_ODR      = 0x1E
    __WOM_THR           = 0x1F
    __FIFO_EN           = 0x23
    __I2C_MST_CTRL      = 0x24
    __I2C_MST_STATUS    = 0x36
    __INT_PIN_CFG       = 0x37
    __INT_ENABLE        = 0x38
    __INT_STATUS        = 0x3A
    __ACCEL_XOUT_H      = 0x3B
    __ACCEL_XOUT_L      = 0x3C
    __ACCEL_YOUT_H      = 0x3D
    __ACCEL_YOUT_L      = 0x3E
    __ACCEL_ZOUT_H      = 0x3F
    __ACCEL_ZOUT_L      = 0x40
    __TEMP_OUT_H        = 0x41
    __TEMP_OUT_L        = 0x42
    __GYRO_XOUT_H       = 0x43
    __GYRO_XOUT_L       = 0x44
    __GYRO_YOUT_H       = 0x45
    __GYRO_YOUT_L       = 0x46
    __GYRO_ZOUT_H       = 0x47
    __GYRO_ZOUT_L       = 0x48
    __I2C_MST_DELAY_CTRL= 0x67
    __SIGNAL_PATH_RESET = 0x68
    __MOT_DETECT_CTRL   = 0x69
    __USER_CTRL         = 0x6A
    __PWR_MGMT_1        = 0x6B
    __PWR_MGMT_2        = 0x6C
    __FIFO_COUNTH       = 0x72
    __FIFO_COUNTL       = 0x73
    __FIFO_R_W          = 0x74
    __WHO_AM_I          = 0x75

    # Configuration bits MPU9250
    __BIT_SLEEP = 0x40
    __BIT_H_RESET = 0x80
    __BITS_CLKSEL = 0x07
    __MPU_CLK_SEL_PLLGYROX = 0x01
    __MPU_CLK_SEL_PLLGYROZ = 0x03
    __MPU_EXT_SYNC_GYROX = 0x02
    __BITS_FS_250DPS = 0x00
    __BITS_FS_500DPS = 0x08
    __BITS_FS_1000DPS = 0x10
    __BITS_FS_2000DPS = 0x18
    __BITS_FS_2G = 0x00
    __BITS_FS_4G = 0x08
    __BITS_FS_8G = 0x10
    __BITS_FS_16G = 0x18
    __BITS_FS_MASK = 0x18
    __BITS_DLPF_CFG_256HZ_NOLPF2 = 0x00
    __BITS_DLPF_CFG_188HZ = 0x01
    __BITS_DLPF_CFG_98HZ = 0x02
    __BITS_DLPF_CFG_42HZ = 0x03
    __BITS_DLPF_CFG_20HZ = 0x04
    __BITS_DLPF_CFG_10HZ = 0x05
    __BITS_DLPF_CFG_5HZ = 0x06
    __BITS_DLPF_CFG_2100HZ_NOLPF = 0x07
    __BITS_DLPF_CFG_MASK = 0x07
    __BIT_INT_ANYRD_2CLEAR = 0x10
    __BIT_RAW_RDY_EN = 0x01
    __BIT_I2C_IF_DIS = 0x10

    def __init__(self):
        self.bus = smbus2.SMBus(1)
        self.address = self.__SLAVE_ADDRESS
        self.fifoCount = 0
        self.temperature = [0.0]
        self.gyroscope_data = [0.0, 0.0, 0.0]
        self.accelerometer_data = [0.0, 0.0, 0.0]

# -----------------------------------------------------------------------------------------------

    def byte_to_float(self, input_buffer):
        byte_array = array.array("B", input_buffer)
        signed_16_bit_int, = struct.unpack(">h", byte_array)  # h means 2 bytes integer, > means big-endian
        return float(signed_16_bit_int)

# -----------------------------------------------------------------------------------------------
#                                 TEST CONNECTION
# usage: call this function to know if SPI and MPU9250 are working correctly.
# returns true if mpu9250 answers
# -----------------------------------------------------------------------------------------------

    def testConnection(self):
        response = self.bus.read_byte_data(self.address, self.__WHO_AM_I)
        if response == self.__DEVICE_ID:
            return True
        else:
            return False

# -----------------------------------------------------------------------------------------------
#                                 ACCELEROMETER SCALE
# usage: call this function at startup, after initialization, to set the right range for the
# accelerometers.
# -----------------------------------------------------------------------------------------------

    def set_acc_scale(self, scale):
        self.bus.write_byte_data(self.address, self.__ACCEL_CONFIG, scale)
        if (scale == self.__BITS_FS_2G):
            self.acc_divider = 16384.0
        elif (scale == self.__BITS_FS_4G):
            self.acc_divider = 8192.0
        elif (scale == self.__BITS_FS_8G):
            self.acc_divider = 4096.0
        elif (scale == self.__BITS_FS_16G):
            self.acc_divider = 2048.0

# -----------------------------------------------------------------------------------------------
#                                 GYROSCOPE SCALE
# usage: call this function at startup, after initialization, to set the right range for the
# gyroscopes.
# -----------------------------------------------------------------------------------------------

    def set_gyro_scale(self, scale):
        self.bus.write_byte_data(self.address, self.__GYRO_CONFIG, scale)
        if (scale == self.__BITS_FS_250DPS):
            self.gyro_divider = 131.0
        elif (scale == self.__BITS_FS_500DPS):
            self.gyro_divider = 65.5
        elif (scale == self.__BITS_FS_1000DPS):
            self.gyro_divider = 32.8
        elif (scale == self.__BITS_FS_2000DPS):
            self.gyro_divider = 16.4

    # ------------------------------------------------------------------------------------------------
    def initialize(self, low_pass_filter_g=0x01, low_pass_filter_a=0x01):
        self.bus.write_byte_data(self.address, self.__PWR_MGMT_1, 0x80)
        time.sleep(0.01)
        self.bus.write_byte_data(self.address, self.__PWR_MGMT_1, 0x01)
        time.sleep(0.01)
        self.bus.write_byte_data(self.address, self.__PWR_MGMT_2, 0x00)
        time.sleep(0.01)
        self.bus.write_byte_data(self.address, self.__CONFIG, low_pass_filter_g)
        time.sleep(0.01)
        self.bus.write_byte_data(self.address, self.__GYRO_CONFIG, 0x18)
        time.sleep(0.01)
        self.bus.write_byte_data(self.address, self.__ACCEL_CONFIG, 0x08)
        time.sleep(0.01)
        self.bus.write_byte_data(self.address, self.__ACCEL_CONFIG_2, low_pass_filter_a)
        time.sleep(0.01)
        self.bus.write_byte_data(self.address, self.__INT_PIN_CFG, 0x30)
        time.sleep(0.01)
        self.bus.write_byte_data(self.address, self.__USER_CTRL, 0x20)
        time.sleep(0.01)
        self.bus.write_byte_data(self.address, self.__I2C_MST_CTRL, 0x0D)
        time.sleep(0.01)

        self.set_gyro_scale(self.__BITS_FS_16G)
        self.set_acc_scale(self.__BITS_FS_2000DPS)

    def set_sample_rate(self, rate):
        sample_rate_div = int(1000/rate - 1)
        self.bus.write_byte_data(self.address, self.__SMPLRT_DIV, sample_rate_div)

    def enable_fifo_mode(self, flag):
        reg = self.bus.read_byte_data(self.address, self.__USER_CTRL)
        if flag:
            reg |= (1 << 6)
        else:
            reg &= ~(1 << 6)
        self.bus.write_byte_data(self.address, self.__USER_CTRL, reg)

    def select_fifo_mode(self, flag):
        reg = self.bus.read_byte_data(self.address, self.__CONFIG)
        if flag:
            reg |= (1 << 6)
        else:
            reg &= ~(1 << 6)
        self.bus.write_byte_data(self.address, self.__CONFIG, reg)

    def reset_fifo(self):
        reg = self.bus.read_byte_data(self.address, self.__USER_CTRL)
        reg |= (1 << 2)
        self.bus.write_byte_data(self.address, self.__USER_CTRL, reg)

    def enable_fifo(self, temp, accel, gyro):
        self.reset_fifo()
        self.enable_temp_fifo(temp)
        self.enable_accel_fifo(accel)
        self.enable_gyro_fifo(gyro)

    def enable_temp_fifo(self, flag):
        reg = self.bus.read_byte_data(self.address, self.__FIFO_EN)
        if flag:
            reg |= (1 << 7)
        else:
            reg &= ~(1 << 7)
        self.bus.write_byte_data(self.address, self.__FIFO_EN, reg)

    def enable_gyro_fifo(self, flag):
        reg = self.bus.read_byte_data(self.address, self.__FIFO_EN)
        if flag:
            reg |= (1 << 6)
            reg |= (1 << 5)
            reg |= (1 << 4)
        else:
            reg &= ~(1 << 6)
            reg &= ~(1 << 5)
            reg &= ~(1 << 4)
        self.bus.write_byte_data(self.address, self.__FIFO_EN, reg)

    def enable_accel_fifo(self, flag):
        reg = self.bus.read_byte_data(self.address, self.__FIFO_EN)
        if flag:
            reg |= (1 << 3)
        else:
            reg &= ~(1 << 3)
        self.bus.write_byte_data(self.address, self.__FIFO_EN, reg)

    def get_fifo_count(self):
        response = self.bus.read_i2c_block_data(self.address, self.__FIFO_COUNTH, 2)
        fifoCount = int(self.byte_to_float(response))
        return fifoCount

    def enable_overflow_interrupt(self, flag):
        reg = self.bus.read_byte_data(self.address, self.__INT_ENABLE)
        if flag:
            reg |= (1 << 4)
        else:
            reg &= ~(1 << 4)
        self.bus.write_byte_data(self.address, self.__INT_ENABLE,reg)

    def get_status(self):
        return self.bus.read_byte_data(self.address, self.__INT_STATUS)

    def get_fifo_bytes(self, fifoCount):
        return_list = list()
        for i in range(0, fifoCount):
            return_list.append(self.bus.read_byte_data(self.address, self.__FIFO_R_W))
        return return_list

    def read_fifo_data(self):
        while True:
            int_status = self.get_status()
            fifoCount = self.get_fifo_count()
            if fifoCount < 14:
                # self.fifoCount = self.get_fifo_count()
                continue

            elif (int_status & 0x10) == 0x10 or fifoCount >= 512:
                print('Overflow!')
                #self.reset_fifo()
                break

            else:
                # response = self.bus.read_i2c_block_data(self.address, self.__FIFO_R_W, 14)
                response = self.get_fifo_bytes(fifoCount)
                packet_count = int(len(response) / 14)
                # print("packet count:%d" % packet_count)

                for j in range(0, packet_count):

                    # Get Accelerometer values
                    for i in range(0, 3):
                        data = self.byte_to_float(response[i * 2:i * 2 + 2])
                        self.accelerometer_data[i] = self.G_SI * data / self.acc_divider
                        # print(self.accelerometer_data)
                    # Get temperature
                    i = 3
                    temp = self.byte_to_float(response[i * 2:i * 2 + 2])
                    self.temperature[i-3] = (temp / 333.87) + 21.0
                    # print(self.temperature)
                    # Get gyroscope values
                    for i in range(4, 7):
                        data = self.byte_to_float(response[i * 2:i * 2 + 2])
                        self.gyroscope_data[i-4] = (self.PI / 180) * data / self.gyro_divider
                        # print(self.gyroscope_data)

                    return self.accelerometer_data, self.gyroscope_data, self.temperature

