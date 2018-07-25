function [x0, Q, R, P0] = ekfMatrices()

% Set default sizes and covariances
Nx = 44;
Nz = 23 + 24;

Q = eye(Nx)*0.001^2;
P0 = eye(Nx);

R = eye(Nz)*0.005^2;

x0 = zeros(Nx,1);
x0(29:31) = [0, 0, -90]/180*pi; % q0
x0(39) = 2; % l0

x0(25:28) = [-2, 3, -1, 0];

x0(41) = 0.1; % c0

end