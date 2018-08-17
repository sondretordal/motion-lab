function qAvg = QuatAvgMarkley(q)


% Markley, F. Landis, Yang Cheng, John Lucas Crassidis, and Yaakov Oshman. 
% "Averaging quaternions." Journal of Guidance, Control, and Dynamics 30, 
% no. 4 (2007): 1193-1197.

% Form the symmetric accumulator matrix
A = zeros(4,4);
M = size(q,1);
wSum = 0;

for i=1:M
    w_i = 1;
    A = w_i.*(q(i,:)'*q(i,:)) + A; % rank 1 update
    wSum = wSum + w_i;
end

% scale
A = (1.0/wSum)*A;

% Get the eigenvector corresponding to largest eigen value
[qAvg,~] = eigs(A,1);

% Transpose to match matlab functios
qAvg = qAvg';
end