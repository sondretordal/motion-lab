close all
clear all
clc

% Load data from mss file
load('supply_mss.mat')

% Prepare non linear state space model matrices
supply.M = vessel.MRB + vessel.A(:,:,end);
supply.Minv = inv(supply.M);
supply.D = vessel.B(:,:,end) + vessel.Bv;
supply.G = vessel.C(:,:,end);

save('supply.mat', 'supply')

% Estimate 1st order systesm from step data using LS
load('step.mat')

[Kss, tau] = ModelEstimate(step.surge, true);
step.surge.Kss = Kss;
step.surge.tau = tau;

[Kss, tau] = ModelEstimate(step.sway, true);
step.sway.Kss = Kss;
step.sway.tau = tau;

[Kss, tau] = ModelEstimate(step.yaw, true);
step.yaw.Kss = Kss;
step.yaw.tau = tau;

save('step.mat', 'step')








