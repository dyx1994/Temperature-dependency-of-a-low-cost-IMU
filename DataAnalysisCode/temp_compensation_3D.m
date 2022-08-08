clc
clear all

f = load('temp_compenstaed_data.mat');
 
ax = f.data_comp(:,1);
T = f.data_comp(:,7);
n = length(ax);

Fs = 20;
tau0 = 1/Fs;
t = [18001:1800:n-18000];
win_len = 36001;

[T_av,tau,S] = DAVAR(ax,t,win_len,tau0,T);

figure
meshz(T_av,tau,S);
colormap(jet);
title('Temperature Compensated Accelerometer X-axis 3D Allan Deviation');
% title('Temperature Compensated Gyroscope X-axis 3D Allan Deviation')
set(gca,'XDir','reverse','YDir','reverse','YScale','log','ZScale','log','ColorScale','log');
axis('tight');
xlabel('T [\circC]');
ylabel('\tau [s]');
zlabel('ADEV \sigma [m/s^2]');
% zlabel('ADEV \sigma [\circ/s]');
view(53,32);