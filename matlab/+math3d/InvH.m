function invH = InvH(H)
% Reverse homgoenous rigid motions
% More efficient than using inv(H)
% 
% INPUTS:
% H         : Homogeneus transformation matrix 4x4
% 
% OUT:
% invH      : Reversed rigid motion matrix 4x4


R = H(1:3,1:3);
d = H(1:3,4);

invH = eye(4,4);

invH(1:3,1:3) = R';
invH(1:3,4) = -R'*d;

invH(4,1:4) = [0,0,0,1];

end

