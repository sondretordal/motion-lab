.. _com:

Setup and Structure
#################################

This section presents the communication structure and setup of the Motion-Lab. 
The laboratory consists of two Stewart Platforms (E-Motion 8000 and 1500), 
an industrial robot (COMAU Smart 5 NJ 110-3.0),
an embedded PC (Beckhoff PC CX2040) working as a central control unit, 
and a Real-Time target computer which is connected to the user portal.

A schematic of the communication setup is illustrated in the figure below.

.. image:: /img/communcation_schematic.svg

As the figure shows, different components uses different communication protocols, 
where each of the components has their own IP address, and communication port.