function l_tt = ode(l_ref, l, l_t, omega, zeta)

% ODE
l_tt = l_ref*omega^2 - 2*zeta*omega*l_t - omega^2*l;

end