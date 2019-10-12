#define GLOBAL_VAR_EXTERN
#include "config.h"

void loopConsole(void)
{
	char a_1, keep_on_running = true,
		f_1_command = false,
		f_2_arm_to_exit = false,
		f_2_print_angles = false,
		f_2_print_settings = false,
		f_2_reload_settings = false,
		f_2_UDP_mode = false,
		temp[80];

	memset(temp, 0x00, 80);

	while (keep_on_running)
	{
		f_1_command = true;

		if (f_1_command)
		{
			printf("\n");
			printf("**** Main Menu ****\n");
			printf("Press E to exit from C5GOpen\n");
			printf("Press C to close the application\n");
			printf("Press P to print current joint angles\n");
			printf("Press S to print velocity boundary settings\n");
			printf("Press R to reaload velocity boundary settings from JSON\n");
			printf("Press U to enable remote UDP Mode\n");

			// Read keyboard input from user
			InputConsole(temp, sizeof(temp));
			a_1 = temp[0];
			
			switch (a_1)
			{
				case 'P':
				case 'p':
					f_1_command = false;
					f_2_print_angles = true;
					break;
				
				case 'S':
				case 's':
					f_1_command = false;
					f_2_print_settings = true;
					break;

				case 'R':
				case 'r':
					f_1_command = false;
					f_2_reload_settings = true;
					break;

				case 'U':
				case 'u':
					f_1_command = false;
					f_2_UDP_mode = true;
					break;

				case 'E':
				case 'e':
					f_1_command = false;
					f_2_arm_to_exit = true;
					break;

				case 'C':
				case 'c':
					flag_ExitFromOpen = true;

					// Start thread for UDP communication
					pthread_cancel(thread1);

					ORLOPEN_DriveOffFromPC(ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
					sleep(4);
					ORLOPEN_StopCommunication(ORL_SILENT);
					sleep(2);
					keep_on_running = false;
					break;

				default:
					printf("--! Invalid value!\n");
					f_1_command = true;
					break;
			}
		}

		if (f_2_arm_to_exit)
		{
			flag_ExitFromOpen = true;
			f_2_arm_to_exit = false;
			f_1_command = true;
		}

		if (f_2_print_angles)
		{
			ORLOPEN_sync_position(&setpoint, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
			ORL_joints_conversion(&setpoint, ORL_POSITION_LINK_RAD, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);

			printf("**** Current Robot Angles ****\n");

			for (int i = 0; i < 6; i++)
			{
				printf("Joint No. %i = %f [deg]\n", i, setpoint.value[i]/PI*180.0);
			}

			f_2_print_angles = false;
			f_1_command = true;
		}

		if (f_2_print_settings)
		{
			printSettings();

			f_2_print_settings = false;
			f_1_command = true;
		}

		if (f_2_reload_settings)
		{
			// Load and print new settings
			loadSettings();
			printSettings();

			f_2_reload_settings = false;
			f_1_command = true;
		}

		if (f_2_UDP_mode)
		{
			printf("**** Remote UDP Mode ****\n");
			printf("Press O to read data recieved on UDP \n");
			printf("Press Q to return to main menu \n\n");

			mode = UDP_MODE;
			while (f_2_UDP_mode)
			{
				switch (getch())
				{
				case 'O':
				case 'o':
					if (udp_started == 1)
					{
						if (udpRecieve->udpKey == UDP_KEY)
						{
							printf("UdpKey = %i \n", udpRecieve->udpKey);
							printf("Mode = %i \n\n", udpRecieve->mode);

							for (int i = 0; i < 6; i++)
							{
								printf("qDotRef[%i] = %f [rad/s]\n", i, udpRecieve->qDotRef[i]);
							}

							printf("\n");
							printf("**** Remote UDP Mode ****\n");
							printf("Press O to read data recieved on UDP \n");
							printf("Press Q to return to main menu \n\n");
						}
						else
						{
							printf("The client's UDP key is wrong! \n\n");

							printf("**** Remote UDP Mode ****\n");
							printf("Press O to read data recieved on UDP \n");
							printf("Press Q to return to main menu \n\n");
						}
						
					}
					else
					{
						printf("The UDP connection has not been started yet! \n\n");

						printf("**** Remote UDP Mode ****\n");
						printf("Press O to read data recieved on UDP \n");
						printf("Press Q to return to main menu \n\n");
					}
					break;

				case 'Q':
				case 'q':
					mode = STOP_MODE;
					f_1_command = true;
					f_2_UDP_mode = false;
					break;
				default:
					break;
				}
			}
		}
	}
}
