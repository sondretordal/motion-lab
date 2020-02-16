##############################################################################
# Beckhoff Automation GmbH & Co. KG
# TwinCAT Target for MATLAB/Simulink 1.2.1221.1
##############################################################################

#------------------------ system settings ------------------------------------
MSBUILDBINPATH = C:\Windows\Microsoft.NET\Framework\v4.0.30220
MODEL_NAME     = WaveSimulator0   
  
#------------------------ Macros read by make_tct -----------------------------
MAKECMD         = nmake
HOST            = PC
BUILD           = yes
SYS_TARGET_FILE = TwinCAT.tlc

#------------------------- Main Make-Targets ----------------------------------
all: 
    @echo ### Created TwinCAT module source file for build with MSBUILD
