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
from pymel.core import *
import fnmatch
# -----------------------------------------------------
# Paths
# -----------------------------------------------------
vray					=		'"C:/Program Files/Autodesk/Maya2012/vray/bin/"'
exrconv					=		'"C:/Program Files/Chaos Group/V-Ray/Maya 2012 for x64/bin/"'
TEMP_PATH				= 		'P:/temp/'
NUKE					=		"Q:/Tools/nuke/bin/64/Nuke6.latest/Nuke6.latest.exe"
# -----------------------------------------------------
# export functions
# -----------------------------------------------------
def mkexportAll():
	VrayScene			=		mkVrayVrscene("1")
	vrayCmd				=		"vray.exe -sceneFile="+VrayScene+' -display = 1 -autoClose=0 -verboseLevel = 4 -displaySRGB = 1  '
	vrayRender(vrayCmd)
def mkexportAllPreview():
	VrayScene			=		mkVrayVrscene("1")
	vrayCmd				=		"vray.exe -sceneFile="+VrayScene+' -display = 1 -imgHeight = 405 -imgWidth = 720 -autoClose=0 -verboseLevel = 4 -displaySRGB = 1  '
	vrayRender(vrayCmd)
def mkexportGeoOffPreview():
	VrayScene			=		mkVrayVrscene("0")
	vrayCmd				=		"vray.exe -sceneFile="+VrayScene+' -imgHeight = 405 -imgWidth = 720 -display = 1 -autoClose=0 -verboseLevel = 4 -displaySRGB = 1  '
	vrayRender(vrayCmd)
def mkexportGeoOff():
	VrayScene			=		mkVrayVrscene("0")
	vrayCmd				=		"vray.exe -sceneFile="+VrayScene+' -display = 1 -autoClose=0 -verboseLevel = 4 -displaySRGB = 1  '
	vrayRender(vrayCmd)
def mkexportAllSaveImage(image):
	VrayScene			=		mkVrayVrscene("1")
	vrayCmd				=		"vray.exe -sceneFile="+VrayScene+' -display = 1  -autoClose=0 -verboseLevel = 4 -displaySRGB = 0 -imgFile= %s'%(image)
	vrayRender(vrayCmd)
def mkexportAllSaveVrimg(nuke):
	Fromat				=	"1280,720"
	files				=	cmds.file(query=1, list=1, withoutCopyNumber=1)
	shotname			=	files[0].split( '.' )
	shotname			=	shotname[0]
	thumbFileName		=	files[0].replace( '.mb', '.vrimg' )
	batFileName			=	files[0].replace( '.mb', '.bat' )
	batfile				=	("%s")%batFileName
	VrayScene			=		mkVrayVrscene("1")
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
	if nuke ==1:
		mkopenNuke(exrimg,shotname,Fromat)
def mkDraft():
	VrayScene			=		mkVrayVrscene("1")
	VrayCmd				=		"vray.exe -sceneFile="+VrayScene+' -display=1 -autoClose=0 -imgHeight = 405 -imgWidth = 720 -verboseLevel = 20 -rtEngine = 1 -rtNoise =.1  -displaySRGB = 1 '
	vrayRender(VrayCmd)
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
	fileInfo			=		mkFileInfo()
	for entry in fileInfo:
		dataPath			=		entry['dataPath'] 
	if not os.path.exists(dataPath):
		os.makedirs(dataPath)
	mel.eval('setAttr "vraySettings.vrscene_render_on" 0;')
	mel.eval('setAttr "vraySettings.vrscene_on" 1;')
	mel.eval('setAttr -type "string" vraySettings.vrscene_filename "%s/vrayTemp";'%(dataPath))
	mel.eval('setAttr "vraySettings.misc_separateFiles" 1;')
	mel.eval('setAttr "vraySettings.misc_exportGeometry"'+num+';')
	getCurrentRenderLayer = cmds.editRenderLayerGlobals(q=True,currentRenderLayer=True)
	mkLayers			=		cmds.ls(type ="renderLayer")
	print mkLayers
	print len(mkLayers)
	if (len(mkLayers)	>		1):
		if (getCurrentRenderLayer == "defaultRenderLayer"):
			vrsceneName	=		'"%s/vrayTemp_masterLayer.vrscene"'%(dataPath)
		else:
			vrsceneName	=		'"%s/vrayTemp_%s.vrscene"'%(dataPath,getCurrentRenderLayer)
	else:
		vrsceneName		=		'"%s/vrayTemp.vrscene"'%(dataPath)
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
# -----------------------------------------------------
# convert Vrimage to EXR
# -----------------------------------------------------
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
	
def mkopenNuke(imagePath,shotName,format):
	path		= 'Q:/Tools/nuke/templates/vray/vray_003.nk'
	pathId		=	1
	script		= ''
	if os.path.exists( path ) == False :
		cmds.warning( 'WARNING', 'The Back to Beauty Template does not exists on your file system.  Please make sur that the following path exists:\r\n\r\n' + path )
	else:
		file = open( path, 'r' )
		for line in file.readlines():
			if fnmatch.fnmatch( line, (' name *') ):
				line = line.split(' name ')[1]
				line = ' name ' + shotName + '_' + line
			script += line
		file.close()
		nodeList	= [ 
			{ 'Read'									: [ { 'file': imagePath }, { 'first' : 1 }, { 'last' : 1 }, { 'format' : format } ] } ,
			{ ('set ' + str(pathId) + ' [stack 0]' )	: [ ] } ,
		]
		nodeScript = getNukeNode( nodeList )
		scriptPath =( TEMP_PATH + 'BackToBeauty.nk' )
		# scriptPath = self.createTempFile( script, scriptPath )
		print scriptPath
		nfile			=		open(scriptPath, 'a')
		print nodeScript
		nfile.write(nodeScript)
		nfile.close()
		os.system("start " + NUKE + " " + scriptPath )
def mkFileInfo():
	awSceneInfo		= cmds.file ( q = True, sceneName = True)
	awSceneInfo		= awSceneInfo.split ( "/" )
	info = []
	projectDir		=	awSceneInfo[0:7]
	projectDir		=	('/'.join(projectDir))
	projectName		=	awSceneInfo[2]
	shotName		=	awSceneInfo[6]
	sceneName		=	awSceneInfo[-1]
	sceneNameBase	=	sceneName.split(".")
	sceneNameBase	=	sceneNameBase[0].split("_")
	sceneNameBase	=	('_'.join(sceneNameBase)+ '/')
	renderFoler		=	awSceneInfo[0:4]
	renderFoler		=	('/'.join(renderFoler) +'/renders/' + shotName + '/3d/' + sceneNameBase  )
	fileDir			=	awSceneInfo[0:-1]
	fileDir			=	('/'.join(fileDir) + '/')
	sceneExtension	=	sceneNameBase[-1]
	sceneVersion	=	sceneNameBase[-1]
	sceneRoot		=	'_'.join(sceneNameBase[0:3])
	sceneDescriptor	=	'_'.join(sceneNameBase[3:-1])
	dataPubPath		=	awSceneInfo[0:5]
	dataPubPath		=	('/'.join(dataPubPath) + '/data/' + shotName )
	imagePath		=	awSceneInfo[0:5]
	imagePath		=	('/'.join(imagePath) + '/images/' + shotName )
	info.append( {'projectDir':projectDir,'renderPath':renderFoler,'imagePath':imagePath, 'dataPath':dataPubPath,'projectName':projectName, 'fileDir':fileDir, 'shotName':shotName , 'sceneName':sceneName, 'sceneRoot':sceneRoot,'sceneDescriptor':sceneDescriptor,'sceneVersion':sceneVersion,'sceneExtension':sceneExtension,} )
	return(info)
	
def getNukeNode( nodeList  ):
	nodeStr = ''
	for node in nodeList :
		for nodeKey, nodeValueList in node.iteritems() :
			if fnmatch.fnmatch( nodeKey, 'set*') or fnmatch.fnmatch( nodeKey, 'push*'):
				nodeStr += nodeKey + '\n'
			else:
				nodeStr += nodeKey + ' {\n'
				for nodeValue in nodeValueList:
					for attrInfoKey, attrInfoVal in nodeValue.iteritems() :
						attrInfoVal = str(attrInfoVal).replace(',', '' )
						nodeStr += ' ' + attrInfoKey +  ' ' + str(attrInfoVal) + '\n'
				nodeStr += '}\n'
	return nodeStr