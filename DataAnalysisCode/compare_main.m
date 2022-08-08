clc
clear all

Fs = 20.0;
t0 = 1/Fs;

f1 = 'mpu9250_data_34deg.txt';
f2 = 'mpu9250_data_43deg.txt';
f3 = 'mpu9250_data_62deg.txt';
f4 = 'mpu9250_data_82deg.txt';
% f5 = 'mpu9250_data_101deg.txt';

data1 = csvread(f1,1);
ax1 = data1(:,1);
ay1 = data1(:,2);
az1 = data1(:,3);
gx1 = data1(:,4)*180/3.14159;
gy1 = data1(:,5)*180/3.14159;
gz1 = data1(:,6)*180/3.14159;

data2 = csvread(f2,1);
ax2 = data2(:,1);
ay2 = data2(:,2);
az2 = data2(:,3);
gx2 = data2(:,4)*180/3.14159;
gy2 = data2(:,5)*180/3.14159;
gz2 = data2(:,6)*180/3.14159;

data3 = csvread(f3,1);
ax3 = data3(:,1);
ay3 = data3(:,2);
az3 = data3(:,3);
gx3 = data3(:,4)*180/3.14159;
gy3 = data3(:,5)*180/3.14159;
gz3 = data3(:,6)*180/3.14159;

data4 = csvread(f4,1);
ax4 = data4(:,1);
ay4 = data4(:,2);
az4 = data4(:,3);
gx4 = data4(:,4)*180/3.14159;
gy4 = data4(:,5)*180/3.14159;
gz4 = data4(:,6)*180/3.14159;

% data5 = csvread(f5,1);
% ax5 = data5(:,1);
% ay5 = data5(:,2);
% az5 = data5(:,3);
% gx5 = data5(:,4)*180/3.14159;
% gy5 = data5(:,5)*180/3.14159;
% gz5 = data5(:,6)*180/3.14159;

[tau_ax1, adev_ax1] = allan(ax1, t0);
[tau_ax2, adev_ax2] = allan(ax2, t0);
[tau_ax3, adev_ax3] = allan(ax3, t0);
[tau_ax4, adev_ax4] = allan(ax4, t0);
% [tau_ax5, adev_ax5] = allan(ax5, t0);

figure
loglog(tau_ax1, adev_ax1,'LineWidth',1.5);
hold on 
loglog(tau_ax2, adev_ax2,'LineWidth',1.5);
hold on
loglog(tau_ax3, adev_ax3,'LineWidth',1.5);
hold on
loglog(tau_ax4, adev_ax4,'LineWidth',1.5);
% hold on
% loglog(tau_ax5, adev_ax5,'LineWidth',1.5);
% legend('34\circC','43\circC','62\circC','82\circC','101\circC');
legend('34\circC','43\circC','62\circC','82\circC');
title('Accelerometer X-axis Allan Deviation');
xlabel('Averaging Time \tau [s]');
ylabel('ADEV \sigma(\tau) [m/s^2]');
axis([0.01 10000 0.0001 0.1]);
grid on
set(gca,'MinorGridAlpha',0.95);

[tau_ay1, adev_ay1] = allan(ay1, t0);
[tau_ay2, adev_ay2] = allan(ay2, t0);
[tau_ay3, adev_ay3] = allan(ay3, t0);
[tau_ay4, adev_ay4] = allan(ay4, t0);
% [tau_ay5, adev_ay5] = allan(ay5, t0);

figure
loglog(tau_ay1, adev_ay1,'LineWidth',1.5);
hold on 
loglog(tau_ay2, adev_ay2,'LineWidth',1.5);
hold on
loglog(tau_ay3, adev_ay3,'LineWidth',1.5);
hold on
loglog(tau_ay4, adev_ay4,'LineWidth',1.5);
% hold on
% loglog(tau_ay5, adev_ay5,'LineWidth',1.5);
% legend('34\circC','43\circC','62\circC','82\circC','101\circC');
legend('34\circC','43\circC','62\circC','82\circC');
title('Accelerometer Y-axis Allan Deviation');
xlabel('Averaging Time \tau [s]');
ylabel('ADEV \sigma(\tau) [m/s^2]');
grid on
set(gca,'MinorGridAlpha',0.95);

[tau_az1, adev_az1] = allan(az1, t0);
[tau_az2, adev_az2] = allan(az2, t0);
[tau_az3, adev_az3] = allan(az3, t0);
[tau_az4, adev_az4] = allan(az4, t0);
% [tau_az5, adev_az5] = allan(az5, t0);

figure
loglog(tau_az1, adev_az1,'LineWidth',1.5);
hold on 
loglog(tau_az2, adev_az2,'LineWidth',1.5);
hold on
loglog(tau_az3, adev_az3,'LineWidth',1.5);
hold on
loglog(tau_az4, adev_az4,'LineWidth',1.5);
% hold on
% loglog(tau_az5, adev_az5,'LineWidth',1.5);
% legend('34\circC','43\circC','62\circC','82\circC','101\circC');
legend('34\circC','43\circC','62\circC','82\circC');
title('Accelerometer Z-axis Allan Deviation');
xlabel('Averaging Time \tau [s]');
ylabel('ADEV \sigma(\tau) [m/s^2]');
grid on
set(gca,'MinorGridAlpha',0.95);

[tau_gx1, adev_gx1] = allan(gx1, t0);
[tau_gx2, adev_gx2] = allan(gx2, t0);
[tau_gx3, adev_gx3] = allan(gx3, t0);
[tau_gx4, adev_gx4] = allan(gx4, t0);
% [tau_gx5, adev_gx5] = allan(gx5, t0);

figure
loglog(tau_gx1, adev_gx1,'LineWidth',1.5);
hold on 
loglog(tau_gx2, adev_gx2,'LineWidth',1.5);
hold on
loglog(tau_gx3, adev_gx3,'LineWidth',1.5);
hold on
loglog(tau_gx4, adev_gx4,'LineWidth',1.5);
% hold on
% loglog(tau_gx5, adev_gx5,'LineWidth',1.5);
% legend('34\circC','43\circC','62\circC','82\circC','101\circC');
legend('34\circC','43\circC','62\circC','82\circC');
title('Gyroscope X-axis Allan Deviation');
xlabel('Averaging Time \tau [s]');
ylabel('ADEV \sigma(\tau) [\circ/s]');
grid on
set(gca,'MinorGridAlpha',0.95);

[tau_gy1, adev_gy1] = allan(gy1, t0);
[tau_gy2, adev_gy2] = allan(gy2, t0);
[tau_gy3, adev_gy3] = allan(gy3, t0);
[tau_gy4, adev_gy4] = allan(gy4, t0);
% [tau_gy5, adev_gy5] = allan(gy5, t0);

figure
loglog(tau_gy1, adev_gy1,'LineWidth',1.5);
hold on 
loglog(tau_gy2, adev_gy2,'LineWidth',1.5);
hold on
loglog(tau_gy3, adev_gy3,'LineWidth',1.5);
hold on
loglog(tau_gy4, adev_gy4,'LineWidth',1.5);
% hold on
% loglog(tau_gy5, adev_gy5,'LineWidth',1.5);
% legend('34\circC','43\circC','62\circC','82\circC','101\circC');
legend('34\circC','43\circC','62\circC','82\circC');
title('Gyroscope Y-axis Allan Deviation');
xlabel('Averaging Time \tau [s]');
ylabel('ADEV \sigma(\tau) [\circ/s]');
grid on
set(gca,'MinorGridAlpha',0.95);

[tau_gz1, adev_gz1] = allan(gz1, t0);
[tau_gz2, adev_gz2] = allan(gz2, t0);
[tau_gz3, adev_gz3] = allan(gz3, t0);
[tau_gz4, adev_gz4] = allan(gz4, t0);
% [tau_gz5, adev_gz5] = allan(gz5, t0);

figure
loglog(tau_gz1, adev_gz1,'LineWidth',1.5);
hold on 
loglog(tau_gz2, adev_gz2,'LineWidth',1.5);
hold on
loglog(tau_gz3, adev_gz3,'LineWidth',1.5);
hold on
loglog(tau_gz4, adev_gz4,'LineWidth',1.5);
% hold on
% loglog(tau_gz5, adev_gz5,'LineWidth',1.5);
% legend('34\circC','43\circC','62\circC','82\circC','101\circC');
legend('34\circC','43\circC','62\circC','82\circC');
title('Gyroscope Z-axis Allan Deviation');
xlabel('Averaging Time \tau [s]');
ylabel('ADEV \sigma(\tau) [\circ/s]');
grid on
set(gca,'MinorGridAlpha',0.95);
