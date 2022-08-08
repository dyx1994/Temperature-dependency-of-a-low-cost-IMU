clc 
clear all

fs = 20.0;


f1 = 'mpu9250_data_cd2.txt';

[ax1,ay1,az1,gx1,gy1,gz1,T1] = dataLoad(f1);
n = length(ax1);
time = 0.05*(1:n);
% figure
% plot(time, T1);
% T_av = int8(mean(T1));
% data plot
% figure
% 
% subplot(3,1,1); plot(time,ax1);
% xlabel('t(s)');ylabel('X(m/s^2)');
% axis([0 4000 0.2 0.8]);
% 
% subplot(3,1,2); plot(time,ay1);
% xlabel('t(s)'); ylabel('Y(m/s^2)');
% axis([0 4000 0.0 0.6]);
% 
% 
% subplot(3,1,3); plot(time,az1);
% xlabel('t(s)'); ylabel('Z(m/s^2)');
% axis([0 4000 9.2 9.8]);
% 
% suptitle('Accelerometer Raw Data at 34\circC');
% 
% 
% figure
% subplot(3,1,1); plot(time,gx1);
% xlabel('t(s)');ylabel('X(\circ/s)');
% axis([0 4000 -0.8 -0.2]);
% 
% subplot(3,1,2); plot(time,gy1);
% xlabel('t(s)'); ylabel('Y(\circ/s)');
% axis([0 4000 0.4 1.0]);
% 
% 
% subplot(3,1,3); plot(time,gz1);
% xlabel('t(s)'); ylabel('Z(\circ/s)');
% axis([0 4000 -0.6 0.0]);
% 
% suptitle('Gyroscope Raw Data at 34\circC');

figure
plot(time,ay1);
xlabel('t(s)'); ylabel('Y(m/s^2)');
title('Accelerometer Y-axis Raw Data');








