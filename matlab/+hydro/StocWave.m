function x = StocWave(Hs,Tp,t)
% x = StocWave(Hs,Tp,t)

N = 25;
dw = 10/N;
phi = rand(N,1)*2*pi;
x = zeros(1,length(t));
for i = 1:N 
    w = dw*i;
    Sx = 5*pi^4*Hs^2/(Tp^4*w^5)*exp(-20*pi^4/(Tp^4*w^4));
    Cn = sqrt(2*Sx*dw);

    xn = Cn*sin(w*t-phi(i));
    x = x + xn;
end

end