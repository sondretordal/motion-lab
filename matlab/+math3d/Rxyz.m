function R = Rxyz(phi)

rx = phi(1);
ry = phi(2);
rz = phi(3);

R = [
                              cos(ry)*cos(rz),                          -cos(ry)*sin(rz),          sin(ry);
    cos(rx)*sin(rz) + cos(rz)*sin(rx)*sin(ry), cos(rx)*cos(rz) - sin(rx)*sin(ry)*sin(rz), -cos(ry)*sin(rx);
    sin(rx)*sin(rz) - cos(rx)*cos(rz)*sin(ry), cos(rz)*sin(rx) + cos(rx)*sin(ry)*sin(rz),  cos(rx)*cos(ry)
];

end