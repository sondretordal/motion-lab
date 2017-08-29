#pragma once
#include <iostream>
#include <iterator>
#include <chrono>
#include <ctime>
#include <random>
#include <thread>
#include <mutex>

#include <Eigen/Dense>

class ShipSimulator
{
private:
    // Thread related
	std::thread thread;
	std::mutex mutex;
    bool running = false;

    // Linearized model matrices
    Eigen::Matrix<double, 6, 6> M;
    Eigen::Matrix<double, 6, 6> D;
    Eigen::Matrix<double, 6, 6> G;

    // Inverse mass matrix
    Eigen::Matrix<double, 6, 6> Minv;

    // Linearized wave force model
    Eigen::Matrix<double, 2, 2> A = Eigen::MatrixXd::Zero(2, 2);
    Eigen::Matrix<double, 2, 1> B = Eigen::MatrixXd::Zero(2, 1);
    Eigen::Matrix<double, 1, 2> C = Eigen::MatrixXd::Zero(1, 2);
    Eigen::Matrix<double, 6, 1> K = Eigen::MatrixXd::Zero(6, 1);

    // Simulation time step
    double dt = 5.0/1000.0;
    typedef std::chrono::steady_clock clock;
    std::chrono::time_point<std::chrono::steady_clock> t0, t1;
    std::chrono::duration<double> elapsed;

    // Kinematic functions
    Eigen::Matrix<double, 3, 3> Rx(double x);
    Eigen::Matrix<double, 3, 3> Ry(double x);
    Eigen::Matrix<double, 3, 3> Rz(double x);
    Eigen::Matrix<double, 3, 3> Rnb(Eigen::Vector3d phi);
    Eigen::Matrix<double, 3, 3> Tphi(Eigen::Vector3d phi);
    Eigen::Matrix<double, 6, 6> Jphi(Eigen::Vector3d phi);

    // System of ODEs function
    Eigen::Matrix<double, 24, 1> ode(double t, Eigen::Matrix<double, 24, 1> y);

    // Simulation state vector
    Eigen::Matrix<double, 24, 1> states;

    // Zero mean gaussian noise
    const double mean = 0.0;
    const double stddev = 1.0;
    std::default_random_engine generator;
    std::normal_distribution<double> dist;

    // Execute simulation for one time step dt
    void run();

public:
    // Constructor and destructor
    ShipSimulator();
    ~ShipSimulator();

    // Linearized wave parameters
    double w0 = 0.43567;
    double Lambda = 0.10190;
    double sigma = 5.33101;
    double K1 = 2e7;
    double K2 = 2e7;
    double K3 = 1.6e8;
    double K4 = 2e7;
    double K5 = 5e6;
    double K6 = 1e8;

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

    void start();
    void close();
};