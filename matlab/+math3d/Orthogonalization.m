function T = Orthogonalization(H)


% http://www.math.tamu.edu/~yvorobet/MATH304-2011A/Lect3-05web.pdf

T = H;

x1 = H(1:3,1);
x2 = H(1:3,2);
x3 = H(1:3,3);

% Project to orthonormal basis
v1 = x1;
w1 = v1/norm(v1);

v2 = x2 - dot(x2,w1)*w1;
w2 = v2/norm(v2);

v3 = x3 - dot(x3,w1)*w1 - dot(x3,w2)*w2;
w3 = v3/norm(v3);

% Return resulting orthogonal basis back to homogeneous matrix T
T(1:3,1) = w1;
T(1:3,2) = w2;
T(1:3,3) = w3;

