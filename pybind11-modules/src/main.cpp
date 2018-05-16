// Pybind includes
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/eigen.h>


// Classes
#include "UdpServer.h"
#include "RemoteInterface.h"
#include "XboxController.h"


namespace py = pybind11;

PYBIND11_PLUGIN(motionlab) {
	// Module
	py::module m("motionlab", "Motion Laboratory module made for Python");

	// Feedback structs
	py::class_<Qtm3DMarkerPositionNoLabel>(m, "Qtm3DMarkerPositionNoLabel")
		.def(py::init<>())
		.def_readonly("x", &Qtm3DMarkerPositionNoLabel::x)
		.def_readonly("y", &Qtm3DMarkerPositionNoLabel::y)
		.def_readonly("z", &Qtm3DMarkerPositionNoLabel::z)
		.def_readonly("id", &Qtm3DMarkerPositionNoLabel::id);

	py::class_<FeedbackStewart>(m, "FeedbackStewart")
		.def(py::init<>())
		.def_readonly("surge", &FeedbackStewart::surge)
		.def_readonly("sway", &FeedbackStewart::sway)
		.def_readonly("heave", &FeedbackStewart::heave)
		.def_readonly("phi", &FeedbackStewart::phi)
		.def_readonly("theta", &FeedbackStewart::theta)
		.def_readonly("psi", &FeedbackStewart::psi)
		.def_readonly("surge_t", &FeedbackStewart::surge_t)
		.def_readonly("sway_t", &FeedbackStewart::sway_t)
		.def_readonly("heave_t", &FeedbackStewart::heave_t)
		.def_readonly("phi_t", &FeedbackStewart::phi_t)
		.def_readonly("theta_t", &FeedbackStewart::theta_t)
		.def_readonly("psi_t", &FeedbackStewart::psi_t)
		.def_readonly("surge_tt", &FeedbackStewart::surge_tt)
		.def_readonly("sway_tt", &FeedbackStewart::sway_tt)
		.def_readonly("heave_tt", &FeedbackStewart::heave_tt)
		.def_readonly("phi_tt", &FeedbackStewart::phi_tt)
		.def_readonly("theta_tt", &FeedbackStewart::theta_tt)
		.def_readonly("psi_tt", &FeedbackStewart::psi_tt);

	py::class_<FeedbackComau>(m, "FeedbackComau")
		.def(py::init<>())
		.def_readonly("q1", &FeedbackComau::q1)
		.def_readonly("q2", &FeedbackComau::q2)
		.def_readonly("q3", &FeedbackComau::q3)
		.def_readonly("q4", &FeedbackComau::q4)
		.def_readonly("q5", &FeedbackComau::q5)
		.def_readonly("q6", &FeedbackComau::q6)
		.def_readonly("q1_t", &FeedbackComau::q1_t)
		.def_readonly("q2_t", &FeedbackComau::q2_t)
		.def_readonly("q3_t", &FeedbackComau::q3_t)
		.def_readonly("q4_t", &FeedbackComau::q4_t)
		.def_readonly("q5_t", &FeedbackComau::q5_t)
		.def_readonly("q6_t", &FeedbackComau::q6_t)
		.def_readonly("q1_tt", &FeedbackComau::q1_tt)
		.def_readonly("q2_tt", &FeedbackComau::q2_tt)
		.def_readonly("q3_tt", &FeedbackComau::q3_tt)
		.def_readonly("q4_tt", &FeedbackComau::q4_tt)
		.def_readonly("q5_tt", &FeedbackComau::q5_tt)
		.def_readonly("q6_tt", &FeedbackComau::q6_tt);

	py::class_<FeedbackLeica>(m, "FeedbackLeica")
		.def(py::init<>())
		.def_readonly("x", &FeedbackLeica::x)
		.def_readonly("y", &FeedbackLeica::y)
		.def_readonly("z", &FeedbackLeica::z)
		.def_readonly("q0", &FeedbackLeica::q0)
		.def_readonly("q1", &FeedbackLeica::q1)
		.def_readonly("q2", &FeedbackLeica::q2)
		.def_readonly("q3", &FeedbackLeica::q3);

	py::class_<FeedbackMru>(m, "FeedbackMru")
		.def(py::init<>())
		.def_readonly("surge", &FeedbackMru::surge)
		.def_readonly("sway", &FeedbackMru::sway)
		.def_readonly("heave", &FeedbackMru::heave)
		.def_readonly("surge_t", &FeedbackMru::surge_t)
		.def_readonly("sway_t", &FeedbackMru::sway_t)
		.def_readonly("heave_t", &FeedbackMru::heave_t)
		.def_readonly("surge_tt", &FeedbackMru::surge_tt)
		.def_readonly("sway_tt", &FeedbackMru::sway_tt)
		.def_readonly("heave_tt", &FeedbackMru::heave_tt)
		.def_readonly("turn_rate", &FeedbackMru::turn_rate)
		.def_readonly("phi", &FeedbackMru::phi)
		.def_readonly("theta", &FeedbackMru::theta)
		.def_readonly("psi", &FeedbackMru::psi)
		.def_readonly("wx", &FeedbackMru::wx)
		.def_readonly("wy", &FeedbackMru::wy)
		.def_readonly("wz", &FeedbackMru::wz)
		.def_readonly("x_t", &FeedbackMru::x_t)
		.def_readonly("y_t", &FeedbackMru::y_t)
		.def_readonly("z_t", &FeedbackMru::z_t)
		.def_readonly("x_tt", &FeedbackMru::x_tt)
		.def_readonly("y_tt", &FeedbackMru::y_tt)
		.def_readonly("z_tt", &FeedbackMru::z_tt);

	py::class_<FeedbackQualisys>(m, "FeedbackQualisys")
		.def(py::init<>())
		.def_readonly("status", &FeedbackQualisys::status)
		.def_readonly("d", &FeedbackQualisys::d)
		.def_readonly("x", &FeedbackQualisys::x)
		.def_readonly("y", &FeedbackQualisys::y)
		.def_readonly("z", &FeedbackQualisys::z);

	py::class_<FeedbackWinch>(m, "FeedbackWinch")
		.def(py::init<>())
		.def_readonly("l", &FeedbackWinch::l)
		.def_readonly("l_t", &FeedbackWinch::l_t)
		.def_readonly("l_tt", &FeedbackWinch::l_tt);
	
	
	py::class_<Feedback>(m, "Feedback")
		.def(py::init<>())
		.def_readonly("t", &Feedback::t)
		.def_readonly("em8000", &Feedback::em8000)
		.def_readonly("em1500", &Feedback::em1500)
		.def_readonly("comau", &Feedback::comau)
		.def_readonly("at960", &Feedback::at960)
		.def_readonly("mru1", &Feedback::mru1)
		.def_readonly("mru2", &Feedback::mru2)
		.def_readonly("qtm", &Feedback::qtm)
		.def_readonly("winch", &Feedback::winch);
		

	// Control structs
	py::class_<ControlComau>(m, "ControlComau")
		.def(py::init<>())
		.def_readwrite("q1", &ControlComau::q1)
		.def_readwrite("q2", &ControlComau::q2)
		.def_readwrite("q3", &ControlComau::q3)
		.def_readwrite("q4", &ControlComau::q4)
		.def_readwrite("q5", &ControlComau::q5)
		.def_readwrite("q6", &ControlComau::q6)
		.def_readwrite("q1_t", &ControlComau::q1_t)
		.def_readwrite("q2_t", &ControlComau::q2_t)
		.def_readwrite("q3_t", &ControlComau::q3_t)
		.def_readwrite("q4_t", &ControlComau::q4_t)
		.def_readwrite("q5_t", &ControlComau::q5_t)
		.def_readwrite("q6_t", &ControlComau::q6_t)
		.def_readwrite("q1_tt", &ControlComau::q1_tt)
		.def_readwrite("q2_tt", &ControlComau::q2_tt)
		.def_readwrite("q3_tt", &ControlComau::q3_tt)
		.def_readwrite("q4_tt", &ControlComau::q4_tt)
		.def_readwrite("q5_tt", &ControlComau::q5_tt)
		.def_readwrite("q6_tt", &ControlComau::q6_tt);

	py::class_<Control>(m, "Control")
		.def(py::init<>())
		.def_readwrite("comau", &Control::comau);
	
	//  interface
	py::class_<RemoteInterface>(m, "RemoteInterface")
		.def(py::init<unsigned int>())
		.def("start", &RemoteInterface::start)
		.def("close", &RemoteInterface::close)
		.def("update", &RemoteInterface::update)
		.def("log", &RemoteInterface::log, "Start synchronous logging")
		.def("async_log", &RemoteInterface::async_log, "Start asynchronous logging")
		.def("clear_log", &RemoteInterface::clear_log)
		.def("save_log", &RemoteInterface::save_log)
		.def_readonly("feedback", &RemoteInterface::feedback)
		.def_readwrite("control", &RemoteInterface::control)
		.def_readwrite("test", &RemoteInterface::test);

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
		

	// Return module
	return m.ptr();
}



