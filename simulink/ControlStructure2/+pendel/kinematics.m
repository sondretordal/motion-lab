function ph = kinematics(pt, phi, l)

% {h} given in {n}
ph = pt + [
    -l*sin(phi(1))
     l*cos(phi(1))*sin(phi(2))
     l*cos(phi(1))*cos(phi(2))
];


end

