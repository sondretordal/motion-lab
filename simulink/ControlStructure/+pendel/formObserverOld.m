function formObserver(calib)

% Static Paramters
g = 9.81;
c = 0.1;

% Time step
syms Ts 'real'

% State vector mapping an intial conditions
x = sym('x', [37,1], 'real');
x0 = zeros(length(x), 1);

eta = x(1:6);
v = x(7:12);
q = x(13:15);
q_t = x(16:18);
phi = x(19:20);
phi_t = x(21:22);
l = x(23);
l_t = x(24);
omega_q = x(25);
zeta_q = x(26);
omega_w = x(27);
zeta_w = x(28);
e = x(29:31);

% Input Mapping
u = sym('u', [4,1], 'real');
u0 = zeros(length(u), 1);

q_ref = u(1:3); u0(1:3) = x0(13:15);
l_ref = u(4); u0(4) = x0(23);

% Ship jacobain
J = [
    eye(3), zeros(3,3);
    zeros(3,3), math3d.Tphi(eta(4:6), 'xyz')
];

% ODE's
eta_t = J*v;
v_t = zeros(6,1);
q_tt = joints.ode(q_ref, q, q_t, omega_q, zeta_q);
l_tt = winch.ode(l_ref, l, l_t, omega_w, zeta_w);

% Robot pt from joints
[p, p_t, p_tt] = comau.forward(q, q_t, q_tt);

% Robot pose relative to EM8000
Hbr = calib.EM8000_TO_COMAU.H;

% Ship/stewart {b} orientation matrix relative to {n}
Rnb = math3d.Rxyz(eta(4:6));

% Body fixed velocity and acceleration skew matrices
W = math3d.skew(v(4:6));
W_t = math3d.skew(v_t(4:6));

Rnb_t = Rnb*W;
Rnb_tt = Rnb*W*W + Rnb*W_t;

% Constant offsets {b} -> {r}
r = Hbr(1:3,4);
Rbr = Hbr(1:3,1:3);

% Position of {t}/{n} given in {n}
pt = eta(1:3) + Rnb*(r + Rbr*p);

% Velocity of {t}/{n} given in {n}
pt_t = v(1:3) + Rnb_t*(r + Rbr*p) + Rnb*(Rbr*p_t);

% Acceleration of {t}/{n} given in {n}
pt_tt = v_t(1:3) + Rnb_tt*(r + Rbr*p)...
    + 2*Rnb_t*(Rbr*p_t) + Rnb*(Rbr*p_tt);

% Pendel ODE
phi_tt = pendel.ode(phi, phi_t, pt_tt, l, l_t, g, c);

% Non linear SS model
f = [
    eta_t
    v_t
    q_t
    q_tt
    phi_t
    phi_tt
    l_t
    l_tt
    zeros(2,1)
    zeros(2,1)
    zeros(3,1)
];

f = x + f*Ts;
F = jacobian(f, x);


% Measurement function
h = [    
    eta
    v
    q
    q_t
    pendel.kinematics(pt, phi, l) + e;
    l
    l_t
];

H = jacobian(h, x);

% Make functtions
matlabFunction(f, 'File', '+pendel/+observer/f.m', 'Vars', {x, u, Ts});
matlabFunction(F, 'File', '+pendel/+observer/fJacobian.m', 'Vars', {x, u, Ts});

matlabFunction(h, 'File', '+pendel/+observer/h.m', 'Vars', {x});
matlabFunction(H, 'File', '+pendel/+observer/hJacobian.m', 'Vars', {x});



end