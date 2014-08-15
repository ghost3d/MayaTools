# ------------------- Written by: Mike Kirylo, ------------------------------------------------
# ------------------- for Zoic Studios 
# ------------------- jan 3 2011
# ------------------- changes resolution of baked textures on selected nodes
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
import fnmatch
sys.path.append( 'Q:/Tools/Shotgun/Scripts/python/' )
# --------------------------------------------------------
# global variables
ShaderList	=	[]
FileTex		=	[]
OrgTex		=	[]
newTex		=	[]
# --------------------------------------------------------
def mkGetshader(newRez):
	mkSel	=	cmds.ls(sl	=	True)
	orgRez	=	"128"
	for entry in mkSel:
		entry = entry+"_Bake"
		ShaderList.append(entry)
		mkFileTex = cmds.listConnections( entry+".color",type = "file")
		FileTex.append(mkFileTex[0])
	for entry in FileTex:
		fileNames	=	cmds.getAttr(entry+".fileTextureName")
		OrgTex.append(fileNames)
	print OrgTex
	for entry in OrgTex:
		newRes= entry.replace( orgRez, newRez )
		newTex.append(newRes)
	for i in range (len(newTex)):
		cmds.setAttr(FileTex[i]+".fileTextureName",newTex[i],type="string")