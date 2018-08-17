function [p, p_t, p_tt] = forward(q, q_t, q_tt)

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

% Position {b} -> {t}
q1 = q(1);
q2 = q(2);
q3 = q(3);

q1_t = q_t(1);
q2_t = q_t(2);
q3_t = q_t(3);

% Obtained from formForwardModel
p = [
    cos(q1)*(a1 - L*sin(q3) - a3*cos(q3) + a2*sin(q2));
    -sin(q1)*(a1 - L*sin(q3) - a3*cos(q3) + a2*sin(q2));
    d1 + L*cos(q3) + a2*cos(q2) - a3*sin(q3);
];

J = [
    -sin(q1)*(a1 - L*sin(q3) - a3*cos(q3) + a2*sin(q2)),  a2*cos(q1)*cos(q2), -cos(q1)*(L*cos(q3) - a3*sin(q3));
    -cos(q1)*(a1 - L*sin(q3) - a3*cos(q3) + a2*sin(q2)), -a2*cos(q2)*sin(q1),  sin(q1)*(L*cos(q3) - a3*sin(q3));
                                                      0,         -a2*sin(q2),          - L*sin(q3) - a3*cos(q3);
];

J_t = [
    q3_t*sin(q1)*(L*cos(q3) - a3*sin(q3)) - q1_t*cos(q1)*(a1 - L*sin(q3) - a3*cos(q3) + a2*sin(q2)) - a2*q2_t*cos(q2)*sin(q1), - a2*q1_t*cos(q2)*sin(q1) - a2*q2_t*cos(q1)*sin(q2), q3_t*cos(q1)*(L*sin(q3) + a3*cos(q3)) + q1_t*sin(q1)*(L*cos(q3) - a3*sin(q3));
    q3_t*cos(q1)*(L*cos(q3) - a3*sin(q3)) + q1_t*sin(q1)*(a1 - L*sin(q3) - a3*cos(q3) + a2*sin(q2)) - a2*q2_t*cos(q1)*cos(q2),   a2*q2_t*sin(q1)*sin(q2) - a2*q1_t*cos(q1)*cos(q2), q1_t*cos(q1)*(L*cos(q3) - a3*sin(q3)) - q3_t*sin(q1)*(L*sin(q3) + a3*cos(q3));
                                                                                                                            0,                                    -a2*q2_t*cos(q2),                                                -q3_t*(L*cos(q3) - a3*sin(q3));
];

% Velocity
p_t = J*q_t;

% Acceleration
p_tt = J_t*q_t + J*q_tt;

end

