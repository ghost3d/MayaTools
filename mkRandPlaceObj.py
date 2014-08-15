## Written by Michael Kirylo 2010
## randomly place objects
## -------imports ------------------------------------
import sys
import os
import shutil
import maya.cmds as cmds
import glob
import time
import random
import operator
from pprint import pprint
## -------shotgun ------------------------------------
sys.path.append( 'Q:/Tools/Shotgun/Scripts/python/' )
sys.path.append( 'Q:/Tools/maya/2011/scripts/python' )

def mkRandPlace():
	mkDupList= []
	mkLocatorList= cmds.ls('locator*')
	print mkLocatorList
	mkObjList = cmds.ls(sl=True)
	if "locatorShape" in mkLocatorList:
		print "shapeNode"
	else:
		 for i in range (0,len(mkLocatorList),len(mkObjList)):
			for x in range (0,len(mkObjList),1):
				mkDup= cmds.duplicate (mkObjList[x])
				mkDupList.append(mkDup)
	for i in  range (len(mkLocatorList)):
		mkRandNum= random.randint(1,len(mkLocatorList))
		cmds.parentConstraint (mkLocatorList[i],mkDupList[mkRandNum])