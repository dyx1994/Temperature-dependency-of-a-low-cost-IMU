"""
@author: Yongxu Duan
e-mail: duanyongxu1994@gmail.com
"""
import numpy as np
import csv
import pandas as pd


class DataImport(object):
    def __init__(self, filename):
        self.file_name = filename
        self.data_array = None
        self.data_shape = None
        self.mpu = None
        self.lsm = None

    def data_load(self):
        """This method is used to load measured data from txt file.
           Input:
                self.file_name: A txt data file with comma splitting the elements
           Outputs:
                data_array: An array that contains all elements in data file
                data_shape: The shape of data file [M, N]
                mpu: A dict stores data only from mpu
                lsm: A dict stores data only from lsm
        """
        print('data_load is called...')
        data_array = []
        with open(self.file_name) as csvfile:
            csv_reader = csv.reader(csvfile)
            data_header = next(csv_reader)
            for row in csv_reader:
                data_array.append(row)

        # data_array = [[float(x) for x in row] for row in data_array]
        data_array = np.array(data_array)
        data_array = data_array.astype(np.float)        # transform from str to float
        # get the shape of data array
        [M, N] = np.shape(data_array)
        data_shape = [M, N]
        # write the data of mpu into a dictionary
        time = data_array[:, 0]
        mpu_accel = data_array[:, 1:4]
        mpu_gyro = data_array[:, 4:7]
        mpu_magn = data_array[:, 7:10]
        mpu = {'time': time, 'mpu_accel': mpu_accel, 'mpu_gyro': mpu_gyro, 'mpu_magn': mpu_magn}

        # write the data of lsm into dictionary
        time = data_array[:, 0]
        lsm_accel = data_array[:, 10:13]
        lsm_gyro = data_array[:, 13:16]
        lsm_magn = data_array[:, 16:19]
        lsm = {'time': time, 'lsm_accel': lsm_accel, 'lsm_gyro': lsm_gyro, 'lsm_magn': lsm_magn}

        print('data load is done...')
        return data_array, data_shape, mpu, lsm





