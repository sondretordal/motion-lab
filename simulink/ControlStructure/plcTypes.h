// Feedback types
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
} ST_StewartFeedback;

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
	double turn_rate;
	double phi;
	double theta;
	double psi;
	double wx;
	double wy;
	double wz;
	double x_t;
	double y_t;
	double z_t;
	double x_tt;
	double y_tt;
	double z_tt;
} ST_MruFeedback;

typedef struct {
    double q1;
    double q2;
    double q3;
    double q4;
    double q5;
    double q6;
    double q1_t;
    double q2_t;
    double q3_t;
    double q4_t;
    double q5_t;
    double q6_t;
    double q1_tt;
    double q2_tt;
    double q3_tt;
    double q4_tt;
    double q5_tt;
    double q6_tt;
} ST_ComauFeedback;

// Control types
typedef struct {
    // Rotation Sequence: XYZ
    double surge;
    double sway;
    double heave;
    double phi;
    double theta;
    double psi;
} ST_ControlStewart;

typedef struct {
    double q1;
    double q2;
    double q3;
    double q4;
    double q5;
    double q6;
    double q1_t;
    double q2_t;
    double q3_t;
    double q4_t;
    double q5_t;
    double q6_t;
    double q1_tt;
    double q2_tt;
    double q3_tt;
    double q4_tt;
    double q5_tt;
    double q6_tt;
} ST_ComauControl;

