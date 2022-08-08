clc 
clear all

% Import Data
f = 'mpu9250_data_34deg.txt';
data = csvread(f,1);
ax = data(:,1);
ay = data(:,2);
az = data(:,3);
gx = data(:,4)*180/3.14159;
gy = data(:,5)*180/3.14159;
gz = data(:,6)*180/3.14159;
Fs = 20.0;
t0 = 1/Fs;
% Compute allan deviation and parameters
% x-axis accelerometer
[tau1, adev1] = allan(ax, t0);
[N1, B1, tauB1] = analyzeAllan(tau1, adev1, 1);
% y-axis acclerometer
[tau2, adev2] = allan(ay, t0);
[N2, B2, tauB2] = analyzeAllan(tau2, adev2, 1);
% z-axis acclerometer
[tau3, adev3] = allan(az, t0);
[N3, B3, tauB3] = analyzeAllan(tau3, adev3, 1);
% % x-axis gyroscope
[tau4, adev4] = allan(gx, t0);
[N4, B4, tauB4] = analyzeAllan(tau4, adev4, 0);
% % y-axis gyroscope
[tau5, adev5] = allan(gy, t0);
[N5, B5, tauB5] = analyzeAllan(tau5, adev5, 0);
% % z-axis gyroscope
[tau6, adev6] = allan(gz, t0);
[N6, B6, tauB6] = analyzeAllan(tau6, adev6, 0);

figure
loglog(tau1, adev1,'LineWidth',1.5);
hold on 
loglog(tau2, adev2,'LineWidth',1.5);
hold on
loglog(tau3, adev3,'LineWidth',1.5);
legend('x-axis','y-axis','z-axis');
title('Accelerometer Allan Deviation at 101\circC');
xlabel('Averaging Time \tau [s]');
ylabel('ADEV \sigma(\tau) [m/s^2]');
grid on
set(gca,'MinorGridAlpha',0.95);

figure
loglog(tau4, adev4,'LineWidth',1.5);
hold on 
loglog(tau5, adev5,'LineWidth',1.5);
hold on
loglog(tau6, adev6,'LineWidth',1.5);
legend('x-axis','y-axis','z-axis');
title('Gyroscope Allan Deviation at 101\circC');
xlabel('Averaging Time \tau [s]');
ylabel('ADEV \sigma(\tau) [\circ/s]');
grid on
set(gca,'MinorGridAlpha',0.95);