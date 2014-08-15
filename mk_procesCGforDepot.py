# ------------------- Written by: Mike Kirylo, ------------------------------------------------
# ------------------- for Zoic Studios 
# ------------------- jan 3 2011
# ------------------- saves maya content to the depot
# -------imports ------------------------------------
import sys
import os
import maya.cmds as cmds
import glob
import shutil
sys.path.append( '//silo/prod/Tools/Shotgun/Scripts/python/' )
sys.path.append( '//silo/prod/Tools/maya/2012/scripts/python/' )
# --------------------------------------------------------
# global paths
# --------------------------------------------------------
assetFolder = "Q:/Tools/eng/depot/downloads/031512/D3D-IndoorPlants_Maya_V4/Maya_V4/"
# --------------------------------------------------------
# grab all files
# --------------------------------------------------------
def mkFileList():
	for files in os.listdir(assetFolder):
		filename, fileExtension = os.path.splitext(files)
		filedir = assetFolder+filename
		file = assetFolder+files
		os.makedirs(filedir)
		print filedir
		print file
		shutil.move(file,filedir)
mkFileList()
