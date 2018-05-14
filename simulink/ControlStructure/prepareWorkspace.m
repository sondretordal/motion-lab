close all
clear all
clc

% Create simulink buses
importPlc = Simulink.importExternalCTypes('plcTypes.h');

% Fundamnetal simulation time step
Ts = 0.005;

% Measured distance form {b2} origo to top plate of EM1500
dz = -0.3;

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
ekfPendel = pendel.observer.formParameters();













