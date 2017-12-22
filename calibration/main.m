close all
clear all
clc

% Static calibration data
calib = staticData();

% EM8000 -> AT960
text = fileread('./data/at960_em8000.json');
data = jsondecode(text);
N = length(data.feedback.t);

AT960 = zeros(4,4,N);
EM8000 = zeros(4,4,N);
for i = 1:N
    % AT960
    AT960(1:3,1:3,i) = math3d.Rq([
        data.feedback.at960.q0(i)
        data.feedback.at960.q1(i)
        data.feedback.at960.q2(i)
        data.feedback.at960.q3(i)
    ]);

    AT960(1:3,4,i) = [
        data.feedback.at960.x(i)
        data.feedback.at960.y(i)
        data.feedback.at960.z(i)
    ];
    
    AT960(4,4,i) = 1;
    
    % EM8000
    EM8000(1:3,1:3,i) = math3d.Rxyz([
        data.feedback.em8000.phi(i)
        data.feedback.em8000.theta(i)
        data.feedback.em8000.psi(i)
    ]);

    EM8000(1:3,4,i) = [
        data.feedback.em8000.surge(i)
        data.feedback.em8000.sway(i)
        data.feedback.em8000.heave(i)
    ];
    
    EM8000(4,4,i) = 1;
end

% Stack A nd B matrices
A = zeros(4,4,N-1);
B = zeros(4,4,N-1);
for i = 2:N
    A(:,:,i-1) = inv(EM8000(:,:,i-1))*EM8000(:,:,i);
    B(:,:,i-1) = AT960(:,:,i-1)*inv(AT960(:,:,i));
end

% Solve hand eye calibration problem
X1 = calibration.HandEyeParkMartin(A, B);

calib.EM8000_TO_AT960.quat = rotm2quat(X1(1:3,1:3))';
calib.EM8000_TO_AT960.pos = X1(1:3,4);

% EM1500 -> TMAC
clear A B AT960 data

text = fileread('./data/tmac_em1500.json');
data = jsondecode(text);
N = length(data.feedback.t);

AT960 = zeros(4,4,N);
EM1500 = zeros(4,4,N);
EM8000 = zeros(4,4,N);
for i = 1:N
    % AT960
    AT960(1:3,1:3,i) = math3d.Rq([
        data.feedback.at960.q0(i)
        data.feedback.at960.q1(i)
        data.feedback.at960.q2(i)
        data.feedback.at960.q3(i)
    ]);

    AT960(1:3,4,i) = [
        data.feedback.at960.x(i)
        data.feedback.at960.y(i)
        data.feedback.at960.z(i)
    ];
    
    AT960(4,4,i) = 1;
    
    % EM1500
    EM1500(1:3,1:3,i) = math3d.Rxyz([
        data.feedback.em1500.phi(i)
        data.feedback.em1500.theta(i)
        data.feedback.em1500.psi(i)
    ]);

    EM1500(1:3,4,i) = [
        data.feedback.em1500.surge(i)
        data.feedback.em1500.sway(i)
        data.feedback.em1500.heave(i)
    ];
    
    EM1500(4,4,i) = 1;
    
    % EM8000
    EM8000(1:3,1:3,i) = math3d.Rxyz([
        data.feedback.em8000.phi(i)
        data.feedback.em8000.theta(i)
        data.feedback.em8000.psi(i)
    ]);

    EM8000(1:3,4,i) = [
        data.feedback.em8000.surge(i)
        data.feedback.em8000.sway(i)
        data.feedback.em8000.heave(i)
    ];
    
    EM8000(4,4,i) = 1;

end

% Stack A nd B matrices
A = zeros(4,4,N-1);
B = zeros(4,4,N-1);

for i = 2:N
    A(:,:,i-1) = inv(EM1500(:,:,i-1))*EM1500(:,:,i);
    B(:,:,i-1) = inv(AT960(:,:,i-1))*AT960(:,:,i);
end

% Solve hand eye calibration problem
X2 = calibration.HandEyeParkMartin(A, B);

calib.EM1500_TO_TMAC.quat = rotm2quat(X2(1:3,1:3))';
calib.EM1500_TO_TMAC.pos = X2(1:3,4);

% Solve X1 from using EM1500 calibration data set
X = zeros(4,4,N);
for i = 1:N
    T01 = eye(4);
    T01(1:3,1:3) = math3d.Rq(calib.WORLD_TO_EM8000.quat);
    T01(1:3,4) = calib.WORLD_TO_EM8000.pos;
    
    T02 = eye(4);
    T02(1:3,1:3) = math3d.Rq(calib.WORLD_TO_EM1500.quat);
    T02(1:3,4) = calib.WORLD_TO_EM1500.pos;
    
    
    X(:,:,i) = inv(T01*EM8000(:,:,i))*T02*EM1500(:,:,i)*X2*inv(AT960(:,:,i));
end

calib = addHomogenousMatrix(calib);

function calib = addHomogenousMatrix(calib)
    
    H = eye(4);
    
    fields = fieldnames(calib);
    for i = 1:length(fields)
        
        field = getfield(calib, fields{i});
        
        H(1:3,4) = field.pos;
        
        
        q = field.quat'/norm(field.quat);
        H(1:3,1:3) = quat2rotm(q);
        
        field = setfield(field, 'H', H);
        
        calib = setfield(calib, fields{i}, field);
        
    end
end


function calib = staticData()

    % WORLD -> EM8000
    calib.WORLD_TO_EM8000.quat = [
        0.000060198987883
        0.705931944115000
        0.708279565403954
        0.000379322138596
    ];

    calib.WORLD_TO_EM8000.pos = [
        -2.969661622702265
        1.976311036084776
        2.662845015592614
    ];

    

    % WORLD -> EM1500
    calib.WORLD_TO_EM1500.quat = [
        0.000269356973877
        -0.708291543794578
        -0.705919386042796
        -0.000914792257884
    ];

    calib.WORLD_TO_EM1500.pos = [
        0.391038069269004
        -1.780959676838664
        1.689612471594921
    ];

    % EM8000 -> EM1500
    calib.EM8000_TO_EM1500.quat = [
        0.999994233253677
        -0.000147371685366
        0.000610386086891
        0.003337539483092
    ];

    calib.EM8000_TO_EM1500.pos = [
        -3.768845951221771
        3.347601117953204
        0.973619107013598
    ];

    % EM8000 -> COMAU
    calib.EM8000_TO_COMAU.quat = [
        0.002461288106714
        -0.501408337431486
        -0.865206982556575
        0.000706081011787
    ];

    calib.EM8000_TO_COMAU.pos = [
        -1.082024099747949
         1.536041691521612
        -1.024461448780775
    ];

    % EM8000 -> MRU1
    calib.EM8000_TO_MRU1.quat = [
        1.0
        0.0
        0.0
        0.0
    ];

    calib.EM8000_TO_MRU1.pos = [
        -1.289
        0.576
        -0.966
    ];

    % EM1500 -> MRU2
    calib.EM1500_TO_MRU1.quat = [
        1.0
        0.0
        0.0
        0.0
    ];

    calib.EM1500_TO_MRU1.pos = [
        0.513
        0.000
        -0.169
    ];

end

