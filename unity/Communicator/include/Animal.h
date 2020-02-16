#include <string>

#include "animallib_Export.h"

using namespace std;

class Animal {
private:
    string name;
public:
    animallib_EXPORT Animal(string);
    virtual animallib_EXPORT void print_name();
};