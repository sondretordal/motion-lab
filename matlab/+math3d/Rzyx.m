function R = Rzyx(phi)

rx = phi(1);
ry = phi(2);
rz = phi(3);

R = [
    cos(ry)*cos(rz), cos(rz)*sin(rx)*sin(ry) - cos(rx)*sin(rz), sin(rx)*sin(rz) + cos(rx)*cos(rz)*sin(ry);
    cos(ry)*sin(rz), cos(rx)*cos(rz) + sin(rx)*sin(ry)*sin(rz), cos(rx)*sin(ry)*sin(rz) - cos(rz)*sin(rx);
           -sin(ry),                           cos(ry)*sin(rx),                           cos(rx)*cos(ry)
];