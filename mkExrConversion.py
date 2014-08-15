# ---------------------------------------------------------------------------------------------
# ------------------- Written by: Mike Kirylo, ------------------------------------------------
# ---------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------
import math
import csv
import string 
import sys
import os
import glob
import re
import fnmatch
import datetime
import maya.cmds as cmds
import maya.mel as mel
from pprint import pprint
# ---------------------------------------------------------------------------------------------
# Global Variables
# ---------------------------------------------------------------------------------------------
NUKE	= 	"Q:/Tools/nuke/bin/64/Nuke6.latest/Nuke6.latest.exe"
DJV		= 	"Q:/Tools/DJV/32/djv-0.8.3.2/bin/djv_info.exe"

# ---------------------------------------------------------------------------------------------
# Main 
# ---------------------------------------------------------------------------------------------
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

def getReadNodes( pathInfo, pathId, imageInfo ):
	format = '\"' + imageInfo['sg_width'] + ' ' + imageInfo['sg_height'] + ' 0 0 ' + imageInfo['sg_width'] + ' ' + imageInfo['sg_height'] + ' 1 ' + os.path.basename( pathInfo ) + '\"'
	nodeList	= [ 
		{ 'Read'									: [ { 'file': pathInfo }, { 'first' : 1 }, { 'last' : 1 }, { 'format' : format } ] } ,
		{ ('set ' + str(pathId) + ' [stack 0]' )	: [ ] } ,
	]
	nodeScript = getNukeNode( nodeList )
	return nodeScript

def getWriteNodes( pathInfo, pathId ,format):
	path = pathInfo.replace( '.exr', format )
	type =format.split(".")
	nodeList	= [ 
		{ ('push $' + str(pathId) )					: [ ] } ,
		{ 'Write'									: [ { 'file' : path } , { 'file_type' : type[1] }, { 'first' : 1 }, { 'last' : 1 }] } ,
	]
	nodeScript = getNukeNode( nodeList )
	return nodeScript

def awSceneInfo():
	info		= cmds.file ( q = True, sceneName = True)
	info		= info.split ( "/" )
	return info

def getRootNodes( ):
	nodeScript	= ''
	nodeScript	+= '#! Q:/Tools/nuke/bin/64/Nuke6.latest/Nuke6.latest.exe -nx\n'
	nodeScript	+= 'version 6.3000\n'
	nodeScript	+= 'define_window_layout_xml {<?xml version=\"1.0\" encoding=\"UTF-8\"?>}\n'
	nodeList	= [ 
		{ 'Root' 			: [ ] } ,
	]
	nodeScript += getNukeNode( nodeList )
	return nodeScript

def getTempDir():
	path = 'P:/temp/mrExrConversion/'
	if os.path.exists( path ) == False:
		os.makedirs( path )
	return path

def getImageInfo( path ):
	print '- Processing DJV ' + os.path.basename( path )
	imageData = {}
	tmpDir		= getTempDir()
	tmpData		= tmpDir + 'Data.txt'
	os.system( DJV + ' -v -time_units ' + 'frames' + ' ' + path + ' > ' + tmpData )
	dataList = open( tmpData , 'r')
	dataList = dataList.read()
	dataList = dataList.replace(' ', '')
	dataList = dataList.split('\n')
	for data in dataList :
		if fnmatch.fnmatch( data, '*=*'):
			data = data.split('=')
			imageData[ ( 'sg_' + data[0].lower() ) ] = data[1]
	print imageData
	return imageData

def getFile( data, path ):
	file = open( path, "w")
	file.write(data)
	file.close()
	os.system("start " + NUKE + " " + path )
	return data

def getNukeCommand( path ):
	cmd = ''
	cmd += NUKE + ' '
	cmd += '-V '
	cmd += '-x '
	cmd += '-m 4 '
	cmd += '-q '
	cmd += '-m 8 '
	cmd += '-q '
	cmd += '-F ' + str(1) + '-' + str(1) + ' '
	cmd += path
	# os.system( cmd )
	return cmd

def mrExrConversion(ImagePath,format):

	# Build Variables
	scriptPath	= 'p:/temp/mrExrConversion/mrExrConversion.nk'
	resList		= [ 512, 1024, 2048, 4096 ]
	pathList	=  ImagePath
	pathId = 0
	# Build Nuke Script
	nukeScript = ''
	nukeScript += getRootNodes()
	for path in pathList :
		print '- Processing: ' + os.path.basename( path )
		imageInfo = getImageInfo( path )
		pathId += 1
		nukeScript += getReadNodes( path, pathId, imageInfo )
		nukeScript += getWriteNodes( path, pathId,format)

	# Save and Render Nuke Script
	print '- Executing: ' + scriptPath
	nukeScript		= getFile( nukeScript, scriptPath )
	nukeCommand		= getNukeCommand( scriptPath )
	os.system(nukeCommand)
	print nukeCommand

def mkGetImageFiles():
	filePath = cmds.fileDialog2(fileMode=3, caption="Texture path")
	exrFiles =[]
	os.chdir(filePath[0])
	for files in os.listdir("."):
		if files.endswith(".exr"):
			exrFiles.append(filePath[0]+'/'+files)
	mrExrConversion(exrFiles,".png")







