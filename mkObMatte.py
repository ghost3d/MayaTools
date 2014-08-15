#Object ID script, creates random mattes for each object or each refrence
## Written by Michael Kirylo 2011
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
sys.path.append( 'Q:/Tools/maya/2012/scripts/python' )
import mkVrayIndxMatte

# create a matte for eacy Obj
def mkObjIndx():
	mkObjList			=		cmds.ls(type='mesh')
	mkCreatVOP			=		"vray objectProperties add_single;"
	mkNum				=		getNum()
	mkNum				=		int(mkNum)
	print mkNum
	for i in range (len(mkObjList)):
		mkVOPlist		=		cmds.ls(type="VRayObjectProperties")
		if mkObjList[i]+"VOP" in mkVOPlist:
			print "vop already created for this object"
		else:
			mkNumber	=		str(mkNum)
			cmds.select(mkObjList[i])
			mel.eval(mkCreatVOP)
			mkrename	=		cmds.rename("vrayobjectproperties", mkObjList[i]+"VOP")
			cmds.setAttr(mkrename+".objectIDEnabled",1)
			mel.eval('setAttr "%s.objectID" %s;'%(mkrename,mkNumber))
			mkNum		=		mkNum + 1
def mkObjSlIndx():
	mkObjList			=		cmds.ls(sl=True)
	mkCreatVOP			=		"vray objectProperties add_single;"
	NameResult			=		cmds.promptDialog( title='Name of ObjectProperties node', message='Enter Name:', button=['OK', 'Cancel'], defaultButton='OK',cancelButton='Cancel', dismissString='Cancel')
	if NameResult == 'OK':
		mktext			=		cmds.promptDialog(query=True, text=True)
	IDResult = cmds.promptDialog( title='object ID number', message='Enter ID:', button=['OK', 'Cancel'], defaultButton='OK',cancelButton='Cancel', dismissString='Cancel')
	if IDResult == 'OK':
		mkID			=		cmds.promptDialog(query=True, text=True)
	mkID=int(mkID)
	if mkObjList == []:
		print "nothing selected"
	else:
		mkVOPlist		=		cmds.ls(type="VRayObjectProperties")
		if mktext+"VOP" in mkVOPlist:
			print "vop already created for this object"
		else:
			mel.eval(mkCreatVOP)
			mkrename	=		cmds.rename("vrayobjectproperties", mktext+"VOP")
			cmds.setAttr(mkrename+".objectID", mkID)
			cmds.setAttr(mkrename+".objectIDEnabled",1)
def getNum():
	mkStartNum			=	[]
	NameResult			=	cmds.promptDialog( title='StartNumber', message='Enter Start number:', button=['OK', 'Cancel'], defaultButton='OK',cancelButton='Cancel', dismissString='Cancel')
	if NameResult		==	'OK':
		mkStartNum		=	cmds.promptDialog(query=True, text=True)
	return mkStartNum