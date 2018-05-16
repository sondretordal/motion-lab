function J = shipJacobian(eta)
    % Rigid body ship kinematics
    J = [
        eye(3), zeros(3,3);
        zeros(3,3), math3d.Tphi(eta(4:6), 'xyz')
    ];
end  