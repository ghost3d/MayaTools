# -------imports ------------------------------------
import sys
import time
import pprint
import os
import maya.cmds as cmds
import maya.mel as mel
from zoic_api.gui import CustomDialog
from PySide import QtGui
# -----------------------------------------------------
# Paths
# -----------------------------------------------------
TEMP_PATH				= 		'C:/temp/vrsceneFiles/'
# -----------------------------------------------------
# Build UI
# -----------------------------------------------------
def vrayStndAloneUI():
	parent = QtGui.QApplication.activeWindow()
	dlg = CustomDialog("Render Vray Stand Alone",parent=parent)
	dlg.addDescription("Render with Vray Stand alone. use this tool to test your scene file with Vray stand alone.")
	Modes = ['standard','preview','draft','SaveExr']
	dlg.addComboBox("Vray Modes", Modes)
	dlg.addButton("Apply") # Buttons always go on the bottom
	dlg.addButton("Cancel") # Each button gets and index value returned on exit
	result = dlg.show() # result will be 0 for Apply, and 1 for Cancel
	if result == 0: # Apply
		VrayMode = dlg.getValue("Vray Modes")
		return VrayMode
	else:
		return False
# -----------------------------------------------------
# Render VrsceneFile
# -----------------------------------------------------
def RenderVray():
	VrayMode 			=		vrayStndAloneUI()
	if VrayMode == "standard":
		VrayScene			=		mkVrayVrscene()
		vrayCmd				=		"vray.exe -sceneFile="+VrayScene+' -display = 1 -autoClose=0 -verboseLevel = 4 -displaySRGB = 1  '
		vrayRender(vrayCmd)
	elif VrayMode == "preview":
		VrayScene			=		mkVrayVrscene()
		vrayCmd				=		"vray.exe -sceneFile="+VrayScene+' -display = 1 -imgHeight = 405 -imgWidth = 720 -autoClose=0 -verboseLevel = 4 -displaySRGB = 1  '
		vrayRender(vrayCmd)
	elif VrayMode == "draft":
		VrayScene			=		mkVrayVrscene()
		VrayCmd				=		"vray.exe -sceneFile="+VrayScene+' -display=1 -autoClose=0 -imgHeight = 405 -imgWidth = 720 -verboseLevel = 20 -rtEngine = 1 -rtNoise =.1  -displaySRGB = 1 '
		vrayRender(VrayCmd)
	elif VrayMode == "SaveExr":
		files				=	cmds.file(query=1, list=1, withoutCopyNumber=1)
		shotname			=	files[0].split( '.' )
		shotname			=	shotname[0]
		shotID				=	shotname.split( '/' )
		shotID				=	shotID[6]
		thumbFileName		=	files[0].replace( '.mb', '.vrimg' )
		batFileName			=	files[0].replace( '.mb', '.bat' )
		batfile				=	("%s")%batFileName
		VrayScene			=		mkVrayVrscene()
		vrayCmd				=		"vray.exe -sceneFile="+VrayScene+' -display = 1  -autoClose=0 -verboseLevel = 4 -displaySRGB = 0 -imgFile= %s'%(thumbFileName)
		vrayRender(vrayCmd)
		t = 0
		while (t < 3 ):
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
	elif VrayMode == False:
		print "Canceled"
	else:
		print "Unexpected VrayMode: %s" % VrayMode

# -----------------------------------------------------
# creat vrscene file
# -----------------------------------------------------
def mkVrayVrscene():
	dataPath			=	    TEMP_PATH
	if os.path.exists(dataPath):
		print "temp folder exists"
		fileList 		=		os.listdir(dataPath)
		for fileName in fileList:
			os.remove(dataPath + fileName)
	if not os.path.exists(dataPath):
		print "creating temp folder"
		os.makedirs(dataPath)
	mel.eval('setAttr "vraySettings.vrscene_render_on" 0;')
	mel.eval('setAttr "vraySettings.vrscene_on" 1;')
	mel.eval('setAttr -type "string" vraySettings.vrscene_filename "%svrayTemp";'%(dataPath))
	mel.eval('setAttr "vraySettings.misc_separateFiles" 1;')
	mel.eval('setAttr "vraySettings.misc_exportGeometry"1;')
	getCurrentRenderLayer = cmds.editRenderLayerGlobals(q=True,currentRenderLayer=True)
	mkLayers			=		cmds.ls(type ="renderLayer")
	if (len(mkLayers)	>		1):
		if (getCurrentRenderLayer == "defaultRenderLayer"):
			vrsceneName	=		'"%svrayTemp_masterLayer.vrscene"'%(dataPath)
		else:
			vrsceneName	=		'"%svrayTemp_%s.vrscene"'%(dataPath,getCurrentRenderLayer)
	else:
		vrsceneName		=		'"%svrayTemp.vrscene"'%(dataPath)
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
	vrayExeCmd			=		Vcmd
	bat.append (vrayExeCmd)
	batFile				=		open(TEMP_PATH+'/vray.bat', 'w')
	for entry in bat:
		batFile.write(entry + '\n')
	batFile.close()
	mel.eval(mkVrayVrsceneOff)
	mel.eval(mkVrayRenderOn)
	cmd					=		TEMP_PATH+"vray.bat"
	cmd					=		"exec (\"" + cmd + "\")"
	mel.eval(cmd)
# -----------------------------------------------------
# convert Vrimage to EXR
# -----------------------------------------------------
def vrimg2exr (image,filename):
	bat					=		[]
	vrayExeCmd			=		'vrimg2exr "%s" -half -compression zips'%(image)
	bat.append (vrayExeCmd)
	batFile				=		open(filename, 'w')
	for entry in bat:
		batFile.write(entry + '\n')
	batFile.close()
	cmd					=		filename
	cmd					=		"exec (\"" + cmd + "\")"
	mel.eval(cmd)

# -----------------------------------------------------
# execute command
# -----------------------------------------------------
if __name__ == '__main__':
	RenderVray()
