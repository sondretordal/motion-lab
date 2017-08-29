#include "ShipSimulator.h"

ShipSimulator::ShipSimulator() : dist(mean, stddev), thread() {
    // Fill constant model matrices according to supply.mat form Fossen's work
    M <<  6.82e+06,   0.00e+00,   0.00e+00,   0.00e+00,  -8.27e+06,  0.00e+00,
          0.00e+00,   7.88e+06,   0.00e+00,   1.13e+07,   0.00e+00, -2.60e+06,
          0.00e+00,   0.00e+00,   1.77e+07,   0.00e+00,   4.63e+07,  0.00e+00,
          0.00e+00,   1.13e+07,   0.00e+00,   3.63e+08,   0.00e+00, -6.38e+07,
         -8.27e+06,   0.00e+00,   4.63e+07,   0.00e+00,   6.71e+09,  0.00e+00,
          0.00e+00,  -2.60e+06,   0.00e+00,  -6.38e+07,   0.00e+00,  3.57e+09;

    D <<  5.90e+05,   0.00e+00,   0.00e+00,   0.00e+00,   0.00e+00,  0.00e+00,
          0.00e+00,   1.96e+06,   0.00e+00,   1.90e+06,   0.00e+00,  5.74e+06,
          0.00e+00,   0.00e+00,   1.55e+06,   0.00e+00,   3.73e+07,  0.00e+00,
          0.00e+00,   1.90e+06,   0.00e+00,   3.54e+07,   0.00e+00, -4.75e+07,
          0.00e+00,   0.00e+00,   3.73e+07,   0.00e+00,   1.59e+09,  0.00e+00,
          0.00e+00,   5.74e+06,   0.00e+00,  -4.75e+07,   0.00e+00,  8.95e+08;

    G <<  0.00e+00,   0.00e+00,   0.00e+00,   0.00e+00,   0.00e+00,  0.00e+00,
          0.00e+00,   0.00e+00,   0.00e+00,   0.00e+00,   0.00e+00,  0.00e+00,
          0.00e+00,   0.00e+00,   1.39e+07,   0.00e+00,   7.07e+07,  0.00e+00,
          0.00e+00,   0.00e+00,   0.00e+00,   1.34e+08,   0.00e+00,  0.00e+00,
          0.00e+00,   0.00e+00,   7.07e+07,   0.00e+00,   6.47e+09,  0.00e+00,
          0.00e+00,   0.00e+00,   0.00e+00,   0.00e+00,   0.00e+00,  0.00e+00;

    // Calculate inverse mass matrix
    Minv = M.inverse();

    states(2) = 10.0;

    // Cast time step into chrono milliseconds format
    dt_ms = std::chrono::duration_cast<milliseconds>(static_cast<duration>(dt));
}

ShipSimulator::~ShipSimulator() {
    close();
}

void ShipSimulator::run() {
    // Temp data for runge kutta solver
    Eigen::VectorXd k1;
    Eigen::VectorXd k2;
    Eigen::VectorXd k3;
    Eigen::VectorXd k4;
    
    
    while (running) {
        // Start time
        auto t0 = time::now();

        // Apply numerical integration using RK4 solver
        k1 = ode(t, states);
        k2 = ode(t + dt/2, states + dt/2*k1);
        k3 = ode(t + dt/2, states + dt/2*k2);
        k4 = ode(t + dt, states + dt*k3);
        states = states + dt/6*(k1 + 2*k2 + 2*k3 + k4);

        // Assign public data
        mutex.lock();
            // Update time
            t = t + dt;
            
            // Position states
            x = states(0);
            y = states(1);
            z = states(2);
            roll = states(3);
            pitch = states(4);
            yaw = states(5);

            // Velocity states
            u = states(6);
            v = states(7);
            w = states(8);
            p = states(9);
            q = states(10);
            r = states(11);
        mutex.unlock();

        // Calculate elapsed simulation time
        auto t1 = time::now();
        elapsed = abs(t1 - t0);

        // Synchronize loop to real time
        if (elapsed < dt_ms) {   
            std::this_thread::sleep_for(dt_ms - elapsed);
        } else {
            std::cout << "Timestep violated" << std::endl;
        }
    }
}

Eigen::VectorXd ShipSimulator::ode(double t, Eigen::VectorXd y) {
    Eigen::VectorXd y_t;
    Eigen::VectorXd eta, eta_t;
    Eigen::VectorXd v, v_t;
    Eigen::VectorXd x, x_t;
    Eigen::VectorXd tau, tau_wave;
    Eigen::Vector3d phi;

    // Fill x_t with zeros to define size
    x_t = Eigen::MatrixXd::Zero(12, 1);
    
    // Fill tau and tau_wave with zeros
    tau = Eigen::MatrixXd::Zero(6, 1);
    tau_wave = Eigen::MatrixXd::Zero(6, 1);

    // Convert vectorized states to eta, v and x
    eta = y.block<6, 1>(0, 0);
    v = y.block<6, 1>(6, 0);
    x = y.block<12, 1>(12, 0);
    
    // Apply rigid ship body kienamtics
    phi = eta.block<3, 1>(3, 0);
    eta_t = Jphi(phi)*v;

    // System of ODEs for ship
    v_t = Minv*(-D*v - G*eta + tau + tau_wave);

    // Return system of 1. order ODEs
    y_t = Eigen::MatrixXd::Zero(24, 1);

    y_t.block<6, 1>(0, 0) = eta_t;
    y_t.block<6, 1>(6, 0) = v_t;
    y_t.block<12, 1>(12, 0) = x_t;

    return y_t;
}

// Kinematics functions
Eigen::Matrix3d ShipSimulator::Rx(double x) {
    Eigen::Matrix3d R;

    R <<  1,       0,       0,
          0,  cos(x), -sin(x),
          0,  sin(x),  cos(x);

    return R;
}

Eigen::Matrix3d ShipSimulator::Ry(double x) {
    Eigen::Matrix3d R;

    R <<  cos(x),  0,  sin(x),
               0,  1,       0,
         -sin(x),  0,  cos(x);

    return R;
}

Eigen::Matrix3d ShipSimulator::Rz(double x) {
    Eigen::Matrix3d R;

    R <<  cos(x), -sin(x),  0,
          sin(x),  cos(x),  0,
               0,       0,  1;

    return R;
}

Eigen::Matrix3d ShipSimulator::Rnb(Eigen::Vector3d phi) {
    Eigen::Matrix3d R;

    double rx = phi(0);
    double ry = phi(1);
    double rz = phi(2);

    R = Rz(rz)*Ry(ry)*Rx(rx);

    return R;
}

Eigen::Matrix3d ShipSimulator::Tphi(Eigen::Vector3d phi) {
    Eigen::Matrix3d T;

    double rx = phi(0);
    double ry = phi(1);

    T <<  1,  sin(rx)*tan(ry),  cos(rx)*tan(ry),
          0,          cos(rx),         -sin(rx),
          0,  sin(rx)/cos(ry),  cos(rx)/cos(ry);

    return T;
}

Eigen::MatrixXd ShipSimulator::Jphi(Eigen::Vector3d phi) {
    Eigen::MatrixXd J = Eigen::MatrixXd::Zero(6, 6);

    if (cos(phi(1)) == 0.0) {
        std::cout << "Singular for theta = +-90 degrees" << std::endl;
        exit(EXIT_FAILURE);
    } else {
        J.block<3, 3>(0, 0) = Rnb(phi);
        J.block<3, 3>(3, 3) = Tphi(phi);
    }

    return J;
}

