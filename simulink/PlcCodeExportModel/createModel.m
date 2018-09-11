clear all
close all
clc

% Paramters
load('hydroSupply.mat');

omega_q = 10*2*pi;
zeta_q = 0.7;

omega_w = 4*2*pi;
zeta_w = 0.7;
c = 0.05;
g = 9.81;

% State vector mapping an intial conditions
x = sym('x', [24,1], 'real');
x0 = zeros(length(x), 1);

eta = x(1:6);
v = x(7:12);
q = x(13:15); x0(13:15) = [0, 0, -90]/180*pi;
q_t = x(16:18);
phi = x(19:20); x0(19:20) = [5, 0]/180*pi;
phi_t = x(21:22);
l = x(23); x0(23) = 2;
l_t = x(24);

% Input Mapping
u = sym('u', [10,1], 'real');
u0 = zeros(length(u), 1);

tau = u(1:6);
q_ref = u(7:9); u0(7:9) = [0, 0, -90]/180*pi;
l_ref = u(10); u0(10) = 3.0;

% Disturbacne mapping
d = sym('d', [6,1], 'real');

% ODE's
eta_t = ship.kinematics(eta, v);
v_t = ship.ode(eta, v, supply.Minv, supply.D, supply.G, tau);
q_tt = q_ref*omega_q^2 - 2*zeta_q*omega_q*q_t - omega_q^2*q;
l_tt = l_ref*omega_w^2 - 2*zeta_w*omega_w*l_t - omega_w^2*l;

% Robot tool given in {n}
load('motionlab/calib.mat');

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
phi_tt = pendel.ode(phi, phi_t, pt_tt, l, l_t, g) - c*phi_t;

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
];


matlabFunction(f, 'File', 'test.m', 'Vars', {x, u})

% %% Simulation
% dt = 0.005;
% t = 0:dt:200;
% 
% x = zeros(length(x0), length(t));
% x(:,1) = x0;
% 
% for i = 1:length(t)-1
%     
%     x_t = test(x(:,i), u0);
%     
%     x(:,i+1) = x(:,i) + x_t*dt;
% end
% 
% figure;
% n = 10;
% plot(t, x(19:20,:)/pi*180);


