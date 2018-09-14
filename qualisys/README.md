# Usage
This project is intended to be used together with the Qualisys Track Manager found on the Qualisys PC inside the Motion Laboratory (PC3 on the KVM switch.

# Remote Data Trnasfer to Beckhoff CX2040
* Execute "RTClientExample.exe" found in the install directory of the Qualisys Track Manager SW. After starting the Track Manager project.
* Connect to the "localhost".
* Chose "Little Endian" data type.
* Chose "Data Transfer"
* Select component type number "5: 3D no labels".
* Select "Stream Data UDP".
* Chose "2 : Stream to different address and port".
* Set the port number to 50199 and IP adress to 192.168.90.199.
* Select "All Frames".
* Finally chose "1 : Show current frame".

The data is now avaibale in the PLC project.
