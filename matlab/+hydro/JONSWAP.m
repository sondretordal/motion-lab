function [S,w] = JONSWAP(Hs,Tp,N,plotSpectrum)
% S = JONSWAP(Hs,Tp,w,plotSpectrum)
%
% INPUT:
% Hs                Significant wave height
% Tp                Typical wave period
% dw                Delta frequency
% plotSpectrum      'true' or 'false'
%
% OUTPUT:
% S                 Energy spectrum S(w)
% w                 dw:dw:(1/Tp*2*pi)*2.5;

% Source:
% https://en.wikipedia.org/wiki/Sea_state

% Create frequency vector based on N
w(:,1) = linspace(1/Tp*2*pi*0.5,1/Tp*2*pi*2.5,N);

S = zeros(length(w),1);
% Return JONSWAP wave spectrum
for i = 1:length(w);
    % Throw error if 0 is found in w
    if w(i) == 0.0
        fprintf('w(%i) = 0.0 \n',i);
        fprintf('Cant handle 0 frequency! \n',i);
        break;
    end
    
    if w(i) <= 5.24/Tp
        sigma = 0.07;
    else
        sigma = 0.09;
    end
    
    Y = exp(-((0.191*w(i)*Tp-1)/(2^(0.5)*sigma))^2);
    
    S(i) = 155*Hs^2/(Tp^4*w(i)^5)*exp(-944/(Tp^4*w(i)^4))*3.3^Y;
end

% Plot the frequency spectrum
if strcmp(plotSpectrum,'true')
    figure;
    plot(w,S,'b'), grid on, hold on
    plot(w,S,'k.')
    xlabel('$\omega - [rad/s]$','FontSize',14,'Interpreter', 'Latex')
    ylabel('$S(\omega) - [m^2s]$','FontSize',14,'Interpreter', 'Latex')
    leg = legend('$S(\omega)$','$S(\omega_i)$');
    set(leg,'FontSize',14,'Interpreter', 'Latex')
end

end