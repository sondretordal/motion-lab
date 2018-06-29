function form(calib)

% Static Paramters
g = 9.81;

% Time step
syms Ts 'real'

% State vector mapping an intial conditions
Nx = 48;
x = sym('x', [Nx,1], 'real');

eta1 = x(1:6);
v1 = x(7:12);

eta2 = x(13:18);
v2 = x(19:24);

o = x(25:28);

q = x(29:31);
q_t = x(32:34);

phi = x(35:36);
phi_t = x(37:38);

l = x(39);
l_t = x(40);

% Phi
omega_q = x(41);
zeta_q = x(42);
omega_l = x(43);
zeta_l = x(44);
c = x(45);

e = x(46:48);


% Input Mapping
u = sym('u', [4,1], 'real');
u0 = zeros(length(u), 1);

q_ref = u(1:3);
l_ref = u(4);

% ODE's
eta1_t = ship.kinematics(eta1, v1);
v1_t = zeros(6,1);

eta2_t = ship.kinematics(eta2, v2);
v2_t = zeros(6,1);

q_tt = joints.ode(q_ref, q, q_t, omega_q, zeta_q);
l_tt = winch.ode(l_ref, l, l_t, omega_l, zeta_l);

% Robot pt from joints
[p, p_t, p_tt] = motionlab.comau.forward(q, q_t, q_tt);

% Robot pose relative to EM8000
Hbr = calib.EM8000_TO_COMAU.H;

% Ship/stewart {b} orientation matrix relative to {n}
Rnb = math3d.Rzyx(eta1(4:6));

% Body fixed velocity and acceleration skew matrices
W = math3d.skew(v1(4:6));
W_t = math3d.skew(v1_t(4:6));

Rnb_t = Rnb*W;
Rnb_tt = Rnb*W*W + Rnb*W_t;

% Constant offsets {b} -> {r}
r = Hbr(1:3,4);
Rbr = Hbr(1:3,1:3);

% Position of {t}/{n} given in {n}
pt = eta1(1:3) + Rnb*(r + Rbr*p);

% Velocity of {t}/{n} given in {n}
pt_t = v1(1:3) + Rnb_t*(r + Rbr*p) + Rnb*(Rbr*p_t);

% Acceleration of {t}/{n} given in {n}
pt_tt = v1_t(1:3) + Rnb_tt*(r + Rbr*p)...
    + 2*Rnb_t*(Rbr*p_t) + Rnb*(Rbr*p_tt);

% Pendel ODE
phi_tt = pendel.ode(phi, phi_t, pt_tt, l, l_t, g, c);

% Non linear SS model
x_t = [
    eta1_t
    v1_t
    eta2_t
    v2_t
    zeros(4,1) % o_t
    q_t
    q_tt
    phi_t
    phi_tt
    l_t
    l_tt
    zeros(5,1) % Phi_t
    zeros(3,1) % e_t
];

f = x + x_t*Ts;
F = jacobian(f, x);


% Measurement function
Rcp = (math3d.Rzyx(eta1(4:6))*calib.EM8000_TO_AT960.H(1:3,1:3))'*...
    math3d.Rz(o(4))*math3d.Rzyx(eta2(4:6))*calib.EM1500_TO_TMAC.H(1:3,1:3);

r1 = eta1(1:3) + math3d.Rzyx(eta1(4:6))*calib.EM8000_TO_AT960.H(1:3,4);
r2 = o(1:3) + math3d.Rz(o(4))*(eta2(1:3) + math3d.Rzyx(eta2(4:6))*calib.EM1500_TO_TMAC.H(1:3,4));

h = [    
    eta1
    v1
    q
    q_t
    pendel.kinematics(pt, phi, l) + e;
    l
    l_t
    eta2
    v2
    (math3d.Rzyx(eta1(4:6))*calib.EM8000_TO_AT960.H(1:3,1:3))'*(r2 - r1)
    Rcp(1,1)
    Rcp(1,2)
    Rcp(1,3)
    Rcp(2,1)
    Rcp(2,2)
    Rcp(2,3)
    Rcp(3,1)
    Rcp(3,2)
    Rcp(3,3)
];

H = jacobian(h, x);

% Make functtions
matlabFunction(f, 'File', '+observer/f.m', 'Vars', {x, u, Ts});
matlabFunction(F, 'File', '+observer/fJacobian.m', 'Vars', {x, u, Ts});

matlabFunction(h, 'File', '+observer/h.m', 'Vars', {x});
matlabFunction(H, 'File', '+observer/hJacobian.m', 'Vars', {x});



end