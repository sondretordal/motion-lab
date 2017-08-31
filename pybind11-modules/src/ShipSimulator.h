#pragma once
#include <iostream>
#include <iterator>

#include <chrono>
#include <ctime>
#include <random>
#include <thread>
#include <mutex>

#include <Eigen/Dense>

// Eigen typedefs
typedef Eigen::Matrix<double, 36, 1> StateVector;

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

    // Inverse mass matrix1
    Eigen::Matrix<double, 6, 6> Minv;

    // Linearized wave force model
    Eigen::Matrix<double, 2, 2> A = Eigen::MatrixXd::Zero(2, 2);
    Eigen::Matrix<double, 2, 1> B = Eigen::MatrixXd::Zero(2, 1);
    Eigen::Matrix<double, 1, 2> C = Eigen::MatrixXd::Zero(1, 2);

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
    StateVector ode(double t, StateVector y);

    // Simulation state vector
    StateVector states;

    // Zero mean gaussian noise
    const double mean = 0.0;
    const double stddev = 1.0;
    const unsigned int seed;    
    std::default_random_engine generator;
    std::normal_distribution<double> dist;

    // RT simulation run function
    void run();
    void convert_states();

public:
    // Constructor and destructor
    ShipSimulator(unsigned int seed);
    ~ShipSimulator();

    // Linearized wave parameters
    double w0;
    double Lambda;
    double sigma;

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

    // DP inputs
    double Kp = 0.0;
    double Kd = 0.0;
    double zeta = 0.7;
    double omega = 0.1*2.0*M_PI;
    double x_d = 0.0;
    double y_d = 0.0;
    double yaw_d = 0.0;

    void integrate();
    void start();
    void close();
};