function model = formModel()

% ** Paramets **
syms Kdc omega zeta 'real'

% Inputs
syms l_ref 'real'

% ** States **
eta = sym('eta', [6,1], 'real');
v = sym('v', [6,1], 'real');
v_t = sym('v_t', [6,1], 'real');
p = sym('p', [3,1], 'real');
p_t = sym('p_t', [3,1], 'real');
p_tt = sym('p_tt', [3,1], 'real');
l = sym('l', 'real');
l_t = sym('l_t', 'real');
phi = sym('phi', [2,1], 'real');
phi_t = sym('phi_t', [2,1], 'real');
c = sym('c', [1,1], 'real');

% Input vector
u = [
    l_ref
];

% State vector
x = [
    eta
    v
    v_t
    p
    p_t
    p_tt
    l
    l_t
    phi
    phi_t
    c
];

% Ship jacobian
J = sym(eye(6));
J(4:6,4:6) = math3d.Tphi(eta(4:6), 'zyx');

% State space ODE
% {n} -> {b}            
ode(1:6,1) = J*v;
ode(7:12,1) = v_t;
ode(13:18,1) = zeros(6,1);

% {r} -> {t} given in {r}
ode(19:21,1) = p_t;
ode(22:24,1) = p_tt;
ode(25:27,1) = zeros(3,1);

% {t} -> {L} given in {n}
ode(28,1) = l_t;
% ode(29,1) = l_ref*Kdc*omega^2 - 2*zeta*omega*l_t - omega^2*l;
ode(29,1) = 0;
ode(30:31,1) = phi_t;
% ode(32:33,1) = pendel.ode(phi, phi_t, zeros(3,1), l, l_t, c);
ode(32:33,1) = pendel.ode(phi, phi_t, zeros(3,1), l, l_t, c);
ode(34,1) = 0;

% State transition function and jacobian
syms Ts 'real';
f = x + ode*Ts;
f = simplify(f);

F = jacobian(f, x);
F = simplify(F);

% Measurement function
data = load('+motionlab/calib.mat');
Hbr = data.calib.EM8000_TO_COMAU.H;

Rnb = math3d.Rzyx(eta(4:6));
Rnr = Rnb*Hbr(1:3,1:3);

% {t} given in {n}
pt = eta(1:3) + Rnb*Hbr(1:3,4) + Rnr*p;

h = [    
    eta
    v
    p
    p_t
    pendel.kinematics(pt, phi, l);
    l
    l_t
];

h = simplify(h); 

H = jacobian(h, x);
H = simplify(H);

% Set default sizes and covariances
Nx = length(x);
Nz = length(h);

Q = eye(Nx)*0.0001^2;
Q(13:18,13:18) = eye(6)*0.05^2;
Q(25:27,25:27) = eye(3)*0.05^2;
Q(29,29) = 0.05^2;
Q(32:33,32:33) = eye(2)*0.1^2;
Q(34,34) = 0.005^2;

R = eye(Nz)*0.001^2;

P = eye(Nx);

x0 = zeros(Nx,1);
x0(19:21) = [1.8, -0.5, 1.5];
x0(28) = 2;

% Return result
model.f = f;
model.F = F;

model.h = h;
model.H = H;

model.x0 = x0;
model.Q = Q;
model.R = R;
model.P = P;

% Make functtions
matlabFunction(f, 'File', '+observer/f.m', 'Vars', {x, u, Ts, omega, zeta, Kdc});
matlabFunction(F, 'File', '+observer/fJacobian.m', 'Vars', {x, u, Ts, omega, zeta, Kdc});

matlabFunction(h, 'File', '+observer/h.m', 'Vars', {x});
matlabFunction(H, 'File', '+observer/hJacobian.m', 'Vars', {x});



end