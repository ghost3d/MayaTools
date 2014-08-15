# ------------------- Written by: Mike Kirylo, ------------------------------------------------
# ------------------- for Zoic Studios 
# ------------------- Oct 24 2011
# ------------------- This script is meant to render using vray stand alone locally
# -------imports ------------------------------------
import sys
import os
import maya.cmds as cmds
import maya.mel as mel
# export Vrscene file get current render layer
def mkexportAll():
	VrayScene = mkVrayVrscene("1")
	vrayCmd = "vray.exe -sceneFile="+VrayScene+' -display = 1 -autoClose=0 -verboseLevel = 4 -displaySRGB = 1 -imgFile= '
	vrayRender(vrayCmd)
def mkexportGeoOff():
	VrayScene = mkVrayVrscene("0")
	vrayCmd = "vray.exe -sceneFile="+VrayScene+' -display = 1 -autoClose=0 -verboseLevel = 4 -displaySRGB = 1 -imgFile= '
	vrayRender(vrayCmd)
def mkexportRT():
	NameResult = cmds.promptDialog( title='duration', message='Enter Duration 0.0', button=['OK', 'Cancel'], defaultButton='OK',cancelButton='Cancel', dismissString='Cancel')
	if NameResult == 'OK':
		mkDuration = cmds.promptDialog(query=True, text=True)
	# mkDuration = float(mkDuration)
	VrayScene = mkVrayVrscene("1")
	VrayCmd = "vray.exe -sceneFile="+VrayScene+' -display=1 -autoClose=0 -verboseLevel = 4 -rtEngine = 1 -rtTimeOut ='+mkDuration+' -displaySRGB = 1 -imgFile="C:/Temp/vrayRTTemp.exr"'
	vrayRender(VrayCmd)
def mkVrayVrscene(num):
	mkVrayRenderOff = 'setAttr "vraySettings.vrscene_render_on" 0;'
	mkVrayVrsceneOn = 'setAttr "vraySettings.vrscene_on" 1;'
	mkVrayTempPath =  'setAttr -type "string" vraySettings.vrscene_filename "c:/temp/vrayTemp";'
	mkVrsettingSepOn ='setAttr "vraySettings.misc_separateFiles" 1;'
	mkGeoOn= 'setAttr "vraySettings.misc_exportGeometry"'+num+';'
	mel.eval(mkVrayRenderOff)
	mel.eval(mkVrayVrsceneOn)
	mel.eval(mkVrsettingSepOn)
	mel.eval(mkGeoOn)
	mel.eval(mkVrayTempPath)
	getCurrentRenderLayer = cmds.editRenderLayerGlobals(q=True,currentRenderLayer=True)
	print getCurrentRenderLayer
	if (getCurrentRenderLayer == "defaultRenderLayer"):
		vrsceneName ='"c:/temp/vrayTemp.vrscene"'
	else:
		vrsceneName ='"'+"c:/temp/vrayTemp"+"_"+getCurrentRenderLayer+".vrscene"+'"'
	return vrsceneName
# render Vrscene file
def vrayRender (Vcmd):
	mkVrayRenderOn =  'setAttr "vraySettings.vrscene_render_on" 1;'
	mkVrayVrsceneOff= 'setAttr "vraySettings.vrscene_on" 0;'
	renderCmd ='RenderIntoNewWindow;'+'renderIntoNewWindow render;'
	mel.eval(renderCmd)
	bat = []
	cDrive ='c:'
	cmdPath ='cd "C:/Program Files/Autodesk/Maya2012/vray/bin/" '
	vrayExeCmd = Vcmd
	bat.append (cDrive)
	bat.append (cmdPath)
	bat.append (vrayExeCmd)
	batFile = open('C:/TEMP/vray.bat', 'w')
	for entry in bat:
		batFile.write(entry + '\n')
	batFile.close()
	mel.eval(mkVrayVrsceneOff)
	mel.eval(mkVrayRenderOn)
	cmd = "C:/Temp/vray.bat"
	cmd = "exec (\"" + cmd + "\")"
	mel.eval(cmd)