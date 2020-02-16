/*
 * HydroSimulator_data.cpp
 *
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * Code generation for model "HydroSimulator".
 *
 * Model version              : 1.867
 * Simulink Coder version : 9.1 (R2019a) 23-Nov-2018
 * C++ source code generated on : Fri Dec 20 06:07:41 2019
 *
 * Target selection: TwinCAT.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: Intel->x86-64 (Windows64)
 * Code generation objective: Execution efficiency
 * Validation result: Not run
 */

#include "HydroSimulator.h"
#include "HydroSimulator_private.h"

/* Block parameters (default storage) */
P_HydroSimulator_T HydroSimulator_P = {
  /* Mask Parameter: DPController_InitialConditionFo
   * Referenced by: '<S33>/Filter'
   */
  0.0,

  /* Mask Parameter: DetectRisePositive_vinit
   * Referenced by: '<S53>/Delay Input1'
   */
  0,

  /* Expression: inf
   * Referenced by: '<S5>/Saturation'
   */
  0.0,

  /* Expression: 1e-6
   * Referenced by: '<S5>/Saturation'
   */
  1.0E-6,

  /* Expression: 1
   * Referenced by: '<S5>/Unit Delay'
   */
  1.0,

  /* Expression: 1
   * Referenced by: '<S5>/Saturation1'
   */
  1.0,

  /* Expression: 1e-10
   * Referenced by: '<S5>/Saturation1'
   */
  1.0E-10,

  /* Expression: zeros(6,1)
   * Referenced by: '<S1>/Integrator1'
   */
  { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 },

  /* Expression: zeros(6,1)
   * Referenced by: '<S1>/Integrator'
   */
  { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 },

  /* Expression: x0
   * Referenced by: '<S8>/Integrator'
   */
  { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 },

  /* Expression: zeros(6,1)
   * Referenced by: '<S1>/Random Sequence'
   */
  { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 },

  /* Computed Parameter: RandomSequence_StdDev
   * Referenced by: '<S1>/Random Sequence'
   */
  { 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 },

  /* Expression: [0,20,500,9000,400,200]
   * Referenced by: '<S1>/Random Sequence'
   */
  { 0.0, 20.0, 500.0, 9000.0, 400.0, 200.0 },

  /* Expression: [1e4,1e4,1e8,1e7,1e8,1e3]'
   * Referenced by: '<S1>/Gain'
   */
  { 10000.0, 10000.0, 1.0E+8, 1.0E+7, 1.0E+8, 1000.0 },

  /* Expression: zeros(6,1)
   * Referenced by: '<S1>/u'
   */
  { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 },

  /* Expression: [0.2, 0.2, 0, 0, 0, 5/180*pi]
   * Referenced by: '<S1>/Input Saturation'
   */
  { 0.2, 0.2, 0.0, 0.0, 0.0, 0.087266462599716474 },

  /* Expression: -[0.2, 0.2, 0, 0, 0, 5/180*pi]
   * Referenced by: '<S1>/Input Saturation'
   */
  { -0.2, -0.2, -0.0, -0.0, -0.0, -0.087266462599716474 },

  /* Expression: -30
   * Referenced by: '<S1>/poles'
   */
  -30.0,

  /* Expression: 0
   * Referenced by: '<S1>/Poles Saturation'
   */
  0.0,

  /* Expression: -30
   * Referenced by: '<S1>/Poles Saturation'
   */
  -30.0,

  /* Expression: ones(6,1)
   * Referenced by: '<S5>/Constant'
   */
  { 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 },

  /* Computed Parameter: Constant_Value_l
   * Referenced by: '<S55>/Constant'
   */
  0
};
