# ---------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------
import string 
import sys
import os
import maya.cmds as cmds
import maya.mel as mel
from pprint import pprint


# ---------------------------------------------------------------------------------------------
# reload scene textures
# ---------------------------------------------------------------------------------------------
sceneTex = cmds.ls(type = "file")
for entry in (sceneTex):
	reloadName =  entry+".fileTextureName"
	mel.eval("AEfileTextureReloadCmd %s" %reloadName)