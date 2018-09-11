function form()

% Parameters
g = 9.81;

Nx = 19;
x = sym('x', [Nx, 1], 'real');
pt = x(1:3);
pt_t = x(4:6);
pt_tt = x(7:9);
phi = x(10:11);
phi_t = x(12:13);
l = x(14);
l_t = x(15);
c = x(16);
e = x(17:19);


% x_t = f(x, u)
x_t = [
    pt_t
    pt_tt
    zeros(3,1)
    phi_t
    pendel.ode(phi, phi_t, pt_tt, l, l_t, g, c)
    l_t
    0
    0
    zeros(3,1)
];

% Time step
syms Ts 'real'

f = x + x_t*Ts;
F = jacobian(f, x);

h = [
    pt
    pt_t
    l
    l_t
    pendel.kinematics(pt, phi, l) + e; % ph
];

H = jacobian(h, x);

% Make functtions
matlabFunction(f, 'File', '+observer/f.m', 'Vars', {x, Ts});
matlabFunction(F, 'File', '+observer/fJacobian.m', 'Vars', {x, Ts});

matlabFunction(h, 'File', '+observer/h.m', 'Vars', {x});
matlabFunction(H, 'File', '+observer/hJacobian.m', 'Vars', {x});



end