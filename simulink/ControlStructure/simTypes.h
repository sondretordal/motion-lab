//#include <plcTypes.h>



typedef struct {
    // Parameters
    double c;
    // Angle feedback
    double phi[2];
    double phi_t[2];
    double phi_tt[2];
} SimPendulum;

typedef struct {
    // Parameters
    double Kdc;
    double omega;
    double zeta;
    // Control input
    double l_ref;
    // Wire Length Feedback
    double l;
    double l_t;
    double l_tt;
} SimWinch;

typedef struct {
    // Control input
    double q_ref[3];
    // Joint Feedback
    double q[3];
    double q_t[3];
    double q_tt[3];
    // Tool Feedback
    double p[3];
    double p_t[3];
    double p_tt[3];
} SimComau;
    