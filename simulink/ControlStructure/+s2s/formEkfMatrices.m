function ekf = formEkfMatrices()

Ns = 18;
No = 4;
Nx = 2*Ns + No;


Q1 = zeros(Ns, Ns);
Q1(13:18,13:18) = eye(6)*0.001^2;

Q2 = Q1;

Q3 = eye(4)*0.001^2;

ekf.Q = blkdiag(Q1, Q2, Q3);

ekf.P0 = eye(Nx);

ekf.mru1.R = eye(12)*0.001^2;
ekf.mru2.R = eye(12)*0.001^2;

ekf.at960.R = eye(12)*0.001^2;
