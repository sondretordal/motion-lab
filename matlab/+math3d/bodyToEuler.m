function [eta_t, eta_tt] = bodyToEuler(eta, v, v_t, angleSequence)

% Velocity
J = velocityJacobian(eta, angleSequence);
eta_t = J*v;

% Accelareation
J_t = accelerationJacobian(eta, eta_t, angleSequence);
eta_tt = J_t*v + J*v_t;

end

function J = velocityJacobian(eta, sequence)
    phi = eta(4);
    theta = eta(5);
    psi = eta(6);

    if strcmp(sequence, 'xyz')
        J = [
            1, 0, 0,                                 0,                                0, 0
            0, 1, 0,                                 0,                                0, 0
            0, 0, 1,                                 0,                                0, 0
            0, 0, 0,               cos(psi)/cos(theta),             -sin(psi)/cos(theta), 0
            0, 0, 0,                          sin(psi),                         cos(psi), 0
            0, 0, 0, -(cos(psi)*sin(theta))/cos(theta), (sin(psi)*sin(theta))/cos(theta), 1
        ];
        
    elseif strcmp(sequence, 'zyx')
        J = [ 
            1, 0, 0, 0,                                0,                                0
            0, 1, 0, 0,                                0,                                0
            0, 0, 1, 0,                                0,                                0
            0, 0, 0, 1, (sin(phi)*sin(theta))/cos(theta), (cos(phi)*sin(theta))/cos(theta)
            0, 0, 0, 0,                         cos(phi),                        -sin(phi)
            0, 0, 0, 0,              sin(phi)/cos(theta),              cos(phi)/cos(theta)
        ];

    end
end

function J_t = accelerationJacobian(eta, eta_t, sequence)
    phi = eta(4);
    theta = eta(5);
    psi = eta(6);
    
    phi_t = eta_t(4);
    theta_t = eta_t(5);
    psi_t = eta_t(6);

    if strcmp(sequence, 'xyz')
        J_t = [
            0, 0, 0,                                                                       0,                                                                       0, 0
            0, 0, 0,                                                                       0,                                                                       0, 0
            0, 0, 0,                                                                       0,                                                                       0, 0
            0, 0, 0,  (cos(psi)*sin(theta)*theta_t - cos(theta)*sin(psi)*psi_t)/cos(theta)^2, -(cos(theta)*cos(psi)*psi_t + sin(theta)*sin(psi)*theta_t)/cos(theta)^2, 0
            0, 0, 0,                                                          cos(psi)*psi_t,                                                         -sin(psi)*psi_t, 0
            0, 0, 0, -(cos(psi)*theta_t - cos(theta)*sin(theta)*sin(psi)*psi_t)/cos(theta)^2,  (sin(psi)*theta_t + cos(theta)*cos(psi)*sin(theta)*psi_t)/cos(theta)^2, 0
        ];
        
    elseif strcmp(sequence, 'zyx')
        J_t = [
            0, 0, 0, 0,                                                                      0,                                                                       0
            0, 0, 0, 0,                                                                      0,                                                                       0
            0, 0, 0, 0,                                                                      0,                                                                       0
            0, 0, 0, 0, (sin(phi)*theta_t + cos(phi)*cos(theta)*sin(theta)*phi_t)/cos(theta)^2,  (cos(phi)*theta_t - cos(theta)*sin(phi)*sin(theta)*phi_t)/cos(theta)^2
            0, 0, 0, 0,                                                        -sin(phi)*phi_t,                                                         -cos(phi)*phi_t
            0, 0, 0, 0, (cos(phi)*cos(theta)*phi_t + sin(phi)*sin(theta)*theta_t)/cos(theta)^2, -(cos(theta)*sin(phi)*phi_t - cos(phi)*sin(theta)*theta_t)/cos(theta)^2
        ];
    end
end