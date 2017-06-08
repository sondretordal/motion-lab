UDP Interface for the Comau Robot
#################################
The comau robot makes use of the C5GOpen modality to control and read feedback mesuremnets 
from the robot controller using the PowerLink connection. This program extends the capability of the
C5GOpen interface to also accept remote control and logging using an UDP connection, which again is 
connected to the Beckhoff control unit.

Compilation and Run
###################

| cd comau
| cmake .
| make
| ./main

The eORL library provided by Comau robotics is required for the UDP iterface to work.
Also the robot controller has to be configured to use tyhe C5GOpen modality.




