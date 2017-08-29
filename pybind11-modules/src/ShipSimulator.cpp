#include "ShipSimulator.h"

ShipSimulator::ShipSimulator() : thread() {
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

    // Set all states to zero
    states = Eigen::VectorXd::Zero(24, 1);

    // Calculate inverse mass matrix
    Minv = M.inverse();
}

ShipSimulator::~ShipSimulator() {
    close();
}

void ShipSimulator::start() {
    running = true;
    thread = std::thread(&ShipSimulator::run, this);
}

void ShipSimulator::close()  {
    running = false;
    if (thread.joinable()) {
        thread.join();
        std::cout << "Thread joined sucessfully!" << std::endl;
    }
}

void ShipSimulator::run() {
    // Temp data for runge kutta solver
    Eigen::VectorXd k1;
    Eigen::VectorXd k2;
    Eigen::VectorXd k3;
    Eigen::VectorXd k4;
    
    // Start time
    t0 = clock::now();

    while (running) {
        // Apply numerical integration using RK4 solver
        k1 = ode(t, states);
        k2 = ode(t + dt/2, states + dt/2*k1);
        k3 = ode(t + dt/2, states + dt/2*k2);
        k4 = ode(t + dt, states + dt*k3);
        states = states + dt/6*(k1 + 2*k2 + 2*k3 + k4);

        t1 = clock::now();
        elapsed = t1 - t0;

        // Assign public data
        mutex.lock();
            // Update time
            t = elapsed.count();
            
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

        // Sleep loop
        std::this_thread::sleep_for(std::chrono::milliseconds(static_cast<unsigned int>(dt*1000.0)));
    }
}

Eigen::Matrix<double, 24, 1> ShipSimulator::ode(double t, Eigen::Matrix<double, 24, 1> y) {
    Eigen::Matrix<double, 24, 1> y_t;
    Eigen::Matrix<double, 12, 1> x, x_t;
    Eigen::Matrix<double, 6, 1> eta, eta_t, v, v_t, tau, tau_wave;
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

    // Calcualate wave spectrum
    A(0, 1) = 1.0;
    A(1, 0) = -w0*w0;
    A(1, 1) = -2.0*abs(Lambda*w0);
    B(1, 0) = 2.0*abs(Lambda*w0*sigma);
    C(0, 1) = 1.0;

    // Assing wave gains
    K[0] = K1;
    K[1] = K2;
    K[2] = K3;
    K[3] = K4;
    K[4] = K5;
    K[5] = K6;

    for (int dof = 0; dof < tau_wave.rows(); dof++) {
        tau_wave(dof, 0) = K(dof)*C*x.block<2, 1>(dof*2, 0);
        x_t.block<2, 1>(dof*2, 0) = A*x.block<2, 1>(dof*2, 0) + B*dist(generator);
    }
    
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
Eigen::Matrix<double, 3, 3> ShipSimulator::Rx(double x) {
    Eigen::Matrix<double, 3, 3> R;

    R <<  1,       0,       0,
          0,  cos(x), -sin(x),
          0,  sin(x),  cos(x);

    return R;
}

Eigen::Matrix<double, 3, 3> ShipSimulator::Ry(double x) {
    Eigen::Matrix<double, 3, 3> R;

    R <<  cos(x),  0,  sin(x),
               0,  1,       0,
         -sin(x),  0,  cos(x);

    return R;
}

Eigen::Matrix<double, 3, 3> ShipSimulator::Rz(double x) {
    Eigen::Matrix<double, 3, 3> R;

    R <<  cos(x), -sin(x),  0,
          sin(x),  cos(x),  0,
               0,       0,  1;

    return R;
}

Eigen::Matrix<double, 3, 3> ShipSimulator::Rnb(Eigen::Vector3d phi) {
    Eigen::Matrix<double, 3, 3> R;

    double rx = phi(0);
    double ry = phi(1);
    double rz = phi(2);

    R = Rz(rz)*Ry(ry)*Rx(rx);

    return R;
}

Eigen::Matrix<double, 3, 3> ShipSimulator::Tphi(Eigen::Vector3d phi) {
    Eigen::Matrix<double, 3, 3> T;

    double rx = phi(0);
    double ry = phi(1);

    T <<  1,  sin(rx)*tan(ry),  cos(rx)*tan(ry),
          0,          cos(rx),         -sin(rx),
          0,  sin(rx)/cos(ry),  cos(rx)/cos(ry);

    return T;
}

Eigen::Matrix<double, 6, 6> ShipSimulator::Jphi(Eigen::Vector3d phi) {
    Eigen::Matrix<double, 6, 6> J = Eigen::MatrixXd::Zero(6, 6);

    if (cos(phi(1)) == 0.0) {
        std::cout << "Singular for theta = +-90 degrees" << std::endl;
        exit(EXIT_FAILURE);
    } else {
        J.block<3, 3>(0, 0) = Rnb(phi);
        J.block<3, 3>(3, 3) = Tphi(phi);
    }

    return J;
}

