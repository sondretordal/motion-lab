function phi_zyx = xyz2zyx(phi_xyz)

phi = phi_xyz(1,:);
theta = phi_xyz(2,:);
psi = phi_xyz(3,:);

phi_zyx(1,:) = atan2(cos(psi).*sin(phi) + sin(psi).*sin(theta).*cos(phi), cos(theta).*cos(phi));
phi_zyx(2,:) = -asin(sin(phi).*sin(psi) - cos(phi).*cos(psi).*sin(theta));
phi_zyx(3,:) = atan2(sin(psi).*cos(phi) + cos(psi).*sin(theta).*sin(phi), cos(psi).*cos(theta));

end