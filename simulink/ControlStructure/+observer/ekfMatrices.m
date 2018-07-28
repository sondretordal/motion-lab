function [x0, Q, R, P0] = ekfMatrices(sim)

% Set default sizes and covariances
Nx = 32;
Nz = 23;

Q = eye(Nx)*0.001^2;
P0 = eye(Nx);

R = eye(Nz)*0.005^2;

x0 = zeros(Nx,1);
x0(13:15) = [0, 0, -90]/180*pi; % q0
x0(19) = 2; % l0
x0(25) = 0.1; % c0

x0(29) = 1*2*pi;
x0(30) = 0.8;

x0(31) = 4*2*pi;
x0(32) = 0.8;

end