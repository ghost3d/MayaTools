# -------imports ------------------------------------
import sys
import os
import shutil
import maya.cmds as cmds
import maya.mel as mel
from pprint import pprint
import math

def awSceneInfo():
	info		= cmds.file ( q = True, sceneName = True)
	info		= info.split ( "/" )
	return info

def awRootName(sceneInfo):
	fileName 	= sceneInfo[-1]
	fileName 	= fileName.split ( "." )
	#get the base name of the maya scene without the extension
	fileRootName	= fileName[0]
	fileRootName	= fileRootName.split ( "_" )
	return fileRootName

def awExtension(sceneInfo):
	fileName 	= sceneInfo[-1]
	fileName 	= fileName.split ( "." )
	#get the base name of the maya scene without the extension
	fileExtension	= fileName[1]
	return fileExtension
	
def awVersionNumber(awRootName):
	versionNumber	= awRootName[-1]
	versionNumber	= ( ( int(versionNumber ) ) + 1 )
	return versionNumber

def awCheckFile(newFileName):
	fileExists = os.path.exists(newFileName)
	return fileExists

def awVersionUp():
	sceneInfo = awSceneInfo()
	sceneInfoCheck = len(awSceneInfo())
	if (sceneInfoCheck != 1):
		fileDir = sceneInfo [0:-1]
		fileDir = '/'.join( fileDir )
		fileName = awRootName(sceneInfo)
		rootName = awRootName(sceneInfo) [0:-1]
		rootName = '_'.join( rootName )
		versionNumber = awVersionNumber(fileName)
		versionNumber	= str( versionNumber ).zfill ( 3 ) 
		extension = awExtension(sceneInfo)
		#New file version and full path
		newFileName = fileDir + '/' + rootName + '_' + versionNumber + '.' + extension 
		#Check to see if the file exists and if i does it will iterate up until it doesn't match
		checkFile = awCheckFile(newFileName)
		while (checkFile == True):
			versionNumber = int( versionNumber )
			versionNumber = versionNumber + 1 
			versionNumber	= str( versionNumber ).zfill ( 3 )
			newFileName = fileDir + '/' + rootName + '_' + versionNumber + '.' + extension 
			checkFile = awCheckFile(newFileName)
			#print newFileName
		# Saves out new file a version higher
		print newFileName
		cmds.file( rename= newFileName  )
		cmds.file( save=True, type='mayaBinary' )
	else:
		cmds.warning('You have to save your file first before versioning up.')
	
#awVersionUp()