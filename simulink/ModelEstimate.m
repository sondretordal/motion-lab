function [Kss, tau] = ModelEstimate(data, compare)

N = length(data.t);
y_t = zeros(N,1);

% Numerical differentiation of y
for i = 2:N
    dt = data.t(i) - data.t(i-1);
    
    y_t(i) = (data.y(i) - data.y(i-1))/dt;
end

% Stack data in measurement matrix
A = [data.u, -y_t];

% Solve using least squares method
phi = inv(A'*A)*A'*data.y;

Kss = phi(1);
tau = phi(2);

y_sim = zeros(N,1);
for i = 2:N
    dt = data.t(i) - data.t(i-1);
    
    y_t = 1/tau*(Kss*data.u(i) - y_sim(i-1));
    
    y_sim(i) = y_sim(i-1) + y_t*dt;
end

if compare
    figure();
    plot(data.t, data.y, 'b'), hold on
    plot(data.t, y_sim, 'r--')
end

end