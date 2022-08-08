function [T_av,tau,S] = DAVAR(x,t,win_len,tau0,T)
% DAVAR
% INPUT
% x    -->  Data to be analyzed. x must be a column vector.
% t    -->  Vector of time indexes at which the DAVAR is computed
% win_len -->  Length of the window. N must be odd.
% tau0    -->  Time step on the tau axis.
%
% OUTPUT
% S    -->  A Ntau-by-Nt matrix representing the Dynamic Allan Deviation,
%           where Ntau=N/3 (rounded toward zero) and Nt is the length of t.
% T_av -->  Average temperature of clusters
% tau  -->  Average time of clusters

Nx=length(x);
Nt=length(t);

if ~mod(win_len,2)
   error('N must be odd');
end

L1=t(1)-1-(win_len-1)/2;
if L1<0
    x=[zeros(-L1,1);x];
    disp('Warning: zero padding at the beginning of x');
else
    L1=0;
end

L2=t(Nt)+(win_len-1)/2-Nx;
if L2>0
    x=[x;zeros(L2,1)];
    disp('Warning: zero padding at the end of x');
else
    L2=0;
end

Ntau=floor(win_len/3);
tau=tau0*[1:Ntau];
S=zeros(Ntau,Nt);
T_av = zeros(1,Nt);
for n=1:Nt
   T_av(:,n) = mean(T(-L1+t(n)-(win_len-1)/2:-L1+t(n)+(win_len-1)/2));
   xN=x(-L1+t(n)-(win_len-1)/2:-L1+t(n)+(win_len-1)/2);
   S(:,n)=allan_3D(xN,tau0);
end

end