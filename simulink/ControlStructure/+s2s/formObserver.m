function formObserver()

% ** Calibratoin data **
data = load('+motionlab/calib.mat');

% Ship 1 states
eta1 = sym('eta1', [6,1], 'real');
v1 = sym('v1', [6,1], 'real');
v1_t = sym('v1_t', [6,1], 'real');

% Ship 2 states
eta2 = sym('eta2', [6,1], 'real');
v2 = sym('v2', [6,1], 'real');
v2_t = sym('v2_t', [6,1], 'real');

% Offset states
syms dx dy dz dpsi 'real'

% Vectorize states
x1 = [
    eta1
    v1
    v1_t
];

x2 = [
    eta2
    v2
    v2_t
];

x3 = [
    dx
    dy
    dz
    dpsi
];

% Augumented state vector
x = [x1; x2; x3];

% Sampling time
syms Ts 'real'

% Discretized SS model using forward euler
f1 = x1 + s2s.shipOde(x1)*Ts;
f2 = x2 + s2s.shipOde(x2)*Ts;
f3 = x3 + s2s.offsetOde(x3)*Ts;

% Augument discrete SS model
f = [f1; f2; f3];

% State transition jacobian
fJacobian = jacobian(f, x);

% Save as matlab functions            
matlabFunction(f, 'File', '+s2s/+observer/f.m', 'Vars', {x, Ts});
matlabFunction(fJacobian, 'File', '+s2s/+observer/fJacobian.m', 'Vars', {x, Ts});

% Measurement Model
hMruOne = [
    eta1
    v1
];

hMruTwo = [
    eta2
    v2
];

% Measured rotation matrix
rL = sym('rL', [3,1], 'real');
qL = sym('qL', [1,4], 'real');

rP = sym('rP', [3,1], 'real');
qP = sym('qP', [1,4], 'real');

RLP = (math3d.Rxyz(eta1(4:6))*math3d.Rq(qL))'*...
                math3d.Rz(x3(4))*math3d.Rxyz(eta2(4:6))*math3d.Rq(qP);

RLP = simplify(RLP);

hLeica = [
    % Position
    (math3d.Rxyz(eta1(4:6))*math3d.Rq(qL))'*(x3(1:3) + ...
    math3d.Rz(x3(4))*(eta2(1:3) + math3d.Rxyz(eta2(4:6))*rP) - ...
    (eta1(1:3) + math3d.Rxyz(eta1(4:6))*rL))
    % Oriantation
    RLP(1,1)
    RLP(1,2)
    RLP(1,3)
    RLP(2,1)
    RLP(2,2)
    RLP(2,3)
    RLP(3,1)
    RLP(3,2)
    RLP(3,3)
];

% Measurement Jacobians
hMruOneJacobian = jacobian(hMruOne, x);
hMruTwoJacobian = jacobian(hMruTwo, x);
hLeicaJacobian = jacobian(hLeica, x);

% Save as matlab functions
matlabFunction(hMruOne, 'File', '+s2s/+observer/hMruOne', 'Vars', {x});
matlabFunction(hMruOneJacobian, 'File', '+s2s/+observer/hMruOneJacobian', 'Vars', {x});

matlabFunction(hMruTwo, 'File', '+s2s/+observer/hMruTwo', 'Vars', {x});
matlabFunction(hMruTwoJacobian, 'File', '+s2s/+observer/hMruTwoJacobian', 'Vars', {x});

matlabFunction(hLeica, 'File', '+s2s/+observer/hLeica', 'Vars', {x, rL, qL, rP, qP});
matlabFunction(hLeicaJacobian, 'File', '+s2s/+observer/hLeicaJacobian', 'Vars', {x, rL, qL, rP, qP});


end