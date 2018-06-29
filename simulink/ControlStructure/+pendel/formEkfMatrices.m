function model = formEkfMatrices()

% Set default sizes and covariances
Nx = 31;
Nz = 23;

Q = eye(Nx)*0.001^2;
P0 = eye(Nx);

R = eye(Nz)*0.005^2;



x0 = zeros(Nx,1);
x0(13:15) = [0, 0, -90]/180*pi;
x0(23) = 2;
x0(25) = 4*2*pi;
x0(26) = 0.3;
x0(27) = 2*2*pi;
x0(28) = 0.3;

% Return result
model.x0 = x0;
model.Q = Q;
model.R = R;
model.P0 = P0;

end