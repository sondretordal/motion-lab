function plotShipSimStates(simout)

close all

% Stack data from simout
t = simout.Time;
eta = simout.Data';

set(groot,'defaultTextInterpreter','latex')
fontSize = 12;
set(0,'defaultAxesFontSize', fontSize)

tS = 20;
T = 230;

t = t-tS;

figure;
plot(t, eta(1,:), 'r'), hold on
plot(t, eta(2,:), 'g')
plot(t, eta(3,:), 'b')
xlim([0, T-tS])
xlabel('Time - [s]')
ylabel('Position - [m]')
legend('x', 'y', 'x')
pbaspect([16 9 1])

print('plotShipSimPositon.eps', '-depsc')

figure;
plot(t, eta(4,:)/pi*180, 'r'), hold on
plot(t, eta(5,:)/pi*180, 'g')
plot(t, eta(6,:)/pi*180, 'b')
xlim([0, T-tS])
xlabel('Time - [s]')
ylabel('Angle - [deg]')
legend('\phi', '\theta', '\psi')
pbaspect([16 9 1])

print('plotShipSimAttitude.eps', '-depsc')

end