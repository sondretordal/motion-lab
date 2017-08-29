#pragma once
#include <iostream>
#include <iterator>
#include <chrono>
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
    Eigen::MatrixXd M = Eigen::MatrixXd::Zero(6, 6);
    Eigen::MatrixXd D = Eigen::MatrixXd::Zero(6, 6);
    Eigen::MatrixXd G = Eigen::MatrixXd::Zero(6, 6);

    // Inverse mass matrix
    Eigen::MatrixXd Minv = Eigen::MatrixXd::Zero(6, 6);

    // Simulation time step
    const double dt = 5.0/1000.0;
    typedef std::chrono::high_resolution_clock time;
    typedef std::chrono::milliseconds milliseconds;
    typedef std::chrono::duration<float> duration;
    duration elapsed;
    milliseconds dt_ms;
    
    // Kinematic functions
    Eigen::Matrix3d Rx(double x);
    Eigen::Matrix3d Ry(double x);
    Eigen::Matrix3d Rz(double x);
    Eigen::Matrix3d Rnb(Eigen::Vector3d phi);
    Eigen::Matrix3d Tphi(Eigen::Vector3d phi);
    Eigen::MatrixXd Jphi(Eigen::Vector3d phi);

    // System of ODEs function
    Eigen::VectorXd ode(double t, Eigen::VectorXd y);

    // Execute simulation for one time step dt
    void run();

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

    void start() {
        running = true;
        thread = std::thread(&ShipSimulator::run, this);
    }

    void close() {
        running = false;
        if (thread.joinable()) {
            thread.join();
            std::cout << "Thread joined sucessfully!" << std::endl;
        }
    }
};