#define GLOBAL_VAR_EXTERN
#include "config.h"

double Limit(double u, double hiLim, double loLim)
{	
	if (u > hiLim)
	{
		return hiLim;
	}
	else if (u < loLim)
	{
		return loLim;
	}
	else
	{
		return u;
	}


}

void *ReadWriteUDP(void *arg)
{
	// UDP struct and defines
	struct sockaddr_in si_me, si_other;
	socklen_t slen;
	int s;

	slen = sizeof(si_other);

	//create a UDP socket
	if ((s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == -1)
	{
		printf("ERROR creating UDP socket on %i, IP: %s \n", PORT, SERVER);
	}

	// zero out the structure
	memset((char*)&si_me, 0, sizeof(si_me));
	si_me.sin_family = AF_INET;
	si_me.sin_port = htons(PORT);
	si_me.sin_addr.s_addr = inet_addr(SERVER);

	//bind socket to port
	if (bind(s, (struct sockaddr*)&si_me, sizeof(si_me)) == -1)
	{
		printf("ERROR binding to port %i, IP: %s \n", PORT, SERVER);
	}

	// Initilize udp buffers
	char udpBufferRead[sizeof(UdpDataIn)];
	char udpBufferWrite[sizeof(UdpDataOut)];

	while (1)
	{
		// Try to receive some data, this is a blocking call
		if ((recvfrom(s, udpBufferRead, sizeof(udpBufferRead), 0, (struct sockaddr*) &si_other, &slen)) == -1)
		{
			printf("ERROR recieving data on port %i, IP: %s \n", PORT, SERVER);
		}
		
		// Detonate that the udp connection has been started once
		udp_started = 1;

		// Cast recieved buffer to struct
		udpRecieve = (UdpDataIn*)udpBufferRead;

		// Cast struct to send buffer
		memcpy(&udpBufferWrite, &udpSend, sizeof(udpSend));

		// Send data to client
		if (sendto(s, udpBufferWrite, sizeof(udpBufferWrite), 0, (struct sockaddr*) &si_other, slen) == -1)
		{
			printf("ERROR sending data on port %i, IP: %s \n", PORT, SERVER);
		}
	}

	return NULL;

}

int InitializeControlPosition(void)
{
	int res;
	long sm_out_maskjnt;
	ORL_System_Variable orl_sys_var;
	char s_modality[40];
	int modality;

	res = ORLOPEN_GetPowerlinkState(ORL_VERBOSE);

	if (res == PWL_ACTIVE)
	{
		sm_out_maskjnt = ORLOPEN_GetOpenMask(ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
		modality = ORLOPEN_GetModeMasterAx(ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
		DecodeModality(modality, s_modality);
		printf("\n------ ARM %d MODE %d %s - %s mask %x ------------ \n",
			ORL_ARM1 + 1,
			modality, s_modality,
			((ORLOPEN_GetStatusMasterAx(ORL_SILENT, ORL_CNTRL01, ORL_ARM1) == 4) ? "DRIVE_ON" : "DRIVEOFF"),(unsigned int)sm_out_maskjnt);

		ORLOPEN_sync_position(&Setpoint.Pos, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
		ORL_joints_conversion(&Setpoint.Pos, ORL_POSITION_LINK_DEGREE, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);

		for (int i = 0; i < 6; i++) {
			Setpoint.Vel.value[i] = 0.0;
			Setpoint.Acc.value[i] = 0.0;

			Reference.Vel.value[i] = 0.0;
			Reference.Acc.value[i] = 0.0;
		}

		printf("ORLOPEN_sync_position J %f %f %f %f %f %f %f\n", Reference.Pos.value[ORL_AX1], Reference.Pos.value[ORL_AX2], Reference.Pos.value[ORL_AX3], Reference.Pos.value[ORL_AX4], Reference.Pos.value[ORL_AX5], Reference.Pos.value[ORL_AX6], Reference.Pos.value[ORL_AX7]);
		
		sprintf((char *)orl_sys_var.sysvar_name, "$ARM_DATA[%d].ARM_OVR", ORL_ARM1 + 1);
		orl_sys_var.ctype = ORL_INT;
		orl_sys_var.iv = 20;
		ORL_set_data(orl_sys_var, ORL_SILENT, ORL_CNTRL01);
		return 1;

	}
	return 0;
}



void DecodeModality(int si_modality, char* string)
{
	switch (si_modality)
	{
	case CRCOPEN_LISTEN:
		sprintf(string, "CRCOPEN_LISTEN");
		break;
	case CRCOPEN_POS_ABSOLUTE:
		sprintf(string, "CRCOPEN_POS_ABSOLUTE");
		break;
	case CRCOPEN_POS_RELATIVE:
		sprintf(string, "CRCOPEN_POS_RELATIVE");
		break;
	case CRCOPEN_POS_ADDITIVE:
		sprintf(string, "CRCOPEN_POS_ADDITIVE");
		break;
	case CRCOPEN_POS_ADDITIVE_SB:
		sprintf(string, "CRCOPEN_POS_ADDITIVE_SB");
		break;
	case CRCOPEN_POS_ADDITIVE_SBE:
		sprintf(string, "CRCOPEN_POS_ADDITIVE_SBE");
		break;
	default:
		sprintf(string, "--");
		break;
	}
}


int InputConsole(char * input_buffer, int size)
{
	char* temp;

	if (fgets(input_buffer, size, stdin) != NULL)
	{

	}
	if ((input_buffer[0] == 0) || (input_buffer[0] == 0x0a))
		return 0;
	else
	{
		temp = strchr(input_buffer, '\n');
		if ((temp != NULL) && ((temp - input_buffer) << size))
			*temp = '\0';
		return 1;
	}
}

// Read terminal input without echo
char getch()
{
	char buf = 0;
	struct termios old = { 0 };
	if (tcgetattr(0, &old) < 0)
		perror("tcsetattr()");
	old.c_lflag &= ~ICANON;
	old.c_lflag &= ~ECHO;
	old.c_cc[VMIN] = 1;
	old.c_cc[VTIME] = 0;
	if (tcsetattr(0, TCSANOW, &old) < 0)
		perror("tcsetattr ICANON");
	if (read(0, &buf, 1) < 0)
		perror("read()");
	old.c_lflag |= ICANON;
	old.c_lflag |= ECHO;
	if (tcsetattr(0, TCSADRAIN, &old) < 0)
		perror("tcsetattr ~ICANON");
	return (buf);
}

