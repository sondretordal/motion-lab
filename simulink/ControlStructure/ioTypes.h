// Feedback data
typedef struct {
    // Rotation Sequence: XYZ
    double surge;
    double sway;
    double heave;
    double phi;
    double theta;
    double psi;
    double surge_t;
    double sway_t;
    double heave_t;
    double phi_t;
    double theta_t;
    double psi_t;
    double surge_tt;
    double sway_tt;
    double heave_tt;
    double phi_tt;
    double theta_tt;
    double psi_tt;
} StewartFeedback;

typedef struct {
	// Rotation Sequence: ZYX
	double surge;
	double sway;
	double heave;
	double surge_t;
	double sway_t;
	double heave_t;
	double surge_tt;
	double sway_tt;
	double heave_tt;
	double phi;
	double theta;
	double psi;
	double wx;
	double wy;
	double wz;
} MruFeedback;

typedef struct {
    double q1;
    double q2;
    double q3;
    double q1_t;
    double q2_t;
    double q3_t;
} ComauFeedback;

// Control data
typedef struct {
    double q1;
    double q2;
    double q3;
    double q4;
    double q5;
    double q6;
} ComauControl;

