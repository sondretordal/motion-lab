﻿// ****************** WaveSimulator0_types.h *******************************
// Generated by TwinCAT Target for MATLAB/Simulink (TE1400)
// MATLAB R2019a (win64)
// TwinCAT 3.1.4022
// TwinCAT Target 1.2.1237
// Beckhoff Automation GmbH & Co. KG     (www.beckhoff.com)
// *************************************************************
/*
 * WaveSimulator0_types.h
 *
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * Code generation for model "WaveSimulator0".
 *
 * Model version              : 1.866
 * Simulink Coder version : 9.1 (R2019a) 23-Nov-2018
 * C++ source code generated on : Fri Dec 20 06:06:43 2019
 *
 * Target selection: TwinCAT.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: Intel->x86-64 (Windows64)
 * Code generation objective: Execution efficiency
 * Validation result: Not run
 */

#ifndef RTW_HEADER_WaveSimulator0_types_h_
#define RTW_HEADER_WaveSimulator0_types_h_
#include "rtwtypes.h"
#include "multiword_types.h"
#include "zero_crossing_types.h"

/* Custom Type definition for MATLAB Function: '<S1>/PolePlacer' */
#ifndef struct_tag_sSGjtgAkySzprQicY751LpE
#define struct_tag_sSGjtgAkySzprQicY751LpE

struct tag_sSGjtgAkySzprQicY751LpE
{
  real_T t[20001];
  real_T u[20001];
  real_T y[20001];
  real_T Kss;
  real_T tau;
};

#endif                                 /*struct_tag_sSGjtgAkySzprQicY751LpE*/

#ifndef typedef_sSGjtgAkySzprQicY751LpE_WaveS_T
#define typedef_sSGjtgAkySzprQicY751LpE_WaveS_T

typedef struct tag_sSGjtgAkySzprQicY751LpE sSGjtgAkySzprQicY751LpE_WaveS_T;

#endif                               /*typedef_sSGjtgAkySzprQicY751LpE_WaveS_T*/

#ifndef struct_tag_sHd1RgFhFFbHSsLb0uGaiAF
#define struct_tag_sHd1RgFhFFbHSsLb0uGaiAF

struct tag_sHd1RgFhFFbHSsLb0uGaiAF
{
  sSGjtgAkySzprQicY751LpE_WaveS_T surge;
  sSGjtgAkySzprQicY751LpE_WaveS_T sway;
  sSGjtgAkySzprQicY751LpE_WaveS_T yaw;
};

#endif                                 /*struct_tag_sHd1RgFhFFbHSsLb0uGaiAF*/

#ifndef typedef_sHd1RgFhFFbHSsLb0uGaiAF_WaveS_T
#define typedef_sHd1RgFhFFbHSsLb0uGaiAF_WaveS_T

typedef struct tag_sHd1RgFhFFbHSsLb0uGaiAF sHd1RgFhFFbHSsLb0uGaiAF_WaveS_T;

#endif                               /*typedef_sHd1RgFhFFbHSsLb0uGaiAF_WaveS_T*/

#ifndef struct_tag_sbfhLDQO4tyWXbilgALyS7G
#define struct_tag_sbfhLDQO4tyWXbilgALyS7G

struct tag_sbfhLDQO4tyWXbilgALyS7G
{
  sHd1RgFhFFbHSsLb0uGaiAF_WaveS_T step;
};

#endif                                 /*struct_tag_sbfhLDQO4tyWXbilgALyS7G*/

#ifndef typedef_sbfhLDQO4tyWXbilgALyS7G_WaveS_T
#define typedef_sbfhLDQO4tyWXbilgALyS7G_WaveS_T

typedef struct tag_sbfhLDQO4tyWXbilgALyS7G sbfhLDQO4tyWXbilgALyS7G_WaveS_T;

#endif                               /*typedef_sbfhLDQO4tyWXbilgALyS7G_WaveS_T*/

/* Custom Type definition for MATLAB Function: '<S1>/StateSpaceModel' */
#ifndef struct_tag_sUhiAtiCAEQlyyJxooooSHD
#define struct_tag_sUhiAtiCAEQlyyJxooooSHD

struct tag_sUhiAtiCAEQlyyJxooooSHD
{
  real_T M[36];
  real_T Minv[36];
  real_T D[36];
  real_T G[36];
};

#endif                                 /*struct_tag_sUhiAtiCAEQlyyJxooooSHD*/

#ifndef typedef_sUhiAtiCAEQlyyJxooooSHD_WaveS_T
#define typedef_sUhiAtiCAEQlyyJxooooSHD_WaveS_T

typedef struct tag_sUhiAtiCAEQlyyJxooooSHD sUhiAtiCAEQlyyJxooooSHD_WaveS_T;

#endif                               /*typedef_sUhiAtiCAEQlyyJxooooSHD_WaveS_T*/

#ifndef struct_tag_sepW0InKR6DJka3SKNpSBrE
#define struct_tag_sepW0InKR6DJka3SKNpSBrE

struct tag_sepW0InKR6DJka3SKNpSBrE
{
  sUhiAtiCAEQlyyJxooooSHD_WaveS_T supply;
};

#endif                                 /*struct_tag_sepW0InKR6DJka3SKNpSBrE*/

#ifndef typedef_sepW0InKR6DJka3SKNpSBrE_WaveS_T
#define typedef_sepW0InKR6DJka3SKNpSBrE_WaveS_T

typedef struct tag_sepW0InKR6DJka3SKNpSBrE sepW0InKR6DJka3SKNpSBrE_WaveS_T;

#endif                               /*typedef_sepW0InKR6DJka3SKNpSBrE_WaveS_T*/

/* Parameters (default storage) */
typedef struct P_WaveSimulator0_T_ P_WaveSimulator0_T;

/* Forward declaration for rtModel */
typedef struct tag_RTM_WaveSimulator0_T RT_MODEL_WaveSimulator0_T;

#endif                                 /* RTW_HEADER_WaveSimulator0_types_h_ */
