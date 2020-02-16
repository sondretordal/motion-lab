#include <iostream>
#include "Animal.h"

#include "animallib_Export.h"

using namespace std;

animallib_EXPORT Animal::Animal(string name):name (name){}

animallib_EXPORT void Animal::print_name(){
    cout << "Name is " << this->name << endl;
}