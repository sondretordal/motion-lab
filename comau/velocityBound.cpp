# include "velocityBound.h"


VelocityBound velocityBound(double q[6], double qMin[6], double qMax[6], double V[6], double A[6], double Ts)
{
    // qDotMin <= qDot <= qDotMax
    // Eq. (13) in "Control of Redundant Robots Under Hard Joint
    // Constraints: Saturation in the Null Space", F, Flacco, A. De Luca, 
    // O. Khatib, IEEE Trnsactions on Robotics, 2015

    double a, b, c;
    VelocityBound bound;

    for (int i = 0; i < 6; i++)
    {
        // Ensure that V and A is positive
        V[i] = fabs(V[i]);
        A[i] = fabs(A[i]);

        // Ensure q is in [qMin, qMax]
        q[i] = fmax(q[i], qMin[i]);
        q[i] = fmin(q[i], qMax[i]);
        
        // Lower Bound       
        a = (qMin[i] - q[i])/Ts;
        b = -V[i];
        c = -sqrt(2*A[i]*(q[i] - qMin[i]));

        bound.qDotMin[i] = fmax(a, fmax(b, c));

        // Upper Bound
        a = (qMax[i] - q[i])/Ts;
        b = V[i];
        c = sqrt(2*A[i]*(qMax[i] - q[i]));

        bound.qDotMax[i] = fmin(a, fmin(b, c));
    }

    // Return velocity bound
    return bound;
    
}
