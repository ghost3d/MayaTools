# Written by Michael Kirylo 2011
# Create Vray material ID
# -------imports ------------------------------------
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
# -----------------------------------------------------
# create material Attribute and multimattes
# -----------------------------------------------------
def mkCreateMatID():
	mkSelItems		=	mkSelection()
	mkAddIDAttr(mkSelItems,"1",1)
def mkCreateMM():
	mkSelItems		=	mkAllshaders()
	mkGetShdrnumbers(mkSelItems)
def mkGroupID():
	mkSelItems		=	mkSelection()
	mkAddIDAttr(mkSelItems,"1",0)
# -----------------------------------------------------
# remove ID's 
# -----------------------------------------------------
def mkRemoveMatID():
	mkSelItems		=	mkSelection()
	mkAddIDAttr(mkSelItems,"0",1)
def mkRemoveAllMatID():
	mkSelItems		=	mkAllshaders()
	mkAddIDAttr(mkSelItems,"0",1)
# -----------------------------------------------------
# find Shaders
# -----------------------------------------------------
def mkSelection():
	mkSel			=	cmds.ls(sl=True)
	return mkSel
def mkAllshaders():
	mkAllShdr		=	cmds.ls(mat = True)
	return mkAllShdr
# -----------------------------------------------------
# add vray attribute to shaders
# -----------------------------------------------------
def mkAddIDAttr(item,num,type):
	for entry in (item):
		mkattr			=	'vray addAttributesFromGroup %s  vray_material_id %s;'%(entry, num)
		mkcolorAttr		=	'vrayAddAttr  %s vrayColorId;vrayAddAttr %s vrayMaterialId;'%(entry, entry)
		mkUIT			=	'setUITemplate -pst attributeEditorTemplate;'
		mel.eval(mkattr)
		mel.eval(mkcolorAttr)
		mel.eval(mkUIT)
	if num				==	"1" :
		mkAddMatID(item,type)
# -----------------------------------------------------
# add ID number to shaders 
# -----------------------------------------------------
def mkAddMatID(item,type):
	mkStartNum			=	[]
	NameResult			=	cmds.promptDialog( title='StartNumber', message='Enter Start number:', button=['OK', 'Cancel'], defaultButton='OK',cancelButton='Cancel', dismissString='Cancel')
	if NameResult		==	'OK':
		mkStartNum		=	cmds.promptDialog(query=True, text=True)
	mkStartNum			=	int(mkStartNum)
	for entry in (item):
		mkStartNumStr	=	str(mkStartNum)
		mkAddIDCmd		=	'setAttr "%s.vrayMaterialId" %s;'%(entry,mkStartNumStr)
		mel.eval (mkAddIDCmd)
		mkStartNum = mkStartNum + type
# -----------------------------------------------------
# find material id numbers in scene
# -----------------------------------------------------
def mkGetShdrnumbers(shdrList):
	IDlist				=	[]
	for i in range (len(shdrList)):
		try:
			mkIDNum		=	'getAttr("'+shdrList[i]+'.vrayMaterialId")'
			mk_id		=	mel.eval(mkIDNum)
			mk_id		=	str(mk_id)
			IDlist.insert(i,mk_id)
		except:
			print "no id assigned"
	if IDlist:
		IDlist.sort()
		last			=	IDlist[-1]
		for i in range (len(IDlist)-2,-1,-1):
			if last		==	IDlist[i]:
				del IDlist[i]
			else:
				last	=	IDlist[i]
	createMM(IDlist)
# -----------------------------------------------------
# create vray render elements 
# -----------------------------------------------------
def createMM(list):
	for i in range (0,len(list),3):
		mel.eval ("vrayAddRenderElement MultiMatteElement;")
		mel.eval ("rename vrayRE_Multi_Matte "+'"'+"MatID_01"+'"'+ ";")
	cmds.select("MatID*")
	mkMatID				=	cmds.ls(sl=True)
	for i in range (len (mkMatID)):
		mel.eval ("setAttr "+'"'+ mkMatID[i]+'.vray_usematid_multimatte" 1;')
		mel.eval ("setAttr -type "+'"'+"string"+'"'+mkMatID[i]+".vray_name_multimatte "+'"'+"MatID"+"%d" %i+'"'+";")
		mkObjIter = iter(list)
	for i in range(0,len(list),3):
		for entry in (mkMatID):
			mel.eval ("setAttr "+'"'+entry+".vray_redid_multimatte" +'"'+mkObjIter.next()+";")
			mel.eval ("setAttr "+'"'+entry+".vray_greenid_multimatte" +'"'+mkObjIter.next()+";")
			mel.eval ("setAttr "+'"'+entry+".vray_blueid_multimatte" +'"'+mkObjIter.next()+";")