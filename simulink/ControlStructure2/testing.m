close all
clear all
clc



dt = 0.005;
t = 0:dt:5;
N = length(t);

y = zeros(N,1);
y_t = zeros(N,1);
y_tt = zeros(N,1);
y_ref = zeros(N,1);

for i = 1:N
    if t(i) <= 1.5
        omega = 1*2*pi;
        zeta = 0.1;
    else
        omega = 5*2*pi;
        zeta = 1;
    end
    
    y_ref(i) = 2*sin(0.3*2*pi*t(i));
    
    y_tt(i) = y_ref(i)*omega^2 - 2*zeta*omega*y_t(i) - omega^2*y(i);
    
    if i < N
        y(i+1) = y(i) + y_t(i)*dt;
        y_t(i+1) = y_t(i) + y_tt(i)*dt;
    end
end

figure;
plot(t, y_ref)
hold on
plot(t, y)
