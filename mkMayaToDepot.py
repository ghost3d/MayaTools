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
sys.path.append( 'Q:/Tools/Shotgun/Scripts/python/' )
# --------------------------------------------------------
# global variables
# --------------------------------------------------------
depotIngPath = "Q:/Tools/Nearline/ingestion/3dModels"
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
	cmds.confirmDialog(m=newZip[-1]+" was created", cb = "cancel")
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
	files			=	maya.cmds.file(query=1, list=1, withoutCopyNumber=1)
	changeformat	=	'setAttr "defaultRenderGlobals.imageFormat" 8;'
	thumbFileName	=	files[0].replace( '.mb', '.jpg' )
	mel.eval(changeformat)
	currentCam		=	mkRenderCam()
	if currentCam	==	" ":
		cmds.warning ("no renderable camera")
	# render and save image
	cmds.render(currentCam[0], x= 720, y =405)
	editor			=	'renderView'
	cmds.renderWindowEditor(editor, e = True, writeImage = thumbFileName)
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
	zipfile		=	zipScene()
	thumbnail	=	mkThumbNail()
	if os.path.exists( thumbnail ) == True:
		dstfile = mkMoveToIngDir(zipfile,thumbnail)
	if os.path.exists( dstfile ) == True:
		DepotIngestion()