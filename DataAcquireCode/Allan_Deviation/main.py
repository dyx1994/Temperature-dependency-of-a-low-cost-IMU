import math
import numpy as np
import allantools
import matplotlib.pyplot as plt
import pandas as pd


def main():
    # data load
    # files
    f1 = '/Users/dyx/temperature-dependency-imus/Allan_Deviation/data/mpu9250_data_02-12-2019_09:22:04_20Hz.txt'
    data_array_1 = pd.read_csv(f1, header=1)

    ax1 = data_array_1[:, 0]
    ay1 = data_array_1[:, 1]






if __name__ == '__main__':
    main()

