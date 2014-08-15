# Written by Michael Kirylo 2009
#--------------------- imports ------------------------
import maya.cmds as cmds
import maya.cmds as cmds
import maya.mel as mel
from zoic_api.gui import CustomDialog
#--------------------- create UI------------------------
class MatchOivot(object):
	def __init__(self):
		self.dlg = CustomDialog("match object pivot to another objects center")
		self.dlg.addDescription("Match object pivot point to the center of another selected object. select the source object then select the taget object. source objects pivot point will be moved to the center of the target object")
		self.dlg.addTextFieldButton("source object", "source", "none" , self.sourceObj , editable = True )
		self.dlg.addTextFieldButton("target object", "target", "none" , self.targetObj , editable = True )
		self.dlg.addButton("Apply") # Buttons always go on the bottom
		self.dlg.addButton("Close") # Each button gets and index value returned on exit
		self.result = self.dlg.show() # result will be 0 for OK, and 1 for Close
	def sourceObj(self):
		selectedCam			=		cmds.ls(sl = True)
		selectedCam			=		str(selectedCam[0])
		self.dlg.setValue("source object", selectedCam)
	def targetObj(self):
		selectedShad		=		cmds.ls(sl = True)
		selectedShad		=		str(selectedShad[0])
		self.dlg.setValue("target object", selectedShad)

def matchObjPivot():
	uiInfo		=	MatchOivot()
	if uiInfo.result == 0: # Apply
		sourcePivot		=	uiInfo.dlg.getValue("source object")	
		targetPivot		=	uiInfo.dlg.getValue("target object")
		mkobjCenterX = cmds.objectCenter (targetPivot,x = True)
		mkobjCenterY = cmds.objectCenter (targetPivot,y = True)
		mkobjCenterZ = cmds.objectCenter (targetPivot,z = True)
		cmds.move(mkobjCenterX,mkobjCenterY,mkobjCenterZ,sourcePivot+".scalePivot",sourcePivot+".rotatePivot")
if __name__=='__main__':
	matchObjPivot()