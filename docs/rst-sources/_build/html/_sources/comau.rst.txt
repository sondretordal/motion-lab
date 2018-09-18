Comau Robot Interface
#####################

General
-------
The Comau robot makes use of the C5GOpen modality to control and read the feedback measurements 
from the robot controller using the PowerLink connection. This program extends the capability of the
C5GOpen interface to also accept remote control and logging using a regular UDP connection.

Compilation and Run
-------------------

.. code-block:: console

    cd comau
    cmake .
    make
    ./main

The eORL library provided by Comau robotics is required for the UDP iterface to work.
Also the robot controller has to be configured to use the C5GOpen modality.




