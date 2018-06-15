function formObserver()

% ** Calibratoin data **
data = load('+motionlab/calib.mat');
Hbr = data.calib.EM8000_TO_COMAU.H;

% ** Paramets **
syms omega zeta 'real'

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

% Robot tool acceleration given in {n}
[pt, pt_t, pt_tt] = pendel.driver(eta, v, v_t, p, p_t, p_tt, Hbr);

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
% ode(29,1) = l_ref*omega^2 - 2*zeta*omega*l_t - omega^2*l;
ode(29,1) = 0;
ode(30:31,1) = phi_t;
ode(32:33,1) = pendel.ode(phi, phi_t, zeros(3,1), l, l_t, c);
% ode(32:33,1) = pendel.ode(phi, phi_t, pt_tt, l, l_t, c);
ode(34,1) = 0;

% State transition function and jacobian
syms Ts 'real';
f = x + ode*Ts;
f = simplify(f);

F = jacobian(f, x);
F = simplify(F);

% Measurement function
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

% Make functtions
matlabFunction(f, 'File', '+pendel/+observer/f.m', 'Vars', {x, Ts});
matlabFunction(F, 'File', '+pendel/+observer/fJacobian.m', 'Vars', {x, Ts});

matlabFunction(h, 'File', '+pendel/+observer/h.m', 'Vars', {x});
matlabFunction(H, 'File', '+pendel/+observer/hJacobian.m', 'Vars', {x});



end