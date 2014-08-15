# ------------------- Written by: Mike Kirylo, ------------------------------------------------
# ------------------- for Zoic Studios 
# ------------------- dec 13 2011
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
RenderableCam = []
# --------------------------------------------------------
# find renderable camera
# --------------------------------------------------------
def mkRenderCam():
	cameras = cmds.ls(type= "camera")
	for cam in (cameras):
		camRenderable = cmds.getAttr (cam+".renderable")
		if camRenderable == True:
			RenderableCam.append(cam)
	if RenderableCam == [] :
		cmds.warning ("no renderable cameras in scene")
	return RenderableCam
# --------------------------------------------------------
# Zip scene file
# --------------------------------------------------------
def zipScene():
	import sys
	fileName = maya.cmds.file(q=True, sceneName=True)
	# If the scene has not been saved
	if (fileName==""):
		cmds.warning( "file not saved" )
	# get the default character encoding of the system
	theLocale = cmds.about(codeset=True)
	# get a list of all the files associated with the scene
	files = maya.cmds.file(query=1, list=1, withoutCopyNumber=1)
	# create a zip file named the same as the scene by appending .zip 
	zipFileName = files[0].replace( '.mb', '.zip' )
	zip=zipfile.ZipFile(zipFileName, 'w', zipfile.ZIP_DEFLATED)
	# add each file associated with the scene, including the scene
	# to the .zip file
	for file in files:
		name = file.encode(theLocale)
		zip.write(name)		
	zip.close()
	# output a message whose result is the name of the zip file newly created
	newZip = zipFileName.split("/")
	cmds.confirmDialog(m=newZip[-1]+" was created", cb = "cancel")
	mkThumbNail(files,zipFileName)
	# mkIngestionDir(zipFileName,'.zip')
# --------------------------------------------------------
# make thumbnail
# --------------------------------------------------------
def mkThumbNail(fileName,zipfile):
	# get file name and path for thumbnail
	changeformat ='setAttr "defaultRenderGlobals.imageFormat" 8;'
	files = fileName
	thumbFileName = files[0].replace( '.mb', '.jpg' )
	mel.eval(changeformat)
	currentCam =mkRenderCam()
	if currentCam == " ":
		cmds.warning ("no renderable camera")
	# render and save image
	cmds.render(currentCam[0], x= 720, y =405)
	editor = 'renderView'
	cmds.renderWindowEditor(editor, e = True, writeImage = thumbFileName)
	newFolder = mkIngestionDir(thumbFileName,'.jpg')
	mkIngestionDir(zipfile,'.zip')
	DepotIngestion()
	removeFolder(newFolder)
# --------------------------------------------------------
# copy files to ingestion dir
# --------------------------------------------------------
def mkIngestionDir(source,type):
	mkFile = source
	filename =source.split("/")
	filename = filename[-1]
	mkSource =source.split("/")
	mkSource = mkSource[-1]
	mkSource = mkSource.replace( type, "" )
	mkFolder =source.split("/")
	mkFolder.pop(-1)
	mkFolder = "/".join(mkFolder)
	mkFolder=mkFolder+"/"+mkSource
	if os.path.exists( mkFolder ) == False:
		os.makedirs( mkFolder )
	copycmd = 'sysFile -copy'+' '+'"'+mkFolder+'/'+ filename +'"'+' ' + '"'+ mkFile+'"'+';'
	mel.eval (copycmd)
	dst = "Q:/Tools/Nearline/ingestion/3dModels"
	delcmd = 'sysFile -delete'+' "'+mkFile+'";'
	mel.eval (delcmd)
	createdirCmd = 'sysFile -makeDir'+' '+'"'+dst+'/' +mkSource+'/"'
	mel.eval(createdirCmd)
	cpyDepotCmd = 'sysFile -mov'+' '+'"'+dst+'/' +mkSource+'/'+filename +'"'+' ' + '"'+mkFolder+'/'+ filename +'"'+';'
	mel.eval (cpyDepotCmd)
	print "copied "+filename+" to depot"
	removeEmptydir = 'sysFile -removeEmptyDir'+' '+'"'+mkFolder+'/";'
	mel.eval (removeEmptydir)
	cmds.confirmDialog(m=filename+" ready for upload", cb = "cancel")
	return mkFolder
def DepotIngestion():
	from  sgCronDepotTextureIngest import main
	main(*sys.argv)

	
def removeFolder(folderpath):
	os.rmdir(folderpath)

	