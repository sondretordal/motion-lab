# motion-lab

Source files for Motion Lab UiA

HMI
./hmi

PLC
./plc

Example and tutorial on using the cmake build system with MSVC compiler:
https://github.com/cognitivewaves/CMake-VisualStudio-Example

Boost build command for MSVC 14.0 64-bit:
bootstrap
b2 --includedir=C:/api/include --libdir==C:/api/lib --build-dir=C:/api/build --address-model=64 --build-type=complete --toolset=msvc-14.0 --threading=multi --runtime-link=shared --variant=release install
