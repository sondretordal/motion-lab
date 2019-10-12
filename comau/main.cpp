#include <config.h>
#include <eORL.h>


int  main (int argc, char **argv)
{
	// Read Velocity Boundary settings from JSON
	loadSettings();

	// Local vars
	ORL_cartesian_position sx_base, sx_tool, sx_uframe;

	// Variables defined in config.h initialization
	flag_ExitFromOpen = false;
	modality_active = CRCOPEN_LISTEN;
	modality_old = CRCOPEN_LISTEN;
	mode = STOP_MODE;
	udp_started == 0;
	
	// IP address and system ID defined in config.h
	printf("Connection to %s: %s.c5g\n",STRING_IP_CNTRL, STRING_SYS_ID);
	
	// Read the .cfg file from the robot controller using the regualer ethernet connection
	if( (ORLOPEN_initialize_controller(STRING_IP_CNTRL,STRING_SYS_ID,ORL_SILENT,ORL_CNTRL01)) != 0 )
	{
		printf("error ORL_initialize_robot\n");
		exit(0);
	}
	else
	{
		printf("%s: %s.c5g OK\n",STRING_IP_CNTRL, STRING_SYS_ID);
	}
	
	// eORL control structs
	setpoint.unit_type = ORL_POSITION_LINK_RAD;

	/* $TOOL */
	sx_tool.unit_type = ORL_CART_POSITION;
	sx_tool.x = 0; sx_tool.y = 0; sx_tool.z = 0.0;
	sx_tool.a = 0; sx_tool.e = 0; sx_tool.r = 0;

	/* $UFRAME */
	sx_uframe.unit_type = ORL_CART_POSITION;
	sx_uframe.x = 0; sx_uframe.y = 0; sx_uframe.z = 0;
	sx_uframe.a = 0; sx_uframe.e = 0; sx_uframe.r = 0;

	/* $BASE ARM*/
	sx_base.unit_type = ORL_CART_POSITION;
	sx_base.x = 0; sx_base.y = 0; sx_base.z = 0;
	sx_base.a = 0; sx_base.e = 0; sx_base.r = 0;
	ORL_initialize_frames(sx_base, sx_tool, sx_uframe, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);

	// Define the callbackfunction and set cycle time
	ORLOPEN_set_period(ORL_0_4_MILLIS, ORL_VERBOSE, ORL_CNTRL01);
	dt = 0.4 / 1000;

	ORLOPEN_SetCallBackFunction(&callbackFunction, ORL_SILENT, ORL_CNTRL01);
	sleep(1);

	// Start the PowerLink communincation
	if (ORLOPEN_StartCommunication(ORL_SILENT) != 0)
	{
		ORLOPEN_GetPowerlinkState(ORL_SILENT);
		exit(0);
	}

	// Create a thread to read write UDP data
	pthread_create(&thread1, NULL, ReadWriteUDP, NULL);
	pthread_mutex_init(&lock, 0);

	// Initilize control position and start loopConsole()
	sleep(2);
	InitializeControlPosition();

	// Start console interface
	loopConsole();
	
	return 0;

}