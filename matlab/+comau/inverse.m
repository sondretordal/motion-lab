function [q, q_t, q_tt] = inverse(p, p_t, p_tt)

% Static link lengths
a1 = 0.350;
a2 = 1.160;
a3 = 0.250;
d1 = 0.830;
d4 = 1.4922;
d6 = 0.210;

% To wire exit point
dt = 0.567;

% To WRE from joint 2
L = d4 + d6 + dt;

% Positional angles
q1 = -atan2(p(2), p(1));

% {t} given in {j1}
T1 = math3d.DH(-q1, d1, a1, pi/2);
Pt = math3d.InvH(T1)*[p(1); p(2); p(3); 1];

% Solve q2 and q3
x = Pt(1);
y = Pt(2);

r = sqrt(a3^2 + L^2);
dtheta = atan2(a3, L);
D = (x^2 + y^2 - a2^2 - r^2)/(2*a2*r);

theta2 = atan2(-sqrt(1 - D^2), D);
theta1 = atan2(y, x) - atan2(r*sin(theta2), a2 + r*cos(theta2));

% Convert to robot angles
q2 = -theta1 + pi/2;
q3 = theta2 - dtheta - q2;

% Posititons
q = [q1; q2; q3];

% Velocity
J = [
    -sin(q1)*(a1 - L*sin(q3) - a3*cos(q3) + a2*sin(q2)),  a2*cos(q1)*cos(q2), -cos(q1)*(L*cos(q3) - a3*sin(q3));
    -cos(q1)*(a1 - L*sin(q3) - a3*cos(q3) + a2*sin(q2)), -a2*cos(q2)*sin(q1),  sin(q1)*(L*cos(q3) - a3*sin(q3));
                                                      0,         -a2*sin(q2),          - L*sin(q3) - a3*cos(q3);
];

q_t = J\p_t;

% Accelerations
q1_t = q_t(1);
q2_t = q_t(2);
q3_t = q_t(3);

J_t = [
    q3_t*sin(q1)*(L*cos(q3) - a3*sin(q3)) - q1_t*cos(q1)*(a1 - L*sin(q3) - a3*cos(q3) + a2*sin(q2)) - a2*q2_t*cos(q2)*sin(q1), - a2*q1_t*cos(q2)*sin(q1) - a2*q2_t*cos(q1)*sin(q2), q3_t*cos(q1)*(L*sin(q3) + a3*cos(q3)) + q1_t*sin(q1)*(L*cos(q3) - a3*sin(q3));
    q3_t*cos(q1)*(L*cos(q3) - a3*sin(q3)) + q1_t*sin(q1)*(a1 - L*sin(q3) - a3*cos(q3) + a2*sin(q2)) - a2*q2_t*cos(q1)*cos(q2),   a2*q2_t*sin(q1)*sin(q2) - a2*q1_t*cos(q1)*cos(q2), q1_t*cos(q1)*(L*cos(q3) - a3*sin(q3)) - q3_t*sin(q1)*(L*sin(q3) + a3*cos(q3));
                                                                                                                            0,                                    -a2*q2_t*cos(q2),                                                -q3_t*(L*cos(q3) - a3*sin(q3));
];

q_tt = J\(p_tt - J_t*q_t);

end