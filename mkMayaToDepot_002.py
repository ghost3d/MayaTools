# ------------------- Written by: Mike Kirylo, ------------------------------------------------
# ------------------- for Zoic Studios 
# ------------------- jan 3 2011
# ------------------- saves maya content to the depot
# -------imports ------------------------------------
import sys
import os
import maya.cmds as cmds
import maya.mel as mel
import maya
import zlib
import zipfile
import maya.cmds as cmds
import shutil
import glob
import time
sys.path.append( '//silo/prod/Tools/Shotgun/Scripts/python/' )
sys.path.append( '//silo/prod/Tools/maya/2012/scripts/python/' )
# --------------------------------------------------------
# global paths
# --------------------------------------------------------
depotIngPath = "//silo/prod/Tools/Nearline/ingestion/3dModels"
IMGCONVERT	= '"C:/Program Files/Autodesk/Maya2012/bin/imconvert.exe"'
# --------------------------------------------------------
# Zip scene file
# --------------------------------------------------------
def zipScene():
	import sys
	fileName		=	maya.cmds.file(q=True, sceneName=True)
	if (fileName==""):
		cmds.warning( "file not saved" )
	theLocale		=	cmds.about(codeset=True)
	files = maya.cmds.file(query=1, list=1, withoutCopyNumber=1)
	zipFileName		=	files[0].replace( '.mb', '.zip' )
	zip=zipfile.ZipFile(zipFileName, 'w', zipfile.ZIP_DEFLATED)
	for file in files:
		name		=	file.encode(theLocale)
		zip.write(name)		
	zip.close()
	newZip			=	zipFileName.split("/")
	return zipFileName
# --------------------------------------------------------
# find renderable camera
# --------------------------------------------------------	
def mkRenderCam():
	RenderableCam		=	[]
	cameras				=	cmds.ls(type= "camera")
	for cam in (cameras):
		camRenderable	=	cmds.getAttr (cam+".renderable")
		if camRenderable == True:
			RenderableCam.append(cam)
	if RenderableCam == [] :
		cmds.warning ("no renderable cameras in scene")
	return RenderableCam
# --------------------------------------------------------
# make thumbnail
# --------------------------------------------------------
def mkThumbNail():
	# get file name and path for thumbnail
	currentRE = mel.eval('currentRenderer;')
	if (currentRE != "vray"):
		cmds.warning ("changing render Engine to Vray")
		mel.eval('setCurrentRenderer vray;')
	import mkVrayDefault
	reload(mkVrayDefault)
	mkVrayDefault.vrayDefault()
	import mkRenderVray
	files			=	maya.cmds.file(query=1, list=1, withoutCopyNumber=1)
	thumbFileName	=	files[0].replace( '.mb', '.jpg' )
	mkRenderVray.mkexportAllSaveImage(thumbFileName)
	t = 0
	while (not os.path.exists( thumbFileName ) and ( t < 15000 )):
		time.sleep(5)
		t+=1
	return thumbFileName
# --------------------------------------------------------
# copy files to ingestion dir
# --------------------------------------------------------
def mkMoveToIngDir(zipFile,thumbnail):
	zipfileName		=	zipFile.split("/")
	zipfileName		=	zipfileName[-1]
	depotFolder		=	zipfileName.replace( ".zip", "" )
	dst				=	depotIngPath +"/"+ depotFolder
	if os.path.exists( dst ) == False:
		cmds.sysFile( dst, makeDir=True )
	dstFile			=	dst+"/"+zipfileName
	cmds.sysFile( zipFile, move = dstFile  )
	thmbFile		=	thumbnail.split("/")
	thmbFile		=	thmbFile[-1]
	thumDstFile			=	dst+"/"+thmbFile
	cmds.sysFile( thumbnail, move = thumDstFile  )
	return dstFile
# --------------------------------------------------------
#run Depot ingestion python script
# --------------------------------------------------------
def DepotIngestion():
	from  sgCronDepotTextureIngest import main
	main(*sys.argv)
# --------------------------------------------------------
#send maya file to depot
# --------------------------------------------------------
def mkSendDepot():
	mkConfirm = cmds.confirmDialog(m="you are about to upload this file to the depot",button = ["yes","no"], cb = "no")
	if mkConfirm == "yes":
		zipfile		=	zipScene()
		thumbnail	=	mkThumbNail()
		if os.path.exists( thumbnail ) == True:
			dstfile = mkMoveToIngDir(zipfile,thumbnail)
		if os.path.exists( dstfile ) == True:
			DepotIngestion()
			cmds.warning ("success")
	else:
		cmds.warning("operation canceled")
