# ------------------- Written by: Mike Kirylo, ------------------------------------------------
# ------------------- march  2014
# ------------------- This script will Export an object as an obj then import it to clean it of any maya nodes. 
# ------------------- imports ------------------------------------
import sys
import os
import maya.cmds as cmds
import maya.mel as mel
from pprint import pprint
from pprint import pformat
from zoic_api.gui import CustomDialog
from PySide import QtGui
# -----------------------------------------------------
# Paths
# -----------------------------------------------------
TEMP_PATH				= 		'C:/temp/'
# -----------------------------------------------------
# UI
# -----------------------------------------------------
class myclass(object):
	def __init__(self):
		parent = QtGui.QApplication.activeWindow()
		self.dlg = CustomDialog("Clean Geo",parent=parent)
		self.dlg.addDescription("This tool will export an obj for each object selected. Objects will be imported and marked Clean, you can also use the tool to export multiple obj's")
		self.dlg.addTextFieldButton("Load Objects", "Load source objects", "none" , self.mkLoadSource , editable = True )
		self.dlg.addButton("Apply") # Buttons always go on the bottom
		self.dlg.addButton("Close") # Each button gets and index value returned on exit
		self.result = self.dlg.show() # result will be 0 for OK, and 1 for Close
	def mkLoadSource(self):
		selectedOBJ			=		cmds.ls(sl = True,g = True,tr = True)
		selectedOBJ			=		",".join(selectedOBJ)
		self.dlg.setValue("Load Objects", selectedOBJ)
# -----------------------------------------------------
# functions
# -----------------------------------------------------
def CleanGeo():
	Uiinfo				=		myclass()
	if Uiinfo.result == 0: # Apply
		sourceObjects		=		Uiinfo.dlg.getValue("Load Objects")
		sourceObjects		=		sourceObjects.split(",")
		exportOnly			=		Uiinfo.dlg.getValue("Export Only")
		for entry in sourceObjects:
			cmds.select(clear = True)
			cmds.select(entry)
			if os.path.exists(TEMP_PATH+"/"+entry+"_clean.obj" ) == True:
				cmds.sysFile(TEMP_PATH+"/"+entry+"_clean.obj", delete = True)
			cmds.file(TEMP_PATH+"/"+entry+"_clean.obj", es = True, type = "OBJexport"  )
			cmds.setAttr (entry + ".visibility" ,  0)
			cmds.file(TEMP_PATH+"/"+entry+"_clean.obj", i = True , type = "OBJ", )
			cmds.rename(entry+"_clean_"+entry, entry+"_clean")
			cmds.sysFile(TEMP_PATH+"/"+entry+"_clean.obj", delete = True)
# -----------------------------------------------------
# execute
# -----------------------------------------------------
if __name__=='__main__':
	CleanGeo()
