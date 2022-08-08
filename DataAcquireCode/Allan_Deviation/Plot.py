"""
@author: Yongxu Duan
e-mail: duanyongxu1994@gmail.com
"""
import matplotlib.pyplot as plt
import numpy as np


class PlotAllan(object):
    def __init__(self, name, A, B, f):
        self.name = name
        self.A = A
        self.B = B
        self.f = f

    def gyro_plot(self, i):
        plt.figure(i)
        plt.loglog(self.A, self.B[:, 0], '-', self.A, self.B[:, 1], '-', self.A, self.B[:, 2], '-')
        # plt.loglog(self.A, self.B)
        plt.title(self.name)
        plt.xlabel('Averaging Time (s)')
        plt.ylabel('Allan Deviation (deg/s)')
        plt.legend(['X axis', 'Y axis', 'Z axis'], loc='upper right')
        plt.grid(True, which='both', linestyle='-.', color='b', linewidth='0.25')
        plt.savefig('%s/%s.png' % (self.f, self.name))
        plt.show()

    def accel_plot(self, j):
        plt.figure(j)
        plt.loglog(self.A, self.B[:, 0], '-', self.A, self.B[:, 1], '-', self.A, self.B[:, 2], '-')
        # plt.loglog(self.A, self.B)
        plt.title(self.name)
        plt.xlabel('Averaging time (s)')
        plt.ylabel('Allan Deviation (m/s^2)')
        plt.legend(['X axis', 'Y axis', 'Z axis'], loc='upper right')
        plt.grid(True, which='both', linestyle='-.', color='b', linewidth='0.25')
        plt.savefig('%s/%s.png' % (self.f, self.name))
        plt.show()

