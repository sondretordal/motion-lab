#include "ShipSimulator.h"

ShipSimulator::ShipSimulator(unsigned int seed)
: thread()
, seed(seed)
, dist(mean, stddev)
, generator(seed) 
{
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
    states = Eigen::VectorXd::Zero(36, 1);

    // Calculate inverse mass matrix
    Minv = M.inverse();

    // Define default wave spectrum
    // wavespectrum(Hs=8.0, T1=12.0, spec='JONSWAP')
    w0 =  0.43567172549;
    Lambda =  0.101904641875;
    sigma =  5.3310138243;
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

void ShipSimulator::convert_states() {
    // Write states to variables
    x = states(0);
    y = states(1);
    z = states(2);
    roll = states(3);
    pitch = states(4);
    yaw = states(5);

    u = states(6);
    v = states(7);
    w = states(8);
    p = states(9);
    q = states(10);
    r = states(11);
}


void ShipSimulator::run() {
    // Start time
    t0 = clock::now();

    
    while (running) {
        // Integrate solution
        integrate();
        
        // Update time
        t1 = clock::now();
        elapsed = t1 - t0;

        // Update states
        mutex.lock();
            t = elapsed.count();
            convert_states();        
        mutex.unlock();

        // Sleep loop
        std::this_thread::sleep_for(std::chrono::milliseconds(static_cast<unsigned int>(dt*1000.0)));
    }
}

void ShipSimulator::integrate() {
    // Apply numerical integration using RK4 solver
    StateVector k1, k2, k3, k4;
    
    k1 = ode(t, states);
    k2 = ode(t + dt/2, states + dt/2*k1);
    k3 = ode(t + dt/2, states + dt/2*k2);
    k4 = ode(t + dt, states + dt*k3);
    
    states = states + dt/6*(k1 + 2*k2 + 2*k3 + k4);

    if (!running) {
        t = t + dt;
        convert_states();
    }
}

StateVector ShipSimulator::ode(double t, StateVector y) {
    StateVector y_t;
    Eigen::Matrix<double, 12, 1> x, x_t;
    Eigen::Matrix<double, 6, 1> eta, eta_t;
    Eigen::Matrix<double, 6, 1> v, v_t;
    Eigen::Matrix<double, 6, 1> tau, tau_wave, K;
    Eigen::Matrix<double, 6, 1> d, d_t, d_tt, r, e, e_t;

    // Fill x_t with zeros to define size
    x_t = Eigen::MatrixXd::Zero(12, 1);
    
    // Fill tau and tau_wave with zeros
    tau = Eigen::MatrixXd::Zero(6, 1);
    tau_wave = Eigen::MatrixXd::Zero(6, 1);

    // Convert vectorized states to local state vectors
    eta = y.block<6, 1>(0, 0);
    v = y.block<6, 1>(6, 0);
    x = y.block<12, 1>(12, 0);
    d = y.block<6, 1>(24, 0);
    d_t = y.block<6, 1>(30, 0);

    // Calcualate wave spectrum
    A(0, 1) = 1.0;
    A(1, 0) = -w0*w0;
    A(1, 1) = -2.0*abs(Lambda*w0);
    B(1, 0) = 2.0*abs(Lambda*w0*sigma);
    C(0, 1) = 1.0;

    // Assing wave gains
    K(0, 0) = 1e5;
    K(1, 0) = 1e5;
    K(2, 0) = 2.5e8;
    K(3, 0) = 4e7;
    K(4, 0) = 1e5;
    K(5, 0) = 1e5;
    

    // Simualte wave forces acting on the ship
    for (int dof = 0; dof < tau_wave.rows(); dof++) {
        tau_wave(dof, 0) = K(dof, 0)*C*x.block<2, 1>(dof*2, 0);
        x_t.block<2, 1>(dof*2, 0) = A*x.block<2, 1>(dof*2, 0) + B*dist(generator);
    }
    
    // Apply rigid ship body kienamtics
    eta_t = Jphi(eta.block<3, 1>(3, 0))*v;

    // Generate desired trajectory
    r = Eigen::MatrixXd::Zero(6, 1);
    r(0, 0) = x_d;
    r(1, 0) = y_d;
    r(5, 0) = yaw_d;
    d_tt = -abs(2*zeta*omega)*d_t - omega*omega*d + omega*omega*r;

    // PD controller fro surge, sway and heave
    e(0, 0) = d(0, 0) - eta(0, 0);
    e(1, 0) = d(1, 0) - eta(1, 0);
    e(2, 0) = d(2, 0) - eta(5, 0);
    e_t(0, 0) =  d_t(0, 0) - eta_t(0, 0);
    e_t(1, 0) =  d_t(1, 0) - eta_t(1, 0);
    e_t(2, 0) =  d_t(2, 0) - eta_t(5, 0);

    tau(0, 0) = Kp*e(0, 0) + Kd*e_t(0, 0);
    tau(1, 0) = Kp*e(1, 0) + Kd*e_t(1, 0);
    tau(5, 0) = Kp*e(2, 0) + Kd*e_t(2, 0);

    // System of ODEs for ship
    v_t = Minv*(-D*v - G*eta + tau + tau_wave);

    // Return system of 1. order ODEs
    y_t.block<6, 1>(0, 0) = eta_t;
    y_t.block<6, 1>(6, 0) = v_t;
    y_t.block<12, 1>(12, 0) = x_t;
    y_t.block<6, 1>(24, 0) = d_t;
    y_t.block<6, 1>(30, 0) = d_tt;

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

