function [D,theta,dtheta] = DirectionSpectrum(N,type,plotSpectrum)




theta(:,1) = linspace(-pi/2,pi/2,N);
dtheta  = theta(2)-theta(1);


if strcmp(type,'type1')
    D(:,1) = 2/pi*cos(theta).^2;
elseif strcmp(type,'type2')
    D(:,1) = 8/(3*pi)*cos(theta).^4;
end

% Plot the direction spectrum
if strcmp(plotSpectrum,'true')
    figure;
    plot(theta,D,'b'), grid on, hold on
    plot(theta,D,'k.')
    xlabel('$\theta - [rad]$','FontSize',14,'Interpreter', 'Latex')
    ylabel('$D(\theta) - [-]$','FontSize',14,'Interpreter', 'Latex')
    leg = legend('$D(\theta)$','$D(\theta_i)$');
    set(leg,'FontSize',14,'Interpreter', 'Latex')
end




end