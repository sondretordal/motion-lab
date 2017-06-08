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

// Variables in original Demo program
EXTRN char 												flag_ExitFromOpen;
EXTRN unsigned int 										modality_active;
EXTRN unsigned int 										modality_old;
EXTRN unsigned int										udp_started;

// Additional global variables
EXTRN pthread_t 										thread1;
EXTRN pthread_mutex_t									lock;
EXTRN double 											dt;
EXTRN int 												mode;

// callbackFunction.cpp
int callbackFunction(int);

// userFunctions.cpp
double Limit(double u, double hiLim, double loLim);
void *ReadWriteUDP(void *arg);
int InitializeControlPosition(void);
void DecodeModality(int si_modality, char* string);
int InputConsole(char * input_buffer, int size);
char getch();

// loopConsole.cpp
void loopConsole(void);

struct JointData {
	ORL_joint_value Pos, Vel, Acc;
};

EXTRN JointData Setpoint, ControlInput, Reference, Feedback;

// UDP data structs
struct UdpDataIn
{
	int udpKey;
	int mode;
	float omega;
	float beta;
	float q1;
	float q2;
	float q3;
	float q4;
	float q5;
	float q6;
	float q1_t;
	float q2_t;
	float q3_t;
	float q4_t;
	float q5_t;
	float q6_t;
	float q1_tt;
	float q2_tt;
	float q3_tt;
	float q4_tt;
	float q5_tt;
	float q6_tt;
};

struct UdpDataOut
{
	int modalityActive;
	float q1_ref;
	float q2_ref;
	float q3_ref;
	float q4_ref;
	float q5_ref;
	float q6_ref;
	float q1;
	float q2;
	float q3;
	float q4;
	float q5;
	float q6;
	float q1_t;
	float q2_t;
	float q3_t;
	float q4_t;
	float q5_t;
	float q6_t;
	float q1_tt;
	float q2_tt;
	float q3_tt;
	float q4_tt;
	float q5_tt;
	float q6_tt;
};

// Define udp output struct
EXTRN UdpDataIn* udpRecieve;
EXTRN UdpDataOut udpSend;






