function form(calib)

% Static Paramters
g = 9.81;

% Time step
syms Ts 'real'

% State vector mapping an intial conditions
Nx = 32;
x = sym('x', [Nx,1], 'real');

eta = x(1:6);
v = x(7:12);

q = x(13:15);
q_t = x(16:18);

l = x(19);
l_t = x(20);

phi = x(21:22);
phi_t = x(23:24);

c = x(25);

e = x(26:28);

omega_q = x(29);
zeta_q = x(30);

omega_l = x(31);
zeta_l = x(32);

% Input mapping
Nu = 4;
u = sym('u', [Nu,1], 'real');

q_ref = u(1:3);
l_ref = u(4);

% ODE's
eta_t = ship.kinematics(eta, v);
v_t = zeros(6,1);

q_tt = joints.ode(q_ref, q, q_t, omega_q, zeta_q);

l_tt = winch.ode(l_ref, l, l_t, omega_l, zeta_l);

c_t = 0;

e_t = zeros(3,1);

% Robot pt from joints
[p, p_t, p_tt] = motionlab.comau.forward(q, q_t, q_tt);

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
x_t = [
    eta_t
    v_t
    q_t
    q_tt
    l_t
    l_tt
    phi_t
    phi_tt    
    c_t
    e_t
    zeros(4,1)
];

f = x + x_t*Ts;
F = jacobian(f, x);

h = [    
    eta
    v
    q
    q_t
    l
    l_t
    pendel.kinematics(pt, phi, l) + e; % ph
];

H = jacobian(h, x);

% Make functtions
matlabFunction(f, 'File', '+observer/f.m', 'Vars', {x, u, Ts});
matlabFunction(F, 'File', '+observer/fJacobian.m', 'Vars', {x, u, Ts});

matlabFunction(h, 'File', '+observer/h.m', 'Vars', {x});
matlabFunction(H, 'File', '+observer/hJacobian.m', 'Vars', {x});



end