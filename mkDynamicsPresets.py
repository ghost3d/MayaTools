import sys
import os
import shutil
import getpass
import maya.cmds as cmds
import maya.mel as mel
import distutils
from distutils.dir_util import copy_tree
from pprint import pprint
import getpass
sys.path.append( 'Q:/Tools/maya/2012/scripts/python' )
#----------------------------------------------------
# paths
#----------------------------------------------------
userName				=	getpass.getuser()
localPresetPath			=	'C:/Users/'+userName+'/Documents/maya/2012-x64/presets/attrPresets/'
#----------------------------------------------------
# share Preset settings
#----------------------------------------------------
def PresetUI():
	if cmds.dockControl('PresetUI', exists=True):
		cmds.deleteUI('PresetUI', ctl=True)
	mkPresetUI = cmds.loadUI (f = 'Q:/Tools/maya/2012/scripts/python/UI/mkPresets.ui')
	cmds.showWindow(mkPresetUI)

def mkSharePreset():
	fileInfo			=			mkFileInfo()
	project				=			mkProjName(fileInfo)
	mkDir				=			project+"/assets/3D/data/Scripts/Presets/attrPresets/"
	if not os.path.exists(mkDir):
		os.makedirs(mkDir)
	return mkDir
def mkCopyPresets():
	print userName
	dstFile				=			mkSharePreset()
	presetfiles			=			cmds.getFileList( folder=localPresetPath )
	for entry in presetfiles:
		presetFullPath	=			localPresetPath + entry
		distutils.dir_util.copy_tree( presetFullPath,dstFile + entry )
	print ("files copied to " + dstFile)
def mkSyncPresets():
	dstFile				=			mkSharePreset()
	presetfiles			=			cmds.getFileList( folder=dstFile)
	for entry in presetfiles:
		presetFullPath	=			dstFile + entry
		distutils.dir_util.copy_tree( presetFullPath, localPresetPath + entry )
	print ("files copied to " + localPresetPath)
		
#----------------------------------------------------
# get file info
#----------------------------------------------------
def mkFileInfo():
	fileInfo		=			cmds.file ( q = True, sceneName = True)
	if fileInfo == "":
		cmds.warning( 'no scene open')
	else:
		fileInfo	=			fileInfo.split ( "/" )
		return fileInfo
def mkProjName(fileInfo):
	ProjInfo = fileInfo[0:3]
	ProjInfo="/".join(ProjInfo)
	return ProjInfo
