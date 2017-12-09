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

% ---------- Tunable Parameters -------------
% Wave settings
K = [1e4,1e4,1e8,1e7,1e8,1e3];
w0 = 0.37260924763921838;
lambda = 0.10230380018702853;
sigma = 5.7537427025997498;

% Pole placement
poles = -10;

% Random generator seeds
seeds = [0,20,500,9000,400,200];





