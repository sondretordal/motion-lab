// Pybind includes
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

// PYBIND11_PLUGIN(motionlab) {
// 	// Module
// 	py::module m("motionlab", "Motion Laboratory module made for Python");

// 	// Wrap class
// 	py::class_<XboxController>(m, "XboxController")
// 		.def(py::init<>())
// 		.def_readonly("left", &XboxController::left)
// 		.def_readonly("right", &XboxController::right)
// 		.def_readonly("joypad", &XboxController::joypad)
// 		.def_readonly("LT", &XboxController::LT)
// 		.def_readonly("RT", &XboxController::RT)
// 		.def_readonly("A", &XboxController::A)
// 		.def_readonly("B", &XboxController::B)
// 		.def_readonly("X", &XboxController::X)
// 		.def_readonly("Y", &XboxController::Y)
// 		.def_readonly("LB", &XboxController::LB)
// 		.def_readonly("RB", &XboxController::RB)
// 		.def_readonly("back", &XboxController::back)
// 		.def_readonly("menu", &XboxController::menu)
// 		.def("start", &XboxController::start, "Start reading the controller inputs")
// 		.def("close", &XboxController::close, "Close the controller connection")
// 		.def("vibrate", &XboxController::vibrate, "Set vibration level")
// 		.def("battery_level", &XboxController::battery_level, "Print battery status")
// 		.def("is_connected", &XboxController::is_connected, "Check if controller is connected");
		
// 	// Return module
// 	return m.ptr();
// }


#include <iostream>
#include <conio.h>
#include <windows.h>

// ADS headers
#include "TcAdsDef.h"
#include "TcAdsApi.h"

using namespace std;

int main()
{

	long nErr, nPort;
	AmsAddr Addr;
	PAmsAddr pAddr = &Addr;

	// Open communication port on the ADS router
	nPort = AdsPortOpen();
	nErr = AdsGetLocalAddress(pAddr);
	
	if (nErr)
	{
		std::cerr << "Error: AdsGetLocalAddress: " << nErr << '\n';
	}
		

	pAddr->port = AMSPORT_R0_PLC_TC3;

	
	return 0;
}



