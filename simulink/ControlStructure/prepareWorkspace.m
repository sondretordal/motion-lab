close all
clear all
clc

% Fundamnetal simulation time step
Ts = 0.005;

% Measured distance form {b2} origo to top plate of EM1500
dz = -0.1690;

% Pendulum damping parameter
c = 0.5;

% Winch Dynamics
winch.omega = 4*2*pi;
winch.zeta = 0.7;

% TRobot Joint Dynamics
robot.omega = 4*2*pi;
robot.zeta = 0.7;

% Pendulum ODE 
phi_tt = pendel.formOde();

% Linearized wave spectrum
Hs = 8.0;
Tp = 12.0;
N = 100;
[S, w, dw] = hydro.PiersonMoscowitz(Hs, Tp, N, 'false');
[lambda, w0, sigma] = hydro.LinearWaveSpec(S, w, 'false');

%% Define covarince from experimental data
load('experiement.mat')

% Stewart simulator covarinces
sim = simulation.formCovariances(data, 'none');

% Form observers
pendelEkf = pendel.formEkfMatrices();
s2sEkf = s2s.formEkfMatrices();

%% *** Create Simulink Bus Objects ***
% Feedback Types
ST_StewartFeedback = bus.StewartFeedback();
ST_MruFeedback = bus.MruFeedback();
ST_ComauFeedback = bus.ComauFeedback();
ST_WinchFeedback = bus.WinchFeedback();
ST_QualisysFeedback = bus.QualisysFeedback();
ST_LeicaFeedback = bus.LeicaFeedback();

% Feedback Bus
clear elems
n = 1;
elems(n) = Simulink.BusElement;
elems(n).Name = 'em8000';
elems(n).DataType = 'ST_StewartFeedback';

n = 2;
elems(n) = Simulink.BusElement;
elems(n).Name = 'em1500';
elems(n).DataType = 'ST_StewartFeedback';

n = 3;
elems(n) = Simulink.BusElement;
elems(n).Name = 'mru1';
elems(n).DataType = 'ST_MruFeedback';

n = 4;
elems(n) = Simulink.BusElement;
elems(n).Name = 'mru2';
elems(n).DataType = 'ST_MruFeedback';

n = 5;
elems(n) = Simulink.BusElement;
elems(n).Name = 'comau';
elems(n).DataType = 'ST_ComauFeedback';

n = 6;
elems(n) = Simulink.BusElement;
elems(n).Name = 'winch';
elems(n).DataType = 'ST_WinchFeedback';

n = 7;
elems(n) = Simulink.BusElement;
elems(n).Name = 'qtm';
elems(n).DataType = 'ST_QualisysFeedback';

n = 8;
elems(n) = Simulink.BusElement;
elems(n).Name = 'at960';
elems(n).DataType = 'ST_LeicaFeedback';

ST_Feedback = Simulink.Bus;
ST_Feedback.Elements = elems;


% Control Types
ST_StewartControl = bus.StewartControl();
ST_WinchControl = bus.WinchControl();
ST_ComauControl = bus.ComauControl();

% Control Bus
clear elems
n = 1;
elems(n) = Simulink.BusElement;
elems(n).Name = 'em8000';
elems(n).DataType = 'ST_StewartControl';

n = 2;
elems(n) = Simulink.BusElement;
elems(n).Name = 'em1500';
elems(n).DataType = 'ST_StewartControl';

n = 3;
elems(n) = Simulink.BusElement;
elems(n).Name = 'comau';
elems(n).DataType = 'ST_ComauControl';

n = 4;
elems(n) = Simulink.BusElement;
elems(n).Name = 'winch';
elems(n).DataType = 'ST_WinchControl';

ST_Control = Simulink.Bus;
ST_Control.Elements = elems;













