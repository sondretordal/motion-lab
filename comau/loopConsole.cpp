#define GLOBAL_VAR_EXTERN
#include "config.h"

void loopConsole(void)
{
	char a_1, keep_on_running = true,
		f_1_command = false,
		f_2_arm_to_exit = false,
		f_2_loop_keyboard = false,
		f_2_heave_mode = false,
		f_2_UDP_mode = false,
		temp[80];

	memset(temp, 0x00, 80);

	while (keep_on_running)
	{
		f_1_command = true;

		if (f_1_command)
		{
			printf("**** Main Menu ****\n");
			printf("Press E to exit from C5GOpen\n");
			printf("Press C to close the application\n");
			printf("Press U to enable remote UDP Mode\n");

			InputConsole(temp, sizeof(temp));
			a_1 = temp[0];
			switch (a_1)
			{
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

				printf("Perform a DriveOFF on the TeachPendent\n");
				sleep(6);
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
							printf("Mode = %i \n", udpRecieve->mode);
							printf("q1 = %f \n", udpRecieve->q1);
							printf("q2 = %f \n", udpRecieve->q2);
							printf("q3 = %f \n", udpRecieve->q3);
							printf("q4 = %f \n", udpRecieve->q4);
							printf("q5 = %f \n", udpRecieve->q5);
							printf("q6 = %f \n \n", udpRecieve->q6);

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
