function X = HandEyeParkMartin(A,B)
% Solve Hand-Eye Calibration Problem
% AX = XB
%
% A	: Measurements of all A - size(4,4,N)  
% B	: Measurements of all B - size(4,4,N)  
%
% Robot Sensor Calibration: Solving AX = XB on the Euclidean Group 
% http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=326576

sz = size(A);
N = sz(1,3);

% Find rotation matrix Rx
M = zeros(3,3);
X = eye(4,4);
for i = 1:N
    Ra = A(1:3,1:3,i);
    Rb = B(1:3,1:3,i);
    
    % Stack data in M matrix
%     M = M + LogR(Rb)'*LogR(Ra);
    M = M + LogR(Rb)*LogR(Ra)';
end

% Solve for rotation matric Rx
Rx = InvSqrt(M'*M)*M';

% Find translation vector using LS
C = zeros(3*N,3);
d = zeros(3*N,1);
for i = 0:N-1
    Ra = A(1:3,1:3,i+1);
    ta = A(1:3,4,i+1);
    tb = B(1:3,4,i+1);
    
    % Stack data in LS problem matrices
    C(i*3+1:i*3+3,:) = eye(3,3) - Ra;
    d(i*3+1:i*3+3,1) = ta - Rx*tb;
end

% Solve LS problem
fprintf('Matrix inversion condition: %f \n', cond(C'*C))



t = inv(C'*C)*C'*d;

% Return solution for X
X(1:3,1:3) = Rx;
X(1:3,4) = t;

end

function ret = LogR(R)
    % Calculate the logarithm of a matrix
    theta = acos((R(1,1) + R(2,2) + R(3,3) - 1.0)/2.0);
    ret = [R(3,2) - R(2,3), R(1,3) - R(3,1), R(2,1) - R(1,2)]'*(theta/(2*sin(theta)));

    if ~(abs(theta) < pi)
    % Error message
        disp('ERROR !!')
    end
end

function ret = InvSqrt(A)
    % Calculate the inverted square root of a matrix
    [V,D] = eig(A);

    ret = V*D^(-1/2)*inv(V);
    
end






