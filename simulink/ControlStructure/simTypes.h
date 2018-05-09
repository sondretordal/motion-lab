typedef struct {
    double phi[2];
    double phi_t[2];
    double phi_tt[2];
    double c;
} PendulumStates;

typedef struct {
    double l;
    double l_t;
    double l_tt;
    double l_ref;
    double Kdc;
    double omega;
    double zeta;
} WinchStates;

typedef struct {
    double p[3];
    double p_t[3];
    double p_tt[3];
} ComauToolPoint;