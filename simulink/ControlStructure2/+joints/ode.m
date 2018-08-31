function q_tt = ode(q_ref, q, q_t, omega, zeta)

% ODE
q_tt = q_ref*omega^2 - 2*zeta*omega*q_t - omega^2*q;

end