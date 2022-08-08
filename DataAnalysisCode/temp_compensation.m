clc
clear all


f = 'mpu9250_data_cd2.txt';
data = csvread(f,1);
ax = data(:,1);
ay = data(:,2);
az = data(:,3);
gx = data(:,4)*180/3.14159;
gy = data(:,5)*180/3.14159;
gz = data(:,6)*180/3.14159;
temp = data(:,7);
n = length(temp);
% time = 0.05*[1:n];
% x = [1:10];
% [m1,s1] = fitting(temp,ax, 10);
% [m2,s2] = fitting(temp,ay, 10);
% [m3,s3] = fitting(temp,az, 10);
% [m4,s4] = fitting(temp,gx, 10);
% [m5,s5] = fitting(temp,gy, 10);
% [m6,s6] = fitting(temp,gz, 10);
% 
% figure 
% scatter(x,m1,'LineWidth',2);
% hold on 
% scatter(x,m2,'LineWidth',2);
% hold on 
% scatter(x,m3,'LineWidth',2);
% legend('ax','ay','az');
% xlabel('n^t^h polynomial');
% ylabel('mean(data-fit)');
% title('Accelerometer Mean Fitting Error');
% 
% figure
% scatter(x,s1,'LineWidth',2);
% hold on
% scatter(x,s2,'LineWidth',2);
% hold on
% scatter(x,s3,'LineWidth',2);
% legend('ax','ay','az');
% xlabel('n^t^h polynomial');
% ylabel('std(data-fit)');
% title('Accelerometer Fitting Error Standard Deviation');
% 
% figure 
% scatter(x,m4,'LineWidth',2);
% hold on 
% scatter(x,m5,'LineWidth',2);
% hold on 
% scatter(x,m6,'LineWidth',2);
% legend('gx','gy','gz');
% xlabel('n^t^h polynomial');
% ylabel('mean(data-fit)');
% title('Gyroscope Mean Fitting Error');
% 
% figure
% scatter(x,s4,'LineWidth',2);
% hold on
% scatter(x,s5,'LineWidth',2);
% hold on
% scatter(x,s6,'LineWidth',2);
% legend('gx','gy','gz');
% xlabel('n^t^h polynomial');
% ylabel('std(data-fit)');
% title('Gyroscope Fitting Error Standard Deviation');
%  polynomial fitting
p1 = double(polyfit(temp,ax,4));
p2 = double(polyfit(temp,ay,4));
p3 = double(polyfit(temp,az,4));

p4 = double(polyfit(temp,gx,4));
p5 = double(polyfit(temp,gy,4));
p6 = double(polyfit(temp,gz,4));

T_NB = 20; % Assumed temperature without bias
% 
ax_compensated = ax - (polyval(p1,temp)-polyval(p1,T_NB));
% ay_compensated = ay - (polyval(p2,temp)-polyval(p2,T_NB));
% az_compensated = az - (polyval(p3,temp)-polyval(p3,T_NB));
% 
% gx_compensated = gx - (polyval(p4,temp)-polyval(p4,T_NB));
% gy_compensated = gy - (polyval(p5,temp)-polyval(p5,T_NB));
% gz_compensated = gz - (polyval(p6,temp)-polyval(p6,T_NB));
% 
% data_comp = zeros(n,7);
% data_comp(:,1) = ax_compensated;
% data_comp(:,2) = ay_compensated;
% data_comp(:,3) = az_compensated;
% data_comp(:,4) = gx_compensated;
% data_comp(:,5) = gy_compensated;
% data_comp(:,6) = gz_compensated;
% data_comp(:,7) = temp;
% 
% file = 'temp_compenstaed_data.mat';
% save(file,'data_comp');
% 
% figure
% 
% subplot(3,1,1); 
% plot(time,ax);
% hold on
% plot(time,ax_compensated);
% xlabel('t(s)');ylabel('X(m/s^2)');
% legend('uncompensated','compensated');
% axis([0 25000 -1 1]);
% 
% subplot(3,1,2); 
% plot(time,ay);
% hold on
% plot(time,ay_compensated);
% xlabel('t(s)'); ylabel('Y(m/s^2)');
% legend('uncompensated','compensated');
% axis([0 25000 -1 1]);
% 
% 
% subplot(3,1,3);
% plot(time,az);
% hold on
% plot(time,az_compensated);
% xlabel('t(s)'); ylabel('Z(m/s^2)');
% legend('uncompensated','compensated');
% % axis([0 25000 8 10]);
% 
% suptitle('Accelerometer Temperature Compensation Data');
% 
% figure
% subplot(3,1,1); 
% plot(time,gx);
% hold on
% plot(time,gx_compensated);
% xlabel('t(s)');ylabel('X(\circ/s)');
% legend('uncompensated','compensated');
% axis([0 25000 -2 2]);
% 
% subplot(3,1,2);
% plot(time,gy);
% hold on
% plot(time,gy_compensated);
% xlabel('t(s)'); ylabel('Y(\circ/s)');
% legend('uncompensated','compensated');
% % axis([0 4500 0.4 1.0]);
% 
% subplot(3,1,3); 
% plot(time,gz);
% hold on
% plot(time,gz_compensated);
% xlabel('t(s)'); ylabel('Z(\circ/s)');
% % axis([0 4500 -0.6 0.0]);
% legend('uncompensated','compensated');
% 
% suptitle('Gyroscope Temperature Compensation Data');