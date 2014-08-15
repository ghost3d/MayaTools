import sys
import os
import shutil
import getpass
import maya.cmds as cmds
import maya.mel as mel
from pprint import pprint

def awCreateMatteIDUI():
	if (cmds.window('awAddMaterialMultiMattes', exists=True) == True):
		cmds.deleteUI('awAddMaterialMultiMattes')
	awAddMMUI = cmds.loadUI (f = 'Q:/Tools/maya/2012/scripts/python/UI/awAddMultiMatteUI_02.ui')
	cmds.showWindow(awAddMMUI)
	awPopulateIDUI()
	
def findMatID():
	selected = cmds.ls(sl=True, mat=True)
	shaders = cmds.ls( mat=True)
	if not(len(selected) == 0):
		matList = selected
	if (len(selected) == 0):
		matList = shaders
	sceneMatID = []
	for mat in matList:
		findVrayMatID = cmds.listAttr( mat, r=True, st='vrayMaterialId')
		if not (findVrayMatID == None):
			nameFix = mat.replace(':','_')
			vrayMatID = cmds.getAttr(mat +".vrayMaterialId") 
			sceneMatID.append({'ID':vrayMatID,'name':nameFix})
	for dic in sceneMatID:
	    for anotherdic in sceneMatID:
	        if dic != anotherdic:
	            if dic['ID'] == anotherdic['ID']:
	                sceneMatID.remove(anotherdic)
	sceneMatID.sort
	return sceneMatID

def createMM( Type ):
	ID = []
	if (Type == 'mat'):
		temp = findMatID()
		for entry in temp:
			ID.append(entry['ID'])
	if (Type == 'obj'):
		temp = findVROPID()
		for entry in temp:
			ID.append(entry['ID'])
	for i in range (0, len(ID), 3):
		chunk = ID[i:i+3]
		makeMultiMatte = mel.eval("vrayAddRenderElement MultiMatteElement")
		if (Type == 'mat'):
			makeMultiMatte = cmds.rename (makeMultiMatte, ('matID_00'))
		if (Type == 'obj'):
			makeMultiMatte = cmds.rename (makeMultiMatte, ('objID_00'))
		cmds.setAttr (makeMultiMatte + ".vray_name_multimatte" , makeMultiMatte , type= "string")
		if (Type == 'mat'):
			cmds.setAttr (makeMultiMatte + ".vray_usematid_multimatte", 1)
		if (Type == 'obj'):
			cmds.setAttr (makeMultiMatte + ".vray_usematid_multimatte", 0)
		cmds.setAttr (makeMultiMatte + ".vray_considerforaa_multimatte", 1)
		if (len(chunk) == 3):
			cmds.setAttr (makeMultiMatte + ".vray_redid_multimatte", chunk[0])
			cmds.setAttr (makeMultiMatte + ".vray_greenid_multimatte", chunk[1])
			cmds.setAttr (makeMultiMatte + ".vray_blueid_multimatte", chunk[2])
		if (len(chunk) == 2):
			cmds.setAttr (makeMultiMatte + ".vray_redid_multimatte", chunk[0])
			cmds.setAttr (makeMultiMatte + ".vray_greenid_multimatte", chunk[1])
		if (len(chunk) == 1):
			cmds.setAttr (makeMultiMatte + ".vray_redid_multimatte", chunk[0])

def createMMSingleChannel( Type ):
	if (Type == 'mat'):
		ID = findMatID()
	if (Type == 'obj'):
		ID = findVROPID()
	for i in ID:
		makeMultiMatte = mel.eval("vrayAddRenderElement MultiMatteElement")
		if (Type == 'mat'):
			makeMultiMatte = cmds.rename (makeMultiMatte, ('ZmID_' + i['name'] ))
		if (Type == 'obj'):
			makeMultiMatte = cmds.rename (makeMultiMatte, ('ZoID_' + i['name'] ))
		cmds.setAttr (makeMultiMatte + ".vray_name_multimatte" , i['name'] , type= "string")
		cmds.setAttr (makeMultiMatte + ".vray_considerforaa_multimatte", 1)
		if (Type == 'mat'):
			cmds.setAttr (makeMultiMatte + ".vray_usematid_multimatte", 1)
			cmds.setAttr (makeMultiMatte + ".vray_redid_multimatte", i['ID'])
			cmds.setAttr (makeMultiMatte + ".vray_redon_multimatte", 1)
			cmds.setAttr (makeMultiMatte + ".vray_greenon_multimatte", 0)
			cmds.setAttr (makeMultiMatte + ".vray_blueon_multimatte", 0)
		if (Type == 'obj'):
			cmds.setAttr (makeMultiMatte + ".vray_usematid_multimatte", 0)
			cmds.setAttr (makeMultiMatte + ".vray_greenid_multimatte", i['ID'])
			cmds.setAttr (makeMultiMatte + ".vray_redon_multimatte", 0)
			cmds.setAttr (makeMultiMatte + ".vray_greenon_multimatte", 1)
			cmds.setAttr (makeMultiMatte + ".vray_blueon_multimatte", 0)
			
def findVROPID():
	selected = cmds.ls(sl=True, exactType='VRayObjectProperties')
	allVROP = cmds.ls(exactType='VRayObjectProperties')
	if not(len(selected) == 0):
		vropList = selected
	if (len(selected) == 0):
		vropList = allVROP
	sceneVROPID = []
	for vrop in vropList:
		findVrayVROPID = cmds.getAttr(vrop +".objectIDEnabled")
		if (findVrayVROPID == True):
			vrayObjID = cmds.getAttr(vrop +".objectID")
			sceneVROPID.append({'ID': vrayObjID, 'name':vrop})
	#sceneVROPID = list(set( sceneVROPID ))
	for dic in sceneVROPID:
	    for anotherdic in sceneVROPID:
	        if dic != anotherdic:
	            if dic['ID'] == anotherdic['ID']:
	                sceneVROPID.remove(anotherdic)
	sceneVROPID.sort()
	return sceneVROPID
	
def awPopulateIDUI():
	cmds.textScrollList('matID',e=True, ra=True)
	cmds.textScrollList('objID',e=True, ra=True)
	findMID = findMatID()
	findOID = findVROPID()
	mID = []
	oID = []
	for entry in findMID:
		mID.append((entry['name']) + " -- " + str(entry['ID']))
	for entry in findOID:
		oID.append((entry['name']) + " -- " + str(entry['ID']))
	cmds.textScrollList('matID',e=True, append = mID)
	cmds.textScrollList('objID',e=True, append = oID)