function K = lqr()

% State space version of pendulum ode
x = sym('x', [10,1], 'real');
pt = x(1:3);
pt_t = x(4:6);
phi = x(7:8);
phi_t = x(9:10);

u = sym('u', [3,1], 'real');
pt_tt = u(1:3);

% Parameters
g = 9.81;
c = 0.1;
l = 3.0;
l_t = 0;

% f(x, u)
f = [
    pt_t
    pt_tt
    phi_t
    pendel.ode(phi, phi_t, pt_tt, l, l_t, g, c)
];

% h(x, u)
h = [
    pt
    phi
];

% Linearized model
x0 = zeros(length(x),1);
u0 = zeros(length(u),1);

A = double(subs(jacobian(f, x), [x; u], [x0; u0]));
B = double(subs(jacobian(f, u), [x; u], [x0; u0]));
C = double(subs(jacobian(h, x), [x; u], [x0; u0]));
D = double(subs(jacobian(h, u), [x; u], [x0; u0]));

sys = ss(A, B, C, D);

Co = ctrb(A, B);
unco = length(A) - rank(Co)

% LQR Controller to drive x -> 0
Q = diag([
    1./(ones(3,1)*0.4^2)
    1./(ones(3,1)*1^2)
    1./(ones(2,1)*(2/180*pi)^2)
    1./(ones(2,1)*(5/180*pi)^2)
]);

R = diag([
    1./(ones(3,1)*1^2)
]).^2;

[K, S, e] = lqr(A, B, Q, R);

end
