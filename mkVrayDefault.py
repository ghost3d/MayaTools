# ------------------- Written by: Mike Kirylo, ------------------------------------------------
# ------------------- for Zoic Studios 
# ------------------- jan 3 2011
# ------------------- set default Vray settings
# -------imports ------------------------------------
import sys
import os
import maya.cmds as cmds
import maya.mel as mel
import maya
import zlib
import zipfile
import maya.cmds as cmds
import shutil
import glob
sys.path.append( '//silo/prod/Tools/Shotgun/Scripts/python/' )

def vrayDefault():
	cmds.setAttr ("vraySettings.sRGBOn", 1)
	# cmds.setAttr ("vraySettings.vfbOffBatch", 0)
	cmds.setAttr ("vraySettings.cmap_adaptationOnly", 0)
	cmds.setAttr ("vraySettings.dmcMinSubdivs", 1)
	cmds.setAttr ("vraySettings.dmcMaxSubdivs", 5)
	cmds.setAttr ("vraySettings.dmcThreshold", 0.01)
	cmds.setAttr ("vraySettings.cmap_linearworkflow", 0)
	cmds.setAttr ("vraySettings.cmap_gamma", 2.2)
	cmds.setAttr ("vraySettings.dmcs_adaptiveAmount", .9)
	cmds.setAttr ("vraySettings.sys_low_thread_priority", 0)
	cmds.setAttr ("vraySettings.dontSaveImage", 1)
	cmds.setAttr ("vraySettings.cmap_adaptationOnly", 0)