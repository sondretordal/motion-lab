#define GLOBAL_VAR_EXTERN
#include "config.h"

int callbackFunction(int period)
{
	char flag_new_modality, s_modality[40];

	// Input parameters
	double beta = 1.0;
	double omega = 1.0;
	double maxVel = 10.0/180.0*PI;

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
		ORLOPEN_sync_position(&Setpoint.Pos, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
		ORL_joints_conversion(&Setpoint.Pos, ORL_POSITION_LINK_RAD, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);

		for (int i = 0; i < 6; i++) {
			Setpoint.Vel.value[i] = 0.0;
			Setpoint.Acc.value[i] = 0.0;

			Reference.Vel.value[i] = 0.0;
			Reference.Acc.value[i] = 0.0;
		}

		break;

	case CRCOPEN_POS_ABSOLUTE:
		// Mode switch
		switch (mode)
		{
		case STOP_MODE:
			// Copy current joint angles
			ORLOPEN_sync_position(&Reference.Pos, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
			ORL_joints_conversion(&Reference.Pos, ORL_POSITION_LINK_RAD, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);

			for (int i = 0; i < 6; i++) {
				Reference.Vel.value[i] = 0.0;
				Reference.Acc.value[i] = 0.0;
			}

			break;

		case UDP_MODE:
			if (udpRecieve->udpKey == UDP_KEY  && udp_started == 1)
			{
				if (udpRecieve->mode == 1)
				{
					maxVel = 10.0/180.0*PI;
					// Read udp joint values				
					pthread_mutex_lock(&lock);
						Reference.Pos.value[0] = (double)udpRecieve->q1;
						Reference.Pos.value[1] = (double)udpRecieve->q2;
						Reference.Pos.value[2] = (double)udpRecieve->q3;
						Reference.Pos.value[3] = (double)udpRecieve->q4;
						Reference.Pos.value[4] = (double)udpRecieve->q5;
						Reference.Pos.value[5] = (double)udpRecieve->q6;
					pthread_mutex_unlock(&lock);
				}
				else if (udpRecieve->mode == 2)
				{
					maxVel = 40.0/180.0*PI;
					// Apply filter settings from host
					pthread_mutex_lock(&lock);
						beta = (double)abs(udpRecieve->beta);
						omega = (double)abs(udpRecieve->omega);

						// Read udp joint values
						Reference.Pos.value[0] = (double)udpRecieve->q1;
						Reference.Pos.value[1] = (double)udpRecieve->q2;
						Reference.Pos.value[2] = (double)udpRecieve->q3;
						Reference.Pos.value[3] = (double)udpRecieve->q4;
						Reference.Pos.value[4] = (double)udpRecieve->q5;
						Reference.Pos.value[5] = (double)udpRecieve->q6;
					pthread_mutex_unlock(&lock);
				}
				else
				{
					// Copy current joint angles
					ORLOPEN_sync_position(&Reference.Pos, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
					ORL_joints_conversion(&Reference.Pos, ORL_POSITION_LINK_RAD, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);

					for (int i = 0; i < 6; i++) {
						Reference.Vel.value[i] = 0.0;
						Reference.Acc.value[i] = 0.0;
					}
				}
			}
			else
			{
				// Copy current joint angles
				ORLOPEN_sync_position(&Reference.Pos, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
				ORL_joints_conversion(&Reference.Pos, ORL_POSITION_LINK_RAD, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);

				for (int i = 0; i < 6; i++) {
					Reference.Vel.value[i] = 0.0;
					Reference.Acc.value[i] = 0.0;
				}
			}
			break;

		default:
			break;
		}

		// Generate setpoint trajectory
		for (int i = 0; i < 6; i++){
			Setpoint.Acc.value[i] = Reference.Acc.value[i] + 2*beta*omega*(Reference.Vel.value[i] - Setpoint.Vel.value[i]) + omega*omega*(Reference.Pos.value[i] - Setpoint.Pos.value[i]);

			Setpoint.Vel.value[i] = Setpoint.Vel.value[i] + Setpoint.Acc.value[i]*dt;
			Setpoint.Vel.value[i] = Limit(Setpoint.Vel.value[i], maxVel, -maxVel);

			Setpoint.Pos.value[i] = Setpoint.Pos.value[i] + Setpoint.Vel.value[i]*dt;
		}

		// Copy and set output joints
		memcpy(&ControlInput.Pos, &Setpoint.Pos, sizeof(Setpoint.Pos));
		ORL_joints_conversion(&ControlInput.Pos, ORL_POSITION_LINK_DEGREE, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
		
		ORLOPEN_set_absolute_pos_target_degree(&ControlInput.Pos, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);

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

	ORLOPEN_get_pos_measured_mr(&Feedback.Pos, &mask, 0, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
	ORL_joints_conversion(&Feedback.Pos, ORL_POSITION_LINK_RAD, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);

	ORLOPEN_get_speed_measured_mrpm(&Feedback.Vel, &mask, 0, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
	ORL_joints_conversion(&Feedback.Vel, ORL_SPEED_LINK_RAD_SEC, ORL_SILENT, ORL_CNTRL01, ORL_ARM1);
	
	pthread_mutex_lock(&lock);
		udpSend.frameCounter += 1;	
		
		// Joint Control input after setpoint generator
		udpSend.q1_ref = Setpoint.Pos.value[0];
		udpSend.q2_ref = Setpoint.Pos.value[1];
		udpSend.q3_ref = Setpoint.Pos.value[2];
		udpSend.q4_ref = Setpoint.Pos.value[3];
		udpSend.q5_ref = Setpoint.Pos.value[4];
		udpSend.q6_ref = Setpoint.Pos.value[5];

		// Joint position feedback
		udpSend.q1 = Feedback.Pos.value[0];
		udpSend.q2 = Feedback.Pos.value[1];
		udpSend.q3 = Feedback.Pos.value[2];
		udpSend.q4 = Feedback.Pos.value[3];
		udpSend.q5 = Feedback.Pos.value[4];
		udpSend.q6 = Feedback.Pos.value[5];
		
		// Joint velocity feedback
		udpSend.q1_t = Feedback.Vel.value[0];
		udpSend.q2_t = Feedback.Vel.value[1];
		udpSend.q3_t = Feedback.Vel.value[2];
		udpSend.q4_t = Feedback.Vel.value[3];
		udpSend.q5_t = Feedback.Vel.value[4];
		udpSend.q6_t = Feedback.Vel.value[5];

		// Joint acceleration feedback
		udpSend.q1_tt = Feedback.Acc.value[0];
		udpSend.q2_tt = Feedback.Acc.value[1];
		udpSend.q3_tt = Feedback.Acc.value[2];
		udpSend.q4_tt = Feedback.Acc.value[3];
		udpSend.q5_tt = Feedback.Acc.value[4];
		udpSend.q6_tt = Feedback.Acc.value[5];
	pthread_mutex_unlock(&lock);
	

	return ORLOPEN_RES_OK;
}

