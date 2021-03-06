﻿// ****************** CHydroSimulator.h *******************************
// Generated by TwinCAT Target for MATLAB/Simulink (TE1400)
// MATLAB R2019a (win64)
// TwinCAT 3.1.4022
// TwinCAT Target 1.2.1237
// Beckhoff Automation GmbH & Co. KG     (www.beckhoff.com)
// *************************************************************

#pragma once

#include "rtwtypes.h"
#include "TcPch.h"
#include "TcMatSim.h"
#include "TcIoInterfaces.h"
#include "TcInterfaces.h"
#include "TcRtInterfaces.h"
#include "HydroSimulatorInterfaces.h"
#include "HydroSimulator.h"








typedef struct{
	CLSID ClassId;
	unsigned int BuildTimeStamp;
	unsigned int ModelCheckSum[4];
	unsigned int ModelVersion[4];
	unsigned int TwinCatVersion[4];
	unsigned int TcTargetVersion[4];
	unsigned int MatlabVersion[4];
	unsigned int SimulinkVersion[4];
	unsigned int CoderVersion[4];
	GUID TcTargetLicenseId;
} TctModuleInfoType;

typedef struct{
	bool Debug;
} TctModuleBuildInfoType;


///////////////////////////////////////////////////////////////////////////////
// Module class
///////////////////////////////////////////////////////////////////////////////
class CHydroSimulator:
  public ITcCyclic,
  public ITcPostCyclic,
  public ITcADI,
  public ITcWatchSource,
  public CTcMatSimModuleBase
{
public:
	DECLARE_IUNKNOWN()
	DECLARE_IPERSIST(CID_HydroSimulator)
	DECLARE_ITCOMOBJECT_SETSTATE()
	DECLARE_PARA();

	CHydroSimulator();
	~CHydroSimulator();

	static int GetInstanceCnt();
	
	// ITcCyclic
	HRESULT TCOMAPI CycleUpdate(ITcTask* ipTask, ITcUnknown* ipCaller, ULONG_PTR context);

	// ITcPostCyclic
	HRESULT TCOMAPI PostCyclicUpdate(ITcTask* ipTask, ITcUnknown* ipCaller, ULONG_PTR context);

	// ITcADI
	DECLARE_ITCADI();

	// ITcWatchSource
	DECLARE_ITCWATCHSOURCE();
	
	// parameters and signals
	bool m_CycleUpdateExecuted;
	TctModuleInfoType m_ModuleInfo;
	TctModuleBuildInfoType m_ModuleBuildInfo;
	RT_MODEL_HydroSimulator_T m_SimStruct;
	ExtU_HydroSimulator_T m_Input;
	ExtY_HydroSimulator_T m_Output;
	B_HydroSimulator_T m_BlockIO;
	P_HydroSimulator_T m_ModelParameters;
	DW_HydroSimulator_T m_DWork;
	X_HydroSimulator_T m_ContState;

	
private:

	// private methods
    DECLARE_OBJPARAWATCH_MAP();
    DECLARE_OBJDATAAREA_MAP();
	HRESULT InitMembers();
	HRESULT CheckAndAdaptCycleTimes();
	
	void rate_scheduler (void);
	void rt_ertODEUpdateContinuousStates (RTWSolverInfo *si );
	real_T rt_urand_Upu32_Yd_f_pw_snf (uint32_T *u);
	real_T rt_nrand_Upu32_Yd_f_pw_snf (uint32_T *u);
	void HydroSimulator_output (void);
	void HydroSimulator_update (void);
	void HydroSimulator_derivatives (void);
	void HydroSimulator_initialize (void);
	void HydroSimulator_terminate (void);
	void rt_ODECreateIntegrationData (RTWSolverInfo *si);
	void rt_ODEDestroyIntegrationData (RTWSolverInfo *si);
	void rt_ODEUpdateContinuousStates (RTWSolverInfo *si);
	void MdlOutputs (int_T tid);
	void MdlUpdate (int_T tid);
	void MdlInitializeSizes (void);
	void MdlInitializeSampleTimes (void);
	void MdlInitialize (void);
	void MdlStart (void);
	void MdlTerminate (void);
	RT_MODEL_HydroSimulator_T* HydroSimulator (void);
	real_T rtGetInf (void);
	real32_T rtGetInfF (void);
	real_T rtGetMinusInf (void);
	real32_T rtGetMinusInfF (void);
	real_T rtGetNaN (void);
	real32_T rtGetNaNF (void);
	void rt_InitInfAndNaN (size_t realSize);
	boolean_T rtIsInf (real_T value);
	boolean_T rtIsInfF (real32_T value);
	boolean_T rtIsNaN (real_T value);
	boolean_T rtIsNaNF (real32_T value);


	// static members
	static int _InstanceCnt;

};
