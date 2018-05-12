// PLC Feedback Types
typedef struct {
    double eta[6];
    double eta_t[6];
    double eta_tt[6];
} ST_StewartFeedback;

typedef struct {
    double eta[6];
    double v[6];
} ST_MruFeedback;

typedef struct {
    double q[3];
    double q_t[3];
    double q_tt[3];
} ST_ComauFeedback;

typedef struct {
    double l;
    double l_t;
    double l_tt;
} ST_WinchFeedback;

typedef struct {
    double d;
    double x;
    double y;
    double z;
} ST_QualisysFeedback;

typedef struct {
    ST_StewartFeedback em8000;
    ST_StewartFeedback em1500;
    ST_MruFeedback mru1;
    ST_MruFeedback mru2;
    ST_ComauFeedback comau;
    ST_WinchFeedback winch;
    ST_QualisysFeedback qtm;
} ST_Feedback;

// PLC Control Types
typedef struct {
    double eta[6];
} ST_StewartControl;

typedef struct {
    double q[3];
    double q_t[3];
    double q_tt[3];
} ST_ComauControl;

typedef struct {
    double l;
    double l_t;
    double l_tt;
} ST_WinchControl;

typedef struct {
    ST_StewartControl em8000;
    ST_StewartControl em1500;
    ST_ComauControl comau;
    ST_WinchControl winch;
} ST_Control;


