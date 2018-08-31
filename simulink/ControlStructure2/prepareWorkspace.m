close all
clear all
clc

% Load static data
load('hydroSupply.mat');
load('motionlab/calib.mat');

% Fundamnetal simulation time step
Ts = 0.005;

% Measured distance form {b2} origo to top plate of EM1500
dz = -0.1690;

%% Pendulum ODE 
phi_tt = pendel.form();

% Linearized wave spectrum
Hs = 8.0;
Tp = 12.0;
N = 100;
[S, w, dw] = hydro.PiersonMoscowitz(Hs, Tp, N, 'false');
[lambda, w0, sigma] = hydro.LinearWaveSpec(S, w, 'false');

%% Define covarince from experimental data
load('experiement.mat')

% Dynamic parameters
omega_q = 1*2*pi;
zeta_q = 0.7;

omega_l = 4*2*pi;
zeta_l = 0.7;

% Stewart simulator covarinces
sim = simulation.formCovariances(data, 'none');

% Form observers
[x0, Q, R, P0] = observer.ekfMatrices();
stringQ = sprintf('%d,' , diag(Q));
stringR = sprintf('%d,' , diag(R));

%% Anti-Sawy Controller Gains
K = antisway.lqr();

%% *** Create Simulink Bus Objects ***
% Feedback Types
ST_FeedbackStewart = bus.FeedbackStewart();
ST_FeedbackMru = bus.FeedbackMru();
ST_FeedbackComau = bus.FeedbackComau();
ST_FeedbackWinch = bus.FeedbackWinch();
ST_FeedbackQualisys = bus.FeedbackQualisys();
ST_FeedbackLeica = bus.FeedbackLeica();

% Feedback Bus
clear elems
n = 1;
elems(n) = Simulink.BusElement;
elems(n).Name = 'em8000';
elems(n).DataType = 'ST_FeedbackStewart';

n = 2;
elems(n) = Simulink.BusElement;
elems(n).Name = 'em1500';
elems(n).DataType = 'ST_FeedbackStewart';

n = 3;
elems(n) = Simulink.BusElement;
elems(n).Name = 'mru1';
elems(n).DataType = 'ST_FeedbackMru';

n = 4;
elems(n) = Simulink.BusElement;
elems(n).Name = 'mru2';
elems(n).DataType = 'ST_FeedbackMru';

n = 5;
elems(n) = Simulink.BusElement;
elems(n).Name = 'comau';
elems(n).DataType = 'ST_FeedbackComau';

n = 6;
elems(n) = Simulink.BusElement;
elems(n).Name = 'winch';
elems(n).DataType = 'ST_FeedbackWinch';

n = 7;
elems(n) = Simulink.BusElement;
elems(n).Name = 'qtm';
elems(n).DataType = 'ST_FeedbackQualisys';

n = 8;
elems(n) = Simulink.BusElement;
elems(n).Name = 'at960';
elems(n).DataType = 'ST_FeedbackLeica';

ST_Feedback = Simulink.Bus;
ST_Feedback.Elements = elems;

% Control Types
ST_ControlStewart = bus.ControlStewart();
ST_ControlWinch = bus.ControlWinch();
ST_ControlComau = bus.ControlComau();

% Control Bus
clear elems

n = 1;
elems(n) = Simulink.BusElement;
elems(n).Name = 'comau';
elems(n).DataType = 'ST_ControlComau';

n = 2;
elems(n) = Simulink.BusElement;
elems(n).Name = 'winch';
elems(n).DataType = 'ST_ControlWinch';

ST_Control = Simulink.Bus;
ST_Control.Elements = elems;













