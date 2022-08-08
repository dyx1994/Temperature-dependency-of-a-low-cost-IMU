function [x_compensated] = temp_comp(temp,x,n,T_NB)
% This function is designed for n-th order polynomial temperature 
% compensation for MPU-9250
% Inputs:
%       temp:   temperature vector data
%       x:      raw data
%       n:      n-th polynomial fitting
%       T_NB:   temperature assumed to have no bias
% Outputs:
%       x_compensated: temperature compensated data
p = double(polyfit(temp,x,n)); 
x_compensated = ax - (polyval(p,temp)-polyval(p,T_NB));

end
