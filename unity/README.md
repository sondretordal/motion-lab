# Unity issue when recieveing UDP packet from remote source
Unity  does not support for some reason to recieve UDP data from a remote soruce e.g. and PLC. As a workaround, a python script can b used as a middleware or alternatively making C++ DLL which handle the communication and hence exchange the data with C# as an external library in real-time.

Other with the sam issue:
https://stackoverflow.com/questions/50560244/sending-udp-messages-works-receiving-not-c-sharp-on-unity3d

Include C/C++ DLL in Unity:
https://ericeastwood.com/blog/17/unity-and-dlls-c-managed-and-c-unmanaged

Create DLL using Cmake project
https://dominoc925.blogspot.com/2016/08/use-cmake-to-help-build-and-use-windows.html

