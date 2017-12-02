// Pybind includes
#include <pybind11/pybind11.h>
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
	py::class_<RemoteFeedbackStewart>(m, "RemoteFeedbackStewart")
		.def(py::init<>())
		.def_readonly("surge", &RemoteFeedbackStewart::surge)
		.def_readonly("sway", &RemoteFeedbackStewart::sway)
		.def_readonly("heave", &RemoteFeedbackStewart::heave)
		.def_readonly("phi", &RemoteFeedbackStewart::phi)
		.def_readonly("theta", &RemoteFeedbackStewart::theta)
		.def_readonly("psi", &RemoteFeedbackStewart::psi)
		.def_readonly("surge_t", &RemoteFeedbackStewart::surge_t)
		.def_readonly("sway_t", &RemoteFeedbackStewart::sway_t)
		.def_readonly("heave_t", &RemoteFeedbackStewart::heave_t)
		.def_readonly("phi_t", &RemoteFeedbackStewart::phi_t)
		.def_readonly("theta_t", &RemoteFeedbackStewart::theta_t)
		.def_readonly("psi_t", &RemoteFeedbackStewart::psi_t)
		.def_readonly("surge_tt", &RemoteFeedbackStewart::surge_tt)
		.def_readonly("sway_tt", &RemoteFeedbackStewart::sway_tt)
		.def_readonly("heave_tt", &RemoteFeedbackStewart::heave_tt)
		.def_readonly("phi_tt", &RemoteFeedbackStewart::phi_tt)
		.def_readonly("theta_tt", &RemoteFeedbackStewart::theta_tt)
		.def_readonly("psi_tt", &RemoteFeedbackStewart::psi_tt);

	py::class_<RemoteFeedbackComau>(m, "RemoteFeedbackComau")
		.def(py::init<>())
		.def_readonly("q1", &RemoteFeedbackComau::q1)
		.def_readonly("q2", &RemoteFeedbackComau::q2)
		.def_readonly("q3", &RemoteFeedbackComau::q3)
		.def_readonly("q4", &RemoteFeedbackComau::q4)
		.def_readonly("q5", &RemoteFeedbackComau::q5)
		.def_readonly("q6", &RemoteFeedbackComau::q6)
		.def_readonly("q1_t", &RemoteFeedbackComau::q1_t)
		.def_readonly("q2_t", &RemoteFeedbackComau::q2_t)
		.def_readonly("q3_t", &RemoteFeedbackComau::q3_t)
		.def_readonly("q4_t", &RemoteFeedbackComau::q4_t)
		.def_readonly("q5_t", &RemoteFeedbackComau::q5_t)
		.def_readonly("q6_t", &RemoteFeedbackComau::q6_t)
		.def_readonly("q1_tt", &RemoteFeedbackComau::q1_tt)
		.def_readonly("q2_tt", &RemoteFeedbackComau::q2_tt)
		.def_readonly("q3_tt", &RemoteFeedbackComau::q3_tt)
		.def_readonly("q4_tt", &RemoteFeedbackComau::q4_tt)
		.def_readonly("q5_tt", &RemoteFeedbackComau::q5_tt)
		.def_readonly("q6_tt", &RemoteFeedbackComau::q6_tt);

	py::class_<RemoteFeedbackLeica>(m, "RemoteFeedbackLeica")
		.def(py::init<>())
		.def_readonly("x", &RemoteFeedbackLeica::x)
		.def_readonly("y", &RemoteFeedbackLeica::y)
		.def_readonly("z", &RemoteFeedbackLeica::z)
		.def_readonly("q0", &RemoteFeedbackLeica::q0)
		.def_readonly("q1", &RemoteFeedbackLeica::q1)
		.def_readonly("q2", &RemoteFeedbackLeica::q2)
		.def_readonly("q3", &RemoteFeedbackLeica::q3);

	py::class_<RemoteFeedbackMru>(m, "RemoteFeedbackMru")
		.def(py::init<>())
		.def_readonly("heave",&RemoteFeedbackMru::heave)
		.def_readonly("heave_t",&RemoteFeedbackMru::heave_t)
		.def_readonly("heave_tt",&RemoteFeedbackMru::heave_tt)
		.def_readonly("turn_rate",&RemoteFeedbackMru::turn_rate)
		.def_readonly("phi",&RemoteFeedbackMru::phi)
		.def_readonly("theta",&RemoteFeedbackMru::theta)
		.def_readonly("psi",&RemoteFeedbackMru::psi)
		.def_readonly("wx",&RemoteFeedbackMru::wx)
		.def_readonly("wy",&RemoteFeedbackMru::wy)
		.def_readonly("wz",&RemoteFeedbackMru::wz)
		.def_readonly("wx_t",&RemoteFeedbackMru::wx_t)
		.def_readonly("wy_t",&RemoteFeedbackMru::wy_t)
		.def_readonly("wz_t",&RemoteFeedbackMru::wz_t)
		.def_readonly("x_t",&RemoteFeedbackMru::x_t)
		.def_readonly("y_t",&RemoteFeedbackMru::y_t)
		.def_readonly("z_t",&RemoteFeedbackMru::z_t)
		.def_readonly("x_tt",&RemoteFeedbackMru::x_tt)
		.def_readonly("y_tt",&RemoteFeedbackMru::y_tt)
		.def_readonly("z_tt",&RemoteFeedbackMru::z_tt);
	
	
	py::class_<RemoteFeedback>(m, "RemoteFeedback")
		.def(py::init<>())
		.def_readonly("t", &RemoteFeedback::t)
		.def_readonly("em8000", &RemoteFeedback::em8000)
		.def_readonly("em1500", &RemoteFeedback::em1500)
		.def_readonly("comau", &RemoteFeedback::comau)
		.def_readonly("at960", &RemoteFeedback::at960)
		.def_readonly("mru1", &RemoteFeedback::mru1)
		.def_readonly("mru2", &RemoteFeedback::mru2);

	// Control structs
	py::class_<RemoteControlComau>(m, "RemoteControlComau")
		.def(py::init<>())
		.def_readwrite("q1", &RemoteControlComau::q1)
		.def_readwrite("q2", &RemoteControlComau::q2)
		.def_readwrite("q3", &RemoteControlComau::q3)
		.def_readwrite("q4", &RemoteControlComau::q4)
		.def_readwrite("q5", &RemoteControlComau::q5)
		.def_readwrite("q6", &RemoteControlComau::q6)
		.def_readwrite("q1_t", &RemoteControlComau::q1_t)
		.def_readwrite("q2_t", &RemoteControlComau::q2_t)
		.def_readwrite("q3_t", &RemoteControlComau::q3_t)
		.def_readwrite("q4_t", &RemoteControlComau::q4_t)
		.def_readwrite("q5_t", &RemoteControlComau::q5_t)
		.def_readwrite("q6_t", &RemoteControlComau::q6_t)
		.def_readwrite("q1_tt", &RemoteControlComau::q1_tt)
		.def_readwrite("q2_tt", &RemoteControlComau::q2_tt)
		.def_readwrite("q3_tt", &RemoteControlComau::q3_tt)
		.def_readwrite("q4_tt", &RemoteControlComau::q4_tt)
		.def_readwrite("q5_tt", &RemoteControlComau::q5_tt)
		.def_readwrite("q6_tt", &RemoteControlComau::q6_tt);

	py::class_<RemoteControl>(m, "RemoteControl")
		.def(py::init<>())
		.def_readwrite("udp_key", &RemoteControl::udp_key)
		.def_readwrite("comau", &RemoteControl::comau);
	
	// Remote interface
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
		.def_readwrite("control", &RemoteInterface::control);

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



