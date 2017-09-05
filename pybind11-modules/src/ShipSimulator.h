#pragma once
#include <iostream>
#include <iterator>
#include <cstdlib>

#include <chrono>
#include <ctime>
#include <random>
#include <thread>
#include <mutex>

#include <Eigen/Dense>

// Eigen typedefs
typedef Eigen::Matrix<double, 24, 1> StateVector;

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
    Eigen::Matrix<double, 6, 1> K;
    Eigen::Matrix<double, 2, 2> A;
    Eigen::Matrix<double, 2, 1> B;
    Eigen::Matrix<double, 1, 2> C;

    // Time constant from step response
    double Ts_x, Ts_y, Ts_yaw;
    double K_x, K_y, K_yaw;

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

    // RT simulation run function
    void run();
    void convert_states();

    

public:

    double drand() {
        return static_cast<double>(rand())/static_cast<double>(RAND_MAX);
    }

    // Constructor and destructor
    ShipSimulator();
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

    // PD controller pole placement
    double poles = 0.3;

    void integrate();
    void start();
    void close();
};