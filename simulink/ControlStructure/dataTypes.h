// Feedback types
typedef struct {
    double eta[6];
    double v[6];
    double v_t[6];
} StewartFeedback;

typedef struct {
    double q[3];
    double q_t[3];
    double q_tt[3];
} ComauFeedback;

// Control types
typedef struct {
    double q[3];
    double q_t[3];
    double q_tt[3];
} ComauControl;

typedef struct {
    double phi[2];
    double phi_t[2];
    double phi_tt[2];
    double l;
    double l_t;
} PendulumStates;
    