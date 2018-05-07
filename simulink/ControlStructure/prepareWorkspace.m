close all
clear all
clc

% Create simulink buses
importPlc = Simulink.importExternalCTypes('ioTypes.h');
importSim = Simulink.importExternalCTypes('simTypes.h');

% Fundamnetal simulation time step
Ts = 0.005;

% Measured length to wire exit point WEP
L = 0.567;

% Pendulum ODE 
phi_tt = pendel.formOde();

% Linearized wave spectrum
Hs = 8.0;
Tp = 12.0;
N = 100;
[S, w, dw] = hydro.PiersonMoscowitz(Hs, Tp, N,'false');
[lambda, w0, sigma] = hydro.LinearWaveSpec(S, w, 'true');

% Mru Uncertanities







