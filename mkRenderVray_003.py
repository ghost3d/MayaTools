# ------------------- Written by: Mike Kirylo, ------------------------------------------------
# ------------------- for Zoic Studios 
# ------------------- Oct 24 2011
# ------------------- This script is meant to render using vray stand alone locally
# -------imports ------------------------------------
import sys
import time
import pprint
import os
import maya.cmds as cmds
import maya.mel as mel
# -----------------------------------------------------
# Paths
# -----------------------------------------------------
vray					=		'"C:/Program Files/Autodesk/Maya2012/vray/bin/"'
exrconv					=		'"C:/Program Files/Chaos Group/V-Ray/Maya 2012 for x64/bin/"'
# -----------------------------------------------------
# export all
# -----------------------------------------------------
def mkexportAll():
	VrayScene			=		mkVrayVrscene("1")
	vrayCmd				=		"vray.exe -sceneFile="+VrayScene+' -display = 1 -autoClose=0 -verboseLevel = 4 -displaySRGB = 1 -imgFile= '
	vrayRender(vrayCmd)
# -----------------------------------------------------
# do not export geo 
# -----------------------------------------------------
def mkexportGeoOff():
	VrayScene			=		mkVrayVrscene("0")
	vrayCmd				=		"vray.exe -sceneFile="+VrayScene+' -display = 1 -autoClose=0 -verboseLevel = 4 -displaySRGB = 1 -imgFile= '
	vrayRender(vrayCmd)
	
def mkexportAllSaveImage(image):
	VrayScene			=		mkVrayVrscene("1")
	vrayCmd				=		"vray.exe -sceneFile="+VrayScene+' -display = 1  -autoClose=0 -verboseLevel = 4 -displaySRGB = 0 -imgFile= %s'%(image)
	vrayRender(vrayCmd)
def mkexportAllSaveVrimg():
	files				=	cmds.file(query=1, list=1, withoutCopyNumber=1)
	thumbFileName		=	files[0].replace( '.mb', '.vrimg' )
	batFileName			=	files[0].replace( '.mb', '.bat' )
	batfile				= ("%s")%batFileName
	VrayScene			=		mkVrayVrscene("1")
	vrayCmd				=		"vray.exe -sceneFile="+VrayScene+' -display = 1  -autoClose=0 -verboseLevel = 4 -displaySRGB = 0 -imgFile= %s'%(thumbFileName)
	vrayRender(vrayCmd)
	t = 0
	while (t < 5000 ):
		try:
			os.rename (thumbFileName,thumbFileName)
		except:
			time.sleep(5)
		t+=1
	vrimg2exr(thumbFileName,batfile)
	exrimg = thumbFileName.replace( '.vrimg', '.exr' )
	time.sleep(2)
	if os.path.exists( exrimg ) == True:
		cmds.sysFile(batfile, delete = True)
		cmds.sysFile(thumbFileName, delete = True)

# -----------------------------------------------------
# use vray RT
# -----------------------------------------------------
def mkexportRT():
	NameResult			=		cmds.promptDialog( title='duration', message='Enter Duration 0.0', button=['OK', 'Cancel'], defaultButton='OK',cancelButton='Cancel', dismissString='Cancel')
	if NameResult		==		'OK':
		mkDuration		=		cmds.promptDialog(query=True, text=True)
	# mkDuration = float(mkDuration)
	VrayScene			=		mkVrayVrscene("1")
	VrayCmd				=		"vray.exe -sceneFile="+VrayScene+' -display=1 -autoClose=0 -verboseLevel = 4 -rtEngine = 1 -rtTimeOut ='+mkDuration+' -displaySRGB = 1 -imgFile="C:/Temp/vrayRTTemp.exr"'
	vrayRender(VrayCmd)
# -----------------------------------------------------
# creat vrscene file
# -----------------------------------------------------
def mkVrayVrscene(num):
	mkVrayRenderOff		=		'setAttr "vraySettings.vrscene_render_on" 0;'
	mkVrayVrsceneOn		=		'setAttr "vraySettings.vrscene_on" 1;'
	mkVrayTempPath		=		'setAttr -type "string" vraySettings.vrscene_filename "c:/temp/vrayTemp";'
	mkVrsettingSepOn	=		'setAttr "vraySettings.misc_separateFiles" 1;'
	mkGeoOn				=		'setAttr "vraySettings.misc_exportGeometry"'+num+';'
	mel.eval(mkVrayRenderOff)
	mel.eval(mkVrayVrsceneOn)
	mel.eval(mkVrsettingSepOn)
	mel.eval(mkGeoOn)
	mel.eval(mkVrayTempPath)
	getCurrentRenderLayer = cmds.editRenderLayerGlobals(q=True,currentRenderLayer=True)
	print getCurrentRenderLayer
	mkLayers			=		cmds.ls(type ="renderLayer")
	if (len(mkLayers)	!=		1):
		if (getCurrentRenderLayer == "defaultRenderLayer"):
			vrsceneName		=		'"c:/temp/vrayTemp_masterLayer.vrscene"'
		else:
			vrsceneName		=		'"'+"c:/temp/vrayTemp"+"_"+getCurrentRenderLayer+".vrscene"+'"'
	else:
		vrsceneName		=		'"c:/temp/vrayTemp.vrscene"'
	print vrsceneName
	return vrsceneName
# -----------------------------------------------------
# render Vrscene file
# -----------------------------------------------------
def vrayRender (Vcmd):
	mkVrayRenderOn		=		'setAttr "vraySettings.vrscene_render_on" 1;'
	mkVrayVrsceneOff	=		'setAttr "vraySettings.vrscene_on" 0;'
	renderCmd			=		'RenderIntoNewWindow;'+'renderIntoNewWindow render;'
	mel.eval(renderCmd)
	bat					=		[]
	cDrive				=		'c:'
	cmdPath				=		'cd "C:/Program Files/Autodesk/Maya2012/vray/bin/" '
	vrayExeCmd			=		Vcmd
	bat.append (cDrive)
	bat.append (cmdPath)
	bat.append (vrayExeCmd)
	batFile				=		open('C:/TEMP/vray.bat', 'w')
	for entry in bat:
		batFile.write(entry + '\n')
	batFile.close()
	mel.eval(mkVrayVrsceneOff)
	mel.eval(mkVrayRenderOn)
	cmd					=		"C:/Temp/vray.bat"
	cmd					=		"exec (\"" + cmd + "\")"
	mel.eval(cmd)
def vrimg2exr (image,filename):
	bat					=		[]
	cDrive				=		'c:'
	cmdPath				=		'cd %s'%(exrconv)
	vrayExeCmd			=		'vrimg2exr "%s" -half -compression zips'%(image)
	bat.append (cDrive)
	bat.append (cmdPath)
	bat.append (vrayExeCmd)
	batFile				=		open(filename, 'w')
	for entry in bat:
		batFile.write(entry + '\n')
	batFile.close()
	cmd					=		filename
	cmd					=		"exec (\"" + cmd + "\")"
	mel.eval(cmd)