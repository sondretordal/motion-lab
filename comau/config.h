#include <iostream>
#include <cmath>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <termios.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <pthread.h>
#include <time.h>
#include <math.h>

#include <eORL.h>

// Rapidjson
#include "rapidjson/filereadstream.h"
#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"

#ifdef  GLOBAL_VAR_EXTERN
#define EXTRN  extern
#else
#define EXTRN
#endif

#define false      										0
#define true       										1

// Set up the IP adress and system ID
#define STRING_IP_CNTRL        							"192.168.90.112"
#define STRING_SYS_ID          							"CNTRLC5G_11477"

// Set up the UDP server ip-adress, port and key
#define SERVER 											"192.168.90.32"
#define PORT 											50032
#define UDP_KEY	  										32

// Define modes
#define STOP_MODE										1
#define UDP_MODE										2

// Define PI
#define PI												3.14159265359

// (GLOBAL) Variables in original Demo program
EXTRN char 												flag_ExitFromOpen;
EXTRN unsigned int 										modality_active;
EXTRN unsigned int 										modality_old;
EXTRN unsigned int										udp_started;

// (GLOBAL) Additional global variables
EXTRN pthread_t 										thread1;
EXTRN pthread_mutex_t									lock;
EXTRN double 											dt;
EXTRN int 												mode;

// callbackFunction.cpp
int callbackFunction(int);

// userFunctions.cpp
void printSettings(void);
void loadSettings(void);
void *ReadWriteUDP(void *arg);
int InitializeControlPosition(void);
void DecodeModality(int si_modality, char* string);
int InputConsole(char * input_buffer, int size);
char getch();

// loopConsole.cpp
void loopConsole(void);

// Joint setpoint
EXTRN ORL_joint_value setpoint;

// Velocity Boundary settings
EXTRN double minAngleDeg[6], maxAngleDeg[6], maxSpeedRPM[6];

// UDP data structs
struct UdpDataIn
{
	int udpKey;
	int mode;
	float qDotRef[6];
};

struct UdpDataOut
{
	int frameCounter;
	float q[6];
	float qDot[6];
};

// Define udp output struct
EXTRN UdpDataIn* udpRecieve;
EXTRN UdpDataOut udpSend;






