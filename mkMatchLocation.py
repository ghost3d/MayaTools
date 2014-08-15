# ------------------- Written by: Mike Kirylo, ------------------------------------------------
# ------------------- March 2014
# ------------------- duplicate objects to another objects locations 
# ------------------- imports ------------------------------------
import sys
import maya.cmds as cmds
import maya.mel as mel
from pprint import pprint
from pprint import pformat
from zoic_api.gui import CustomDialog
from PySide import QtGui
# -----------------------------------------------------
# UI
# -----------------------------------------------------
class myclass(object):
	def __init__(self):
		parent = QtGui.QApplication.activeWindow()
		self.dlg = CustomDialog("Duplicate Objects",parent=parent)
		self.dlg.addDescription("This tool will duplicate an object and move it to the location of all target objects")
		self.dlg.addTextFieldButton("LoadSource", "Load source objects", "none" , self.mkLoadSource , editable = True )
		self.dlg.addTextFieldButton("Load Object", "Load object to duplicate", "none" , self.mkLoadObject , editable = True )
		self.dlg.addCheckBox("Include Input Graph", state = False)
		self.dlg.addCheckBox("Keep constrain", state = False)
		self.dlg.addButton("Apply") # Buttons always go on the bottom
		self.dlg.addButton("Close") # Each button gets and index value returned on exit
		self.result = self.dlg.show() # result will be 0 for OK, and 1 for Close
	def mkLoadSource(self):
		selectedOBJ			=		cmds.ls(sl = True,g = True,tr = True)
		selectedOBJ			=		",".join(selectedOBJ)
		self.dlg.setValue("LoadSource", selectedOBJ)
	def mkLoadObject(self):
		heroOBJ			=		cmds.ls(sl = True,sn = True,tr = True)
		heroOBJ			=		str(heroOBJ[0])
		self.dlg.setValue("Load Object", heroOBJ)
# -----------------------------------------------------
# functions
# -----------------------------------------------------
def RunDuplication():
	Uiinfo				=		myclass()
	if Uiinfo.result == 0: # Apply
		sourceObjects		=		Uiinfo.dlg.getValue("LoadSource")
		sourceObjects		=		sourceObjects.split(",")
		DupObjects			=		Uiinfo.dlg.getValue("Load Object")
		inputGraph			=		Uiinfo.dlg.getValue("Include Input Graph")
		keepConst			=		Uiinfo.dlg.getValue("Keep constrain")
		print keepConst
		
		if inputGraph		== 		0:
			for entry in sourceObjects:
				newObj	=		cmds.duplicate(DupObjects)
				cmds.parentConstraint( entry , newObj )
				if keepConst		==   	0:
					cmds.parentConstraint( entry , newObj, e=True, rm=True )
		else:
			for entry in sourceObjects:
				newObj	=		cmds.duplicate(DupObjects, ic = True)
				Dup 	=		cmds.ls(newObj, tr = True)
				cmds.parentConstraint( entry , Dup )
				if keepConst		==   	0:
					cmds.parentConstraint( entry , Dup, e=True, rm=True )

# -----------------------------------------------------
# execute
# -----------------------------------------------------
if __name__=='__main__':
	RunDuplication()