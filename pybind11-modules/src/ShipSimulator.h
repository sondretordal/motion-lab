#pragma once
#include <iostream>
#include <iterator>
#include <chrono>
#include <random>

#include <Eigen/Dense>

class ShipSimulator
{
private:
    // Linearized model matrices
    Eigen::MatrixXd M = Eigen::MatrixXd::Zero(6, 6);
    Eigen::MatrixXd D = Eigen::MatrixXd::Zero(6, 6);
    Eigen::MatrixXd G = Eigen::MatrixXd::Zero(6, 6);

    // Inverse mass matrix
    Eigen::MatrixXd Minv = Eigen::MatrixXd::Zero(6, 6);

    // Simulation time step
    const double dt = 10.0/1000.0;
    
    // Kinematic functions
    Eigen::Matrix3d Rx(double x);
    Eigen::Matrix3d Ry(double x);
    Eigen::Matrix3d Rz(double x);
    Eigen::Matrix3d Rnb(Eigen::Vector3d phi);
    Eigen::Matrix3d Tphi(Eigen::Vector3d phi);
    Eigen::MatrixXd Jphi(Eigen::Vector3d phi);

    // Temp data for Runge Kutta 4 solver
    Eigen::VectorXd k1;
    Eigen::VectorXd k2;
    Eigen::VectorXd k3;
    Eigen::VectorXd k4;

    // Zero mean gaussian noise
    const double mean = 0.0;
    const double stddev = 1.0;
    std::default_random_engine generator;
    std::normal_distribution<double> dist;

    // Simulation state vector
    Eigen::VectorXd states = Eigen::VectorXd::Zero(24, 1);

public:
    // Constructor and destructor
    ShipSimulator();
    ~ShipSimulator();

    // Simulation results
    double t = 0.0;
    
    double x = 0.0;
    double y = 0.0;
    double z = 0.0;
    double roll = 0.0;
    double pitch = 0.0;
    double yaw = 0.0;

    double u = 0.0;
    double v = 0.0;
    double w = 0.0;
    double p = 0.0;
    double q = 0.0;
    double r = 0.0;

    Eigen::VectorXd ode_fun(double t, Eigen::VectorXd y);

    void simulate();
};