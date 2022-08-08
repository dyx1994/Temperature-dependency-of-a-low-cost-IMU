function [tau, adev] = allan(omega,t0)
%%
% This function is to compute for a single axis allan deviation and 
% averaging time tau values. 
% Inputs: 
%        omega: rate output
%        t0:    time interval
% Outputs:
%        tau:   averaging time [s]
%        adev:  overlapping allan deviation value
%%
theta = cumsum(omega, 1)*t0;
maxNumM = 100;
L = size(theta, 1);
maxM = 2.^floor(log2(L/2));
m = logspace(log10(1), log10(maxM), maxNumM).';
m = ceil(m); % m must be an integer.
m = unique(m); % Remove duplicates.
tau = m*t0;
avar = zeros(numel(m), 1);
for i = 1:numel(m)
    mi = m(i);
    avar(i,:) = sum((theta(1+2*mi:L) - 2*theta(1+mi:L-mi) + theta(1:L-2*mi)).^2, 1);
end
avar = avar ./ (2*tau.^2 .* (L - 2*m));
adev = sqrt(avar);
end
