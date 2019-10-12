#include <stdio.h>
#include <math.h>

struct VelocityBound
{
    double qDotMin[6];
    double qDotMax[6];
};


VelocityBound velocityBound(double q[6], double qMin[6], double qMax[6], double V[6], double A[6], double Ts);


