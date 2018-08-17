function [S,w,dw] = PiersonMoscowitz(Hs,Tp,N,plotSpectrum)


w(:,1) = linspace(0.01,1.5*1/Tp*2*pi*2.5,N);
dw = w(2)-w(1);

S = zeros(N,1);
for i = 1:N 
    
    S(i,1) = 5*pi^4*Hs^2/(Tp^4*w(i)^5)*exp(-20*pi^4/(Tp^4*w(i)^4));
    Cn = sqrt(2*S*dw);
end

% Plot the frequency spectrum
if strcmp(plotSpectrum,'true')
    figure;
    plot(w,S,'b'), grid on, hold on
    plot(w,S,'k.')
    xlabel('$\omega - [rad/s]$','FontSize',14,'Interpreter', 'Latex')
    ylabel('$S(\omega) - [m^2/(rad/s)]$','FontSize',14,'Interpreter', 'Latex')
    leg = legend('$S(\omega)$','$S(\omega_i)$');
    set(leg,'FontSize',14,'Interpreter', 'Latex')
end

end