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
    Eigen::MatrixXd M = Eigen::MatrixXd::Zero(6, 6);
    Eigen::MatrixXd D = Eigen::MatrixXd::Zero(6, 6);
    Eigen::MatrixXd G = Eigen::MatrixXd::Zero(6, 6);

    // Inverse mass matrix
    Eigen::MatrixXd Minv = Eigen::MatrixXd::Zero(6, 6);

    // Linearized wave force model
    Eigen::Matrix2d A = Eigen::MatrixXd::Zero(2, 2);
    Eigen::Vector2d B = Eigen::MatrixXd::Zero(2, 1);
    Eigen::RowVector2d C = Eigen::MatrixXd::Zero(1, 2);
    Eigen::VectorXd K = Eigen::MatrixXd::Zero(6, 1);

    // Simulation time step
    const double dt = 5.0/1000.0;
    typedef std::chrono::steady_clock clock;

    std::chrono::duration<double> elapsed;
    std::chrono::time_point<std::chrono::steady_clock> t0, t1;
    std::time_t time;
    
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

    // Linearized wave parameters
    double w0 = 0.43567;
    double Lambda = 0.10190;
    double sigma = 5.33101;
    double K1 = 0.0;
    double K2 = 0.0;
    double K3 = 1.6e8;
    double K4 = 2e7;
    double K5 = 5e6;
    double K6 = 0.0;

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