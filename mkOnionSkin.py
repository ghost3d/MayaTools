# ------------------- Written by: Mike Kirylo, ------------------------------------------------
# ------------------- july 2013
# ------------------- This script will duplicate a sequence of objects for onion skinning or creating a blend shape out of an animation
# ------------------- imports ------------------------------------
import sys
import maya.cmds as cmds
import maya.mel as mel
from pprint import pprint
from pprint import pformat
from zoic_api.gui import CustomDialog
# -----------------------------------------------------
# UI
# -----------------------------------------------------
class mkOnionUI(object):
	def __init__(self):
		self.dlg = CustomDialog("onion skin")
		self.dlg.addDescription("This tool will duplicate an object for each frame, this is usfull for onion skinning or for creating blend shapes from animations")
		FrameIncraments = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']
		self.dlg.addComboBox("Incrament", FrameIncraments)
		self.dlg.addTextField("Frame range",defaultValue= '',enabled=True)
		self.dlg.addTextFieldButton("Load object", "select object", "none" , self.mkLoadobj , editable = True )
		self.mkTimeRange()
		self.dlg.addButton("Apply") # Buttons always go on the bottom
		self.dlg.addButton("Close") # Each button gets and index value returned on exit
		self.result = self.dlg.show() # result will be 0 for OK, and 1 for Close
	# --------------Time range ------------------------
	def mkTimeRange(self):
		startFrame = cmds.playbackOptions (query = True, minTime = True)
		endFrame = cmds.playbackOptions (query = True, maxTime = True)
		startFrame			=		int(startFrame)
		endFrame			=		int(endFrame)
		self.dlg.setValue("Frame range", str(startFrame)+ '-' + str(endFrame))
	# ---------------load object-----------------------
	def mkLoadobj(self):
		selectedObj			=		cmds.ls(sl = True)
		selectedObj			=		str(selectedObj[0])
		self.dlg.setValue("Load object", selectedObj)
# --------------------execute Onion -------------------------
def executeOnion():
	Uiinfo				=		mkOnionUI()
	if Uiinfo.result == 0: # Apply
		FrameIncraments		=		Uiinfo.dlg.getValue("Incrament")
		TimeLine			=		Uiinfo.dlg.getValue("Frame range")
		TimeLine			=		TimeLine.split('-')
		startFrame			=		int(TimeLine[0])
		endFrame			=		int(TimeLine[1])
		currentFrame		=		startFrame
		animObj				=		Uiinfo.dlg.getValue("Load object")
		FrameIncraments		=		int(FrameIncraments)
		cmds.currentTime( startFrame, edit=True )
		frameNbr			=		startFrame
		while  (frameNbr < endFrame):
			frameNbr = cmds.currentTime( query=True )
			cmds.duplicate (animObj, name = "onionObj_"+ str(frameNbr))
			cmds.currentTime(frameNbr + FrameIncraments , edit=True )
if __name__=='__main__':
	executeOnion()