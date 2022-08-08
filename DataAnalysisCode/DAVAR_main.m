clc
clear all

% Import Data
f = 'mpu9250_data_10-12-2019_17_04_23_20Hz.txt';
data = csvread(f,1);
ax = data(:,1);
ay = data(:,2);
az = data(:,3);
gx = data(:,4)*180/3.14159;
gy = data(:,5)*180/3.14159;
gz = data(:,6)*180/3.14159;
temp = data(:,7);

% Frequency
Fs = 20.0;
t0 = 1/Fs;

