#include "TestCPPLibrary.h"

#include "animallib_Export.h"

extern "C" {
    float TestMultiply(float a, float b)
    {
        return a * b;
    }

    float TestDivide(float a, float b)
    {
        if (b == 0) {
            return 0;
            //throw invalid_argument("b cannot be zero!");
        }

        return a / b;
    }
}