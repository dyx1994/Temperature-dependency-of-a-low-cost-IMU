clc
clear all


% Import cooling down process data…œ
f = 'mpu9250_data_cd2.txt';
data = csvread(f,1);
% ax = data(:,3);
% ay = data(:,2);
% az = data(:,3);
ax = data(:,6)*180/3.14159;
% gy = data(:,5)*180/3.14159;
% gz = data(:,6)*180/3.14159;
T = data(:,7);
n = length(ax);

Fs = 20;
tau0 = 1/Fs;
t = [18001:1800:n-18000];
win_len = 36001;

[T_av,tau,S] = DAVAR(ax,t,win_len,tau0,T);

figure
meshz(T_av,tau,S);
colormap(jet);
title('Gyroscope Z-axis 3D Allan Deviation')
% title('Accelerometer Z-axis 3D Allan Deviation')
set(gca,'XDir','reverse','YDir','reverse','YScale','log','ZScale','log','ColorScale','log');

axis('tight');
xlabel('T [\circC]')
ylabel('\tau [s]')
% zlabel('ADEV \sigma [m/s^2]');
zlabel('ADEV \sigma [\circ/s]');
view(53,32);