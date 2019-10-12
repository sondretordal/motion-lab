#define GLOBAL_VAR_EXTERN
#include "config.h"

#include "velocityBound.h"


int callbackFunction(int period)
{
	char flag_new_modality, s_modality[40];

	// Velocity boundary
	VelocityBound bound;
	double qRef[6], qDotRef[6], qMin[6], qMax[6], V[6],  A[6];

	// Convert to SI units
	for (int i = 0; i < 6; i++)
	{
		qMin[i] = minAngleDeg[i]/180.0*PI;
		qMax[i] = maxAngleDeg[i]/180.0*PI;
		
		V[i] = maxSpeedRPM[i]*2.0*PI/60.0;
		A[i] = 1.0;
	}

	// Control joint position data 
	ORL_joint_value control;

	// Feedback joint data
	ORL_joint_value position, velocity;

	// Modality change notification
	flag_new_modality = false;
	modality_old = modality_active;
	modality_active = ORLOPEN_GetModeMasterAx(ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
	ORLOPEN_GetOpenMask(ORL_SILENT, ORL_CNTRL01, ORL_ARM1);

	if (modality_old != modality_active)
	{
		flag_new_modality = true;
		DecodeModality((unsigned int)modality_active, s_modality);
		printf("ARM %d Modality %d %s\n", (ORL_ARM1 + 1), (unsigned int)modality_active, s_modality);
	}
	else
	{
		flag_new_modality = false;
	}

	switch (modality_active)
	{
	case CRCOPEN_LISTEN:
		ORLOPEN_sync_position(&setpoint, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
		ORL_joints_conversion(&setpoint, ORL_POSITION_LINK_RAD, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);

		break;

	case CRCOPEN_POS_ABSOLUTE:
		// Mode switch
		switch (mode)
		{
		case STOP_MODE:
			// Copy current joint angles
			ORLOPEN_sync_position(&setpoint, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
			ORL_joints_conversion(&setpoint, ORL_POSITION_LINK_RAD, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);

			break;

		case UDP_MODE:
			if (udpRecieve->udpKey == UDP_KEY  && udp_started == 1)
			{
				if (udpRecieve->mode == 1)
				{
					pthread_mutex_lock(&lock);
					for (int i = 0; i < 6; i++)
					{	
						// Apply velocity bound
						qRef[i] = setpoint.value[i];
						qDotRef[i] = (double)udpRecieve->qDotRef[i];

						bound = velocityBound(qRef, qMin, qMax, V, A, dt);

						qDotRef[i] = fmax(qDotRef[i], bound.qDotMin[i]);
						qDotRef[i] = fmin(qDotRef[i], bound.qDotMax[i]);

						// Apply numerical integration based on qDotRef
						setpoint.value[i] = setpoint.value[i] + qDotRef[i]*dt;

						// Absolute postion constraint
						setpoint.value[i] = fmax(setpoint.value[i], qMin[i]);
						setpoint.value[i] = fmin(setpoint.value[i], qMax[i]);
					}
						
					pthread_mutex_unlock(&lock);
				}
				else
				{
					// Copy current joint angles
					ORLOPEN_sync_position(&setpoint, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
					ORL_joints_conversion(&setpoint, ORL_POSITION_LINK_RAD, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);

				}
			}
			else
			{
				// Copy current joint angles
				ORLOPEN_sync_position(&setpoint, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
				ORL_joints_conversion(&setpoint, ORL_POSITION_LINK_RAD, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);

			}
			break;

		default:
			break;

		}

		// Apply joint position control in degrees
		memcpy(&control, &setpoint, sizeof(control));
		ORL_joints_conversion(&control, ORL_POSITION_LINK_DEGREE, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
		
		ORLOPEN_set_absolute_pos_target_degree(&control, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);

		break;
	default:
		break;
	}

	if (flag_ExitFromOpen)
	{
		ORLOPEN_ExitFromOpen(ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
		flag_ExitFromOpen = false;
	}

	// Send feedback data to udp client
	long mask = ORLOPEN_GetOpenMask(ORL_SILENT, ORL_CNTRL01, ORL_ARM1);

	ORLOPEN_get_pos_measured_mr(&position, &mask, 0, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
	ORL_joints_conversion(&position, ORL_POSITION_LINK_RAD, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);

	ORLOPEN_get_speed_measured_mrpm(&velocity, &mask, 0, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
	ORL_joints_conversion(&velocity, ORL_SPEED_LINK_RAD_SEC, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
	
	// Send feedback to UDP user
	pthread_mutex_lock(&lock);
		udpSend.frameCounter += 1;

		for (int i = 0; i < 6; i++)
		{
			udpSend.q[i] = position.value[i];
			udpSend.qDot[i] = velocity.value[i];
		}

	pthread_mutex_unlock(&lock);
	

	return ORLOPEN_RES_OK;
}

