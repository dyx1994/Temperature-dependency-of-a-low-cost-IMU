clc 
clear all


% Import cooling down process data
f = 'mpu9250_data_cd2.txt';
data = csvread(f,1);
a = data(:,1);
% ay = data(:,2);
% az = data(:,3);
% a = data(:,2)*180/3.14159;
% gy = data(:,5)*180/3.14159;
% gz = data(:,6)*180/3.14159;
temp = data(:,7);
n = length(temp);
time = 0.05*(1:n);

% 2D analysis
Fs = 20;
tau0 = 1/Fs;
m = floor(n/36000);
legends = [];
temp_av = [];
RW = [];
BI = [];
TB = [];
err = [];
figure

for i = 0:m-1
    if i == 0
        a_i = a(1:36000);
        temp_i = temp(1:36000);
    else
        a_i = a(36000*i:36000*i+36000);
        temp_i = temp(36000*i:36000*i+36000);
    end
    temp_av(i+1) = round(mean(temp_i));
    err(i+1) = std(temp_i);
    [tau, adev] = allan(a_i,tau0);
    [N, B, tauB] = analyzeAllan(tau, adev);
    RW(i+1) = N;
    BI(i+1) = B;
    TB(i+1) = tauB; 
    loglog(tau,adev,'LineWidth',1.5);
    hold on
    legends{i+1} = [num2str(temp_av(i+1))];
    
end

legend(legends);
title('Accelerometer Cooling Down X-axis Allan Deviation');
xlabel('Averaging Time \tau [s]');
ylabel('ADEV \sigma(\tau) [m/s^2]');
% ylabel('ADEV \sigma(\tau) [\circ/s]');
grid on
set(gca,'MinorGridAlpha',0.95);

figure 

% plot(temp_av,RW,'Marker','*','MarkerSize',10);
errorbar(temp_av,RW,err,'horizontal','Marker','s','MarkerSize',5,'MarkerEdgeColor','red','MarkerFaceColor','red');
title('Accelerometer X-axis VRW');
xlabel('Temperature [\circC]');
ylabel('Random Walk');
set(gca,'XDir','reverse');
grid on

figure
% plot(temp_av,BI,'Marker','*','MarkerSize',10);
errorbar(temp_av,BI,err,'horizontal','Marker','s','MarkerSize',5,'MarkerEdgeColor','red','MarkerFaceColor','red');
title('Accelerometer X-axis BI');
xlabel('Temperature [\circC]');
ylabel('Bias Instability');
set(gca,'XDir','reverse');
grid on

% 3D analysis




