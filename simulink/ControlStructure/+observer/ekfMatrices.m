function [x0, Q, R, P0] = ekfMatrices()

% Set default sizes and covariances
Nx = 19;
Nz = 11;

Q = eye(Nx)*0.001^2;
P0 = eye(Nx);

R = eye(Nz)*0.005^2;

x0 = zeros(Nx,1);
x0(1:3) = [-2.4, 4.6, -2.2]; % pt0
x0(14) = 2.5;
x0(16) = 0.2;


% x0(29) = 1*2*pi;
% x0(30) = 0.8;
% 
% x0(31) = 4*2*pi;
% x0(32) = 0.8;

end