# ------------------- Written by: Mike Kirylo, ------------------------------------------------
# ------------------- for Zoic Studios 
# ------------------- feb 28 2011
# ------------------- This script is meant to on rush a workstation from maya
# -------imports ------------------------------------
import sys
import os
import maya.cmds as cmds
import maya.mel as mel
# -----------------------------------------------------
# Paths
# -----------------------------------------------------
onrush  = "C:/RUSH/bin/onrush.exe"
maya = "C:/Program Files/Autodesk/Maya2012/bin"
# -----------------------------------------------------
def StartOnRush():
	os.system(onrush)