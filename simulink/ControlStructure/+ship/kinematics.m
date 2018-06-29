function eta_t = kinematics(eta, v)

J = [
    eye(3), zeros(3,3);
    zeros(3,3), math3d.Tphi(eta(4:6), 'zyx')
];
    
eta_t = J*v;

end