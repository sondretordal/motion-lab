// Pybind includes
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/eigen.h>


// Classes
#include "XboxController.h"


namespace py = pybind11;

PYBIND11_MODULE(motionlab, m) {
	// Module
	m.doc() = "Motion Laboratory module made for Python";

	// Xbox controller interface
	py::class_<Stick>(m, "Stick")
		.def(py::init<>())
		.def_readonly("x", &Stick::x)
		.def_readonly("y", &Stick::y)
		.def_readonly("clicked", &Stick::clicked);

	py::class_<Joypad>(m, "Pad")
		.def(py::init<>())
		.def_readonly("up", &Joypad::up)
		.def_readonly("down", &Joypad::down)
		.def_readonly("left", &Joypad::left)
		.def_readonly("right", &Joypad::right);

	py::class_<XboxController>(m, "XboxController")
		.def(py::init<>())
		.def_readonly("left", &XboxController::left)
		.def_readonly("right", &XboxController::right)
		.def_readonly("joypad", &XboxController::joypad)
		.def_readonly("LT", &XboxController::LT)
		.def_readonly("RT", &XboxController::RT)
		.def_readonly("A", &XboxController::A)
		.def_readonly("B", &XboxController::B)
		.def_readonly("X", &XboxController::X)
		.def_readonly("Y", &XboxController::Y)
		.def_readonly("LB", &XboxController::LB)
		.def_readonly("RB", &XboxController::RB)
		.def_readonly("back", &XboxController::back)
		.def_readonly("menu", &XboxController::menu)
		.def("start", &XboxController::start, "Start reading the controller inputs")
		.def("close", &XboxController::close, "Close the controller connection")
		.def("vibrate", &XboxController::vibrate, "Set vibration level")
		.def("battery_level", &XboxController::battery_level, "Print battery status")
		.def("is_connected", &XboxController::is_connected, "Check if controller is connected");
}



