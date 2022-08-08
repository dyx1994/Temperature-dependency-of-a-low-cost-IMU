% Allan Deviation
function [sigma] = allan_3D(x,tau0)
x = cumsum(x, 1)*tau0;
N=length(x);
taumax=floor(N/3);
sigma=zeros(taumax,1);
sigma2=zeros(taumax,1);
for k=1:taumax
   for n=1:N-2*k
       sigma2(k)=sigma2(k)+(x(n+2*k)-2*x(n+k)+x(n))^2;
   end
   tau=k*tau0;
   sigma2(k)=1/(2*tau^2)*1/(N-2*k)*sigma2(k);
   sigma(k)=sqrt(sigma2(k));
end
