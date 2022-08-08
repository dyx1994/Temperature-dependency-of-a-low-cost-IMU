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
        # data_array = []
        # with open(self.file_name) as csvfile:
        #     csv_reader = csv.reader(csvfile)
        #     data_header = next(csv_reader)
        #     for row in csv_reader:
        #         data_array.append(row)

        # data_array = np.array(data_array)
        # data_array = data_array.astype(np.float)        # transform from str to float
        data_array = pd.read_csv(self.file_name, header=1)
        data_array = data_array.values

        # get the shape of data array
        [M, N] = np.shape(data_array)
        data_shape = [M, N]
        # write the data of mpu into a dictionary
        mpu_accel = data_array[:, 0:3]
        mpu_gyro = data_array[:, 3:6]
        mpu_temperature = data_array[:, 6]
        mpu = {'mpu_accel': mpu_accel, 'mpu_gyro': mpu_gyro, 'mpu_temperature': mpu_temperature}
        print('data load is done...')
        return data_array, data_shape, mpu





