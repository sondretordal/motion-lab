function model = formEkfMatrices()

% Set default sizes and covariances
Nx = 34;
Nz = 23;

Q = eye(Nx)*0.0001^2;
Q(13:18,13:18) = eye(6)*0.05^2;
Q(25:27,25:27) = eye(3)*0.05^2;
Q(29,29) = 0.05^2;
Q(32:33,32:33) = eye(2)*0.1^2;
Q(34,34) = 0.005^2;

R = eye(Nz)*0.01^2;

P = eye(Nx);

x0 = zeros(Nx,1);
x0(19:21) = [1.8, -0.5, 1.5];
x0(28) = 2;

% Return result
model.x0 = x0;
model.Q = Q;
model.R = R;
model.P = P;

end