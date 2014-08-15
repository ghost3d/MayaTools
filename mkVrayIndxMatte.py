## Written by Michael Kirylo 2011
## Create Vray Muli matte elements
## -------imports ------------------------------------
import sys
import os
import shutil
import maya.cmds as cmds
import glob
import time
import operator
import random
import maya.mel as mel
from pprint import pprint

#get Vray obj properties in scene, and Object id's
def mkVrayIndx ():
	mkObjectId=[]
	mkVobjProp= cmds.ls( type=  "VRayObjectProperties")
	for i in range (len(mkVobjProp)):
		MkObjID = cmds.getAttr(mkVobjProp[i]+".objectID")
		MkObjID=str(MkObjID)
		mkObjectId.insert(i,MkObjID)
		mkObjectId.sort()
	# create multi matte elements
	for i in range (0,len(mkVobjProp),3):
		mkVrayMMcom= "vrayAddRenderElement MultiMatteElement;"
		mkRenameIndx ="rename vrayRE_Multi_Matte "+'"'+"VOPmatte_0"+'"'+ ";"
		mel.eval(mkVrayMMcom)
		mel.eval(mkRenameIndx)
	cmds.select("VOPmatte*")
	mkMultiMat = cmds.ls(sl=True)
	for i in range (len (mkMultiMat)):
		mkRenameMname= "setAttr -type "+'"'+"string"+'"'+mkMultiMat[i]+".vray_name_multimatte "+'"'+"VOPmatte"+"%d" %i+'"'+";"
		mel.eval(mkRenameMname)
	# apply obj ID
	mkObjIter = iter(mkObjectId)
	for i in range(0,len(mkObjectId),3):
		for x in range (len(mkMultiMat)):
			mkObjIDred ="setAttr "+'"'+mkMultiMat[x]+".vray_redid_multimatte" +'"'+mkObjIter.next()+";"
			mel.eval(mkObjIDred)
			mkObjIDgreen ="setAttr "+'"'+mkMultiMat[x]+".vray_greenid_multimatte" +'"'+mkObjIter.next()+";"
			mel.eval(mkObjIDgreen)
			mkObjIDblue ="setAttr "+'"'+mkMultiMat[x]+".vray_blueid_multimatte" +'"'+mkObjIter.next()+";"
			mel.eval(mkObjIDblue)
