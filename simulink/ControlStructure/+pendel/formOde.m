function phi_tt = formOde()
%FOMPENDELODE Summary of this function goes here
%   Detailed explanation goes here

pt = sym('pt', [3,1], 'real');
pt_t = sym('pt_t', [3,1], 'real');
pt_tt = sym('pt_tt', [3,1], 'real');

phi = sym('phi', [2,1], 'real');
phi_t = sym('phi_t', [2,1], 'real');
phi_tt = sym('phi_tt', [2,1], 'real');

syms l l_t l_tt 'real'
syms g m 'real'

% State vectors
x = [
    pt
    l
    phi
];

x_t = [
    pt_t
    l_t
    phi_t
];

x_tt = [
    pt_tt
    l_tt
    phi_tt
];

% Kinematics
ph = pendel.kinematics(pt, phi, l);

J_lin_load = jacobian(ph, x);

Ek = 0.5*m*(J_lin_load*x_t)'*(J_lin_load*x_t);
Ep = m*g*(l - l*cos(phi(1))*cos(phi(2)));

L = Ek - Ep;

part1 = jacobian(jacobian(L, x_t),[x; x_t])*[x_t; x_tt];

part2 = jacobian(L, x)';

tau = simplify(part1 - part2);

% To matrix form
[A, b] = equationsToMatrix(...
    [1,0,0,0,0,0]*tau == 0,...
    [0,1,0,0,0,0]*tau == 0,...
    [0,0,1,0,0,0]*tau == 0,...
    [0,0,0,1,0,0]*tau == 0,...
    [0,0,0,0,1,0]*tau == 0,...
    [0,0,0,0,0,1]*tau == 0,...
    x_tt...
);

M = simplify(A);
M1 = M(5:6,1:4);
M2 = M(5:6,5:6);
F = simplify(b);

% Form diiferential equation
phi_tt = simplify(pinv(M2)*(-M1*x_tt(1:4) + F(5:6)));

matlabFunction(phi_tt, 'File', '+pendel/ode', 'Vars', {phi, phi_t, pt_tt l, l_t, g});
    
end

