function [N, B, tauB] = analyzeAllan(tau, adev, type)
%%
% This function is to compute the angle/velocity random walk and bias
% instability values based on analyzing allan deviation. This function
% also return plot of allan deviation with specific parameters.
% Inputs:
%           tau: averaging time [s] computed from allan function
%           adev: allan deviation computed from allan function
%           type: 1 -- inputs are from accelerometer 
%                 0 -- inputs are from gyroscope
% Outputs:  
%           N: angle/velocity random walk value
%           B: bias instability value
%           tauB: the tau value when bias instability occurs 
%%
% Compute the slope of the log-scaled Allan deviation against Tau
logtau = log10(tau);
logadev = log10(adev);
dlogadev = diff(logadev) ./ diff(logtau);

% Find Angle/Velocity Random Walk
slope = -0.5; % Angle/Velocity random walk has the slope of -0.5
[~, i] = min(abs(dlogadev - slope));

% Find the y-intercept of the line.
b = logadev(i) - slope*logtau(i);

% Determine the angle random walk coefficient from the line.
logN = slope*log(1) + b;
N = 10^logN;
tauN = 1;
lineN = N ./ sqrt(tau);
% figure
% loglog(tau, adev, tau, lineN, '--', tauN, N, 'o')
% title('Allan Deviation with Angle Random Walk')
% xlabel('\tau')
% ylabel('\sigma(\tau)')
% legend('\sigma', '\sigma_N')
% text(tauN, N, 'N')
% grid on

% Find Bias Instability
slope = 0;
i = find(dlogadev>0,1,'first'); % Find the first point that slope equals 0

% Find the y-intercept of the line.
b = logadev(i) - slope*logtau(i);

% Determine the bias instability coefficient from the line.
scfB = sqrt(2*log(2)/pi);
logB = b - log10(scfB);
B = 10^logB;
tauB = tau(i);
lineB = B * scfB * ones(size(tau));
% Plot the results.
tauB = tau(i);
lineB = B * scfB * ones(size(tau));
% figure
% loglog(tau, adev, tau, lineB, '--', tauB, scfB*B, 'o')
% title('Allan Deviation with Bias Instability')
% xlabel('\tau')
% ylabel('\sigma(\tau)')
% legend('\sigma', '\sigma_B')
% text(tauB, scfB*B, '0.664B')
% grid on

% Plot all parameters with Allan deviation
tauParams = [tauN,tauB];
params = [N,scfB*B];
figure
loglog(tau, adev, 'LineWidth', 1.5);
hold on
loglog(tau, lineN,'LineWidth',1.5,'LineStyle','--');
hold on
loglog(tau, lineB,'LineWidth',1.5,'LineStyle','--');
hold on
loglog(tauParams, params, 'o');
% loglog(tau, [lineN, lineB], '--',...
%     tauParams, params, '*')
title('Allan Deviation with Noise Parameters')
xlabel('Averaging time \tau [s]')
if type == 1
    ylabel('AVAR \sigma(\tau) [m/s^2]')
else
    ylabel('AVAR \sigma(\tau) [\circ/s]')
end
legend('\sigma', '\sigma_N', '\sigma_B')
text(tauParams, params, {'N', '0.664B'})
grid on
set(gca,'MinorGridAlpha',0.95);

end