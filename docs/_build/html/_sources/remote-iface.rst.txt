Remote UDP interface
####################

Remote Setup
------------
The Motion Laboratory can be operated using the remote interface, given that the remote mode is enabled from the main HMI. The remote mode is selected in the main HMI.

.. image:: /img/remoteModeEnabled.png

The user have to connect to the physical Ethernet port named X001 on the Beckhoff CX2040. The following settings have to be changed on the remote unit in order to establish the remote UDP connection.

The remote has to switch to use a static IP adress which is set to ``192.168.90.60`` using subnet ``255.255.255.0``. Also ensure that nothign else is using the port ``50060`` since it will be used for the UDP communication with Motion Lab.

The following Python example illustrates how the UDP comunication is realized in a simple PyQt app.

.. literalinclude:: ../remote-iface/RemoteInterface.py
   :language: python


Data Types
----------
The PyQt app sends and recieves data of the types ``TxUdp`` and ``RxUdp`` every 50ms using the UDP socket. The two data types are defined as data structures given by:

.. literalinclude:: ../remote-iface/TxUdp.py
   :language: python

.. literalinclude:: ../remote-iface/RxUdp.py
   :language: python




