# ------------------- Written by: Mike Kirylo, ------------------------------------------------
# ------------------- for Zoic Studios 
# ------------------- Oct 24 2011
# ------------------- This script is meant to render using vray stand alone locally
# -------imports ------------------------------------
import math
import sys
import string
import os
import fnmatch
import urllib
import cPickle
import webbrowser
import getpass
import shutil
import glob
import socket
import datetime
import maya.cmds as cmds
import maya.mel as mel
from pprint import pprint
from pprint import pformat
sys.path.append("Q:/Tools/Shotgun/Scripts/python")
from shotgun_api3 import Shotgun
from zoic_api import Zoic
# -----------------------------------------------------
# Paths
# -----------------------------------------------------
VRAY			= 'vray.exe'
VrayPath		='C:/Program Files/Autodesk/Maya2012/vray/bin/'
# -----------------------------------------------------
# UI
# -----------------------------------------------------
def SubmitGolaemUI():
	if (cmds.window('mkRenderGolaemUI', exists=True) == True):
		cmds.deleteUI('mkRenderGolaemUI')
	GolaemSubmitUI = cmds.loadUI (f = 'Q:/Tools/maya/2012/scripts/python/UI/mkRenderGolaemUI.ui')
	cmds.showWindow(GolaemSubmitUI)
	mkRefreshUI()
def mkRefreshUI():
	mkGolaemSubmitUiInfo()
def mkCloseWindow():
	cmds.deleteUI('mkRenderGolaemUI')
def mkGolaemSubmitUiInfo():
	timeline				=		mkStartEndFrame()
	for entry in timeline:
		startFrame			=		entry['startFrame']
		endFrame			=		entry['endFrame']
	startFrame				=		int(startFrame)
	endFrame				=		int(endFrame)
	cmds.textField('GolaemFrames',e=True, it = str(startFrame)+ '-' + str(endFrame))
	
# -----------------------------------------------------
#  Get project info
# -----------------------------------------------------
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
	info.append( {'projectDir':projectDir,'renderPath':renderFoler, 'dataPath':dataPubPath,'projectName':projectName, 'fileDir':fileDir, 'shotName':shotName , 'sceneName':sceneName, 'sceneRoot':sceneRoot,'sceneDescriptor':sceneDescriptor,'sceneVersion':sceneVersion,'sceneExtension':sceneExtension,} )
	return(info)
# -----------------------------------------------------
# export Vray
# -----------------------------------------------------
def mkexportAll():
	VrayScenePath				=		mkVrayVrscene()
	VrFiles						=		mkFindVR(VrayScenePath)
	shotName					=		mkGolaemVrayExp()
	golaemFiles					=		mkFindGolaem(VrayScenePath,shotName)
	mkEditVR(VrFiles,golaemFiles,VrayScenePath)
# -----------------------------------------------------
# get Frame Range
# -----------------------------------------------------
def mkStartEndFrame():
	timeLine				=		[]
	startFrame = cmds.playbackOptions (query = True, minTime = True)
	endFrame = cmds.playbackOptions (query = True, maxTime = True)
	timeLine.append( { 'startFrame':startFrame,'endFrame':endFrame})
	return(timeLine)
# -----------------------------------------------------
# Export secene vrscene file
# -----------------------------------------------------
def mkVrayVrscene():
	fileInfo				=		mkFileInfo()
	if cmds.checkBox('MblurCheckBox',q=True,v=True):
		mbV					=		1
	else:
		mbV					=		0
	mel.eval('setAttr "vraySettings.vrscene_render_on" 0;')
	mel.eval('setAttr "vraySettings.vrscene_on" 1;')
	mel.eval('setAttr "vraySettings.misc_compressedVrscene" 0;')
	mel.eval('setAttr "vraySettings.misc_meshAsHex" 0;')
	mel.eval('setAttr "vraySettings.misc_eachFrameInFile" 1;')
	mel.eval('setAttr -type "string" vraySettings.vrscene_filename "c:/temp/vrayTemp";')
	mel.eval('setAttr "vraySettings.misc_separateFiles" 0;')
	mel.eval('setAttr "vraySettings.misc_exportGeometry" 1;')
	mel.eval('setAttr "vraySettings.cam_mbIntervalCenter" 0;')
	mel.eval('setAttr "vraySettings.cam_mbOn" %s;'%(mbV))
	TimeLine				=		cmds.textField('GolaemFrames',q=True, tx = True)
	TimeLine				=		TimeLine.split('-')
	startFrame				=		TimeLine[0]
	endFrame				=		TimeLine[1]
	mel.eval('setAttr "defaultRenderGlobals.animation" 1;')
	mel.eval('setAttr "defaultRenderGlobals.startFrame" %s;'%(startFrame))
	mel.eval('setAttr "defaultRenderGlobals.endFrame" %s;'%(endFrame))
	for entry in fileInfo:
		VrscenePath			=		entry['dataPath'] + '/Vrscene/'
	if not os.path.exists(VrscenePath):
		os.makedirs(VrscenePath)
	mel.eval('setAttr -type "string" vraySettings.vrscene_filename "%svrayMain";'%(VrscenePath))
	mel.eval('RenderIntoNewWindow;'+'renderIntoNewWindow render;')
	return VrscenePath
# -----------------------------------------------------
# export Golaem Vray files
# -----------------------------------------------------
def mkGolaemVrayExp(cache,mbValue):
	TimeLine				=		cmds.textField('GolaemFrames',q=True, tx = True)
	TimeLine				=		TimeLine.split('-')
	startFrame				=		float(TimeLine[0])
	endFrame				=		float(TimeLine[1])
	fileInfo = mkFileInfo()
	mkCrowdFile				=		cmds.ls('crowdField*')
	for entry in fileInfo:
		VrscenePath			=		entry['dataPath'] + '/Vrscene/'
		fbxDir				=		entry['dataPath']
		shotName			=		entry['shotName']
	for entry in mkCrowdFile:
		cmds.runCrowdSimulation(startFrame=startFrame, endFrame=endFrame, 
		crowdFieldNode=[entry], exportFromCache = cache,
		vrayExpEnabled=1, vrayExpOutDir=VrscenePath,vrayExpMBlurEnable = mbValue,vrayExpMBlurSamples = 2)
	return shotName
# -----------------------------------------------------
# find scene vrscene files
# -----------------------------------------------------
def mkFindVR(path):
	os.chdir(path)
	VrayMainFiles			=		[]
	for files in glob.glob("vrayMain*"):
		VrayMainFiles.append(files)
	VrayMainFiles.sort()
	return VrayMainFiles
# -----------------------------------------------------
# find golaem vrscene files
# -----------------------------------------------------
def mkFindGolaem(path,shotName):
	os.chdir(path)
	golaemFiles			=		[]
	filePrefix			=		shotName+'*'
	for files in glob.glob(filePrefix):
		golaemFiles.append(files)
	frame				=		{}
	for vrScene in golaemFiles :
		vrName			=		vrScene
		frameId = vrScene.split('.')[1].zfill( 8 )
		frameId			=		int(frameId)
		frame[frameId]=vrName
	return frame
# -----------------------------------------------------
# edit main Vrscene files
# -----------------------------------------------------
def mkEditVR(vrsceneFiles,golameFiles,path):
	vrInclude				=		'#include "%s'%(path)
	VrKey					=		[]
	for entry in vrsceneFiles:
		vrNum				=		entry.split('_')[1]
		vrNum				=		vrNum.split('.')[0]
		vrNum				=		int(vrNum)
		vrNum				=		vrNum*250
		keyNum				=		int(vrNum)
		gKey			=		golameFiles[keyNum]
		vFile			=		open(entry, 'a')
		vFile.write(vrInclude+gKey +'"'+ '\n')
	vFile.close()
# -----------------------------------------------------
# build python file
# -----------------------------------------------------
def getDomain( path ):
	address = socket.gethostbyname(socket.gethostname())
	if fnmatch.fnmatch(address, '192.168.*'):
		path = path.replace( "Q:/", "//silo.zoicla.com/prod/" )
	elif fnmatch.fnmatch(address, '10.10.*'):
		path = path.replace( "Q:/", "//kilo.zoicbc.com/prod/" )
	return path

def getClusterMount( ):
	address = socket.gethostbyname(socket.gethostname())
	if fnmatch.fnmatch(address, '192.168.*'):
		return '\\\\silo\\prod'
	elif fnmatch.fnmatch(address, '10.10.*'):
		return '\\\\kilo\\prod'

def getArchive( ):

	# Get File Path
	path = str(cmds.file( q=True, l=True )[0])
	path = path.replace("/3D/scenes/", "/.archive/")
	path = path.split("/maya/")[0] + '/vray/' + os.path.basename( path.split("/maya/")[1] )[:-3] + '/' + os.path.basename( path.split("/maya/")[1] )
	path = getDirectory( path )

	# Save File Path
	fileType = cmds.file( q=True, type=True)
	fileType = fileType[0].encode('ascii')
	fileType = cmds.file( path, op="", type=fileType ,  pr=True, ea=True, f=True )

	return path

def getPythonHeader( ):
	batch = ''
	batch += "import os\n" 
	batch += "import sys\n"
	batch += "import shutil\n" 
	batch += "os.system( 'ipconfig /flushdns' )\n" 
	batch += "os.system( 'net use q: " + getClusterMount( ) + " /PERSISTENT:YES < nul' )\n" 
	batch += "sys.path.append('Q:\Tools\Shotgun\Scripts\python')\n" 
	batch += "from shotgun_api3 import Shotgun\n" 
	batch += "# -----------------------------------------------------------------------------\n" 
	batch += "SERVER_PATH         = 'http://shotgun.zoicstudios.com'\n" 
	batch += "SCRIPT_USER         = 'sgPublishFilmOutput'\n" 
	batch += "SCRIPT_KEY          = 'd2c2832f69567db0ad75516e018bde24c522c7bf'\n" 
	batch += "# -----------------------------------------------------------------------------\n" 
	batch += "VRAY			= " +'"'+ VRAY +'"'+"\n" 
	batch += "VRAYPATH		= " + '"'+VrayPath +'"'+ "\n" 
	batch += "# -----------------------------------------------------------------------------\n" 
	batch += "sg = Shotgun(SERVER_PATH, SCRIPT_USER, SCRIPT_KEY)\n"
	batch += "frame = os.getenv('RUSH_FRAME')\n" 
	batch += "\n"
	return batch
	
def getVrsceneCommand( vrScene, imgFile, frame ):
	batch  = ''
	batch += "if frame == '" + str(frame) + "':\n"
	batch += "	vrScene		= '" + vrScene + "'\n"
	batch += "	imageFile	= '" + imgFile + "'\n"
	batch += "	if os.path.exists( vrScene ) == False:\n"
	batch += "		print 'FAILURE: Unable to generate a vrScene File.'\n"
	batch += "		sys.exit(1)\n"
	batch += "	else:\n"
	batch += "		print 'rendering Golaem vray file'\n"
	batch += "		cmd = '%s -sceneFile= %s -display = 0  -autoClose=1 -verboseLevel = 4  -imgFile=%s ' % ( VRAY, vrScene, imageFile )\n"
	batch += "		os.chdir(VRAYPATH)\n"
	batch += "		os.system( cmd )"
	batch += "\n"   
	return batch
	
def getPython( ):

	# Get File Path
	path = str(cmds.file( q=True, l=True )[0])
	path = path.replace("/3D/scenes/", "/.archive/")
	path = path.split("/maya/")[0] + '/vray/' + os.path.basename( path.split("/maya/")[1] )[:-3] + '/' + os.path.basename( path.split("/maya/")[1] )[:-3] + '.py'
	path = getDirectory( path )

	return path

def getDirectory( path ):
	if os.path.exists( os.path.dirname( path ) ) == False:
		os.makedirs( os.path.dirname( path ) )
	path = getDomain( path )
	return path
	
def getFile( data, path ):
	path = getDomain( path )
	file = open( path, "w")
	file.write(data)
	file.close()
	return path
	
def executeRemotely( path, version, frameRange ):
	import sgPublishPythonSubmit as sgPublishPythonSubmit
	reload(sgPublishPythonSubmit)
	sgPublishPythonSubmit.sgPublishPythonSubmit( 'DOS-Batch', ('Golaem_' + version.upper() ), ('python ' + path ), frameRange )
def awCheckVrayPlugin():
	vrayPlug = cmds.pluginInfo("vrayformaya.mll", q=True, l=True,)
	if (vrayPlug == False):
		cmds.loadPlugin("vrayformaya.mll")
		cmds.warning("Vray Plugin has been loaded. \n")
	currRenderer = mel.eval('currentRenderer')
	if (currRenderer != "vray"):
		mel.eval("setCurrentRenderer vray")
def mkRenderGolaem( ):
	awCheckVrayPlugin()
	getCurrentRenderLayer		=		cmds.editRenderLayerGlobals(q=True,currentRenderLayer=True)
	if cmds.checkBox('UsecacheCheckBox',q=True,v=True):
		caceV					=		1
	else:
		caceV					=		0
	if cmds.checkBox('MblurCheckBox',q=True,v=True):
		mbV					=		1
	else:
		mbV					=		0
	print mbV
	print caceV
	mkFInfo						=		mkFileInfo()
	for entry in mkFInfo:
		renderDir				=		entry['renderPath'] 
		sceneName				=		entry['sceneName']
	renderPath					=		renderDir + getCurrentRenderLayer
	if not os.path.exists(renderPath):
		os.makedirs(renderPath)
	VrayScenePath				=		mkVrayVrscene()
	VrFiles						=		mkFindVR(VrayScenePath)
	shotName					=		mkGolaemVrayExp(caceV,mbV)
	golaemFiles					=		mkFindGolaem(VrayScenePath,shotName)
	mkEditVR(VrFiles,golaemFiles,VrayScenePath)
	VrPython	= getPython()
	objArchive	= getArchive()
	objCode		= os.path.basename( objArchive )[:-3]
	objScript	= getPythonHeader()
	objRange	= ''
	objId		= 1
	imgFile					=		renderDir + getCurrentRenderLayer+ '/'+sceneName
	img						=		imgFile.replace( '.mb', '.exr ' )
	pprint (img)
	for obj in VrFiles:
		vrsceneFile				=		VrayScenePath + str(obj)
		objScript				+=		getVrsceneCommand( vrsceneFile, img, objId )
		objRange				+=		str(objId) + ":" + str(obj) + ' '
		objId					+=		1
	VrPython	= getFile( objScript, VrPython )
	pprint (VrPython)
	objJobId	= executeRemotely( VrPython, objCode, objRange )