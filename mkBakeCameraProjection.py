# ------------------- Written by: Mike Kirylo, ------------------------------------------------
# ------------------- july 2013
# ------------------- This script will bake a camera projection sequence 
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
		fileTpyes = ['jpg','tiff','tga','png']
		resolution = ['256','512','1024','2048','4096']
		self.dlg = CustomDialog("bake camera projections",parent=parent)
		self.dlg.addDescription("This tool will bake out an animated camera projection")
		self.dlg.addComboBox("formats", fileTpyes)
		self.dlg.addComboBox("resolution", resolution)
		self.dlg.addTextField("Image name",defaultValue='',enabled=True)
		self.dlg.addTextField("Frame range",defaultValue= '',enabled=True)
		self.mkTimeRange()
		self.dlg.addTextFieldButton("Load camera", "select camera", "none" , self.mkLoadCam , editable = True )
		self.dlg.addTextFieldButton("Load shader", "select shader", "none" , self.mkLoadShader , editable = True )
		self.dlg.addTextFieldButton("Load object", "select object", "none" , self.mkLoadobj , editable = True )
		self.dlg.addCheckBox("Normal map", state = False)
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
	# --------------load ui with selections------------------------
	def mkLoadCam(self):
		selectedCam			=		cmds.ls(sl = True)
		selectedCam			=		str(selectedCam[0])
		self.dlg.setValue("Load camera", selectedCam)
	def mkLoadShader(self):
		selectedShad		=		cmds.ls(sl = True)
		selectedShad		=		str(selectedShad[0])
		self.dlg.setValue("Load shader", selectedShad)
	def mkLoadobj(self):
		selectedObj			=		cmds.ls(sl = True)
		selectedObj			=		str(selectedObj[0])
		self.dlg.setValue("Load object", selectedObj)
	# --------------bake camer normal maps------------------------
	def mkCreateCamNrml(self):
		surfaceShdr			=		cmds.shadingNode('surfaceShader', asShader=True, n = "surfaceShaderNode")
		setRangeShdr		=		cmds.shadingNode('setRange', asUtility = True, n='setRangeNode')
		samplerInfoShader	=		cmds.shadingNode('samplerInfo', asUtility = True, n='samplerInfoNode')
		cmds.setAttr (setRangeShdr+".maxX", 1)
		cmds.setAttr (setRangeShdr+".oldMinX", -1)
		cmds.setAttr (setRangeShdr+".oldMaxX", 1)
		cmds.setAttr (setRangeShdr+".maxY", 1)
		cmds.setAttr (setRangeShdr+".oldMinY", -1)
		cmds.setAttr (setRangeShdr+".oldMaxY", 1)
		cmds.setAttr (setRangeShdr+".maxZ", 1)
		cmds.setAttr (setRangeShdr+".oldMinZ", -1)
		cmds.setAttr (setRangeShdr+".oldMaxZ", 1)
		cmds.connectAttr(samplerInfoShader+".normalCameraX", setRangeShdr+".valueX")
		cmds.connectAttr(samplerInfoShader+".normalCameraY", setRangeShdr+".valueY")
		cmds.connectAttr(samplerInfoShader+".normalCameraZ", setRangeShdr+".valueZ")
		cmds.connectAttr(setRangeShdr+".outValue", surfaceShdr+".outColor")
		shaders				=		{}
		shaders['surface']=surfaceShdr
		shaders['setRange']=setRangeShdr
		shaders['sampler']=samplerInfoShader
		return (shaders)
# --------------execute------------------------
def mkBakeExecution():
	Uiinfo				=		myclass()
	if Uiinfo.result == 0: # Apply
		imgFormat 			=		Uiinfo.dlg.getValue("formats")
		imgres				=		Uiinfo.dlg.getValue("resolution")
		surfShdr			=		Uiinfo.mkCreateCamNrml()
		TimeLine			=		Uiinfo.dlg.getValue("Frame range")
		TimeLine			=		TimeLine.split('-')
		startFrame			=		int(TimeLine[0])
		endFrame			=		int(TimeLine[1])
		cameraName			=		Uiinfo.dlg.getValue("Load camera")
		ShaderName			=		Uiinfo.dlg.getValue("Load shader")
		objectName			=		Uiinfo.dlg.getValue("Load object")
		fileImageName		=		Uiinfo.dlg.getValue("Image name")
		normalCheck			=		Uiinfo.dlg.getValue("Normal map")
		cmds.cameraView(camera=cameraName)
		cmds.currentTime( startFrame, edit=True )
		for i in range (startFrame,endFrame):
			mKcurentFrame	=		cmds.currentTime( query=True )
			intFrame		=		int(mKcurentFrame)
			intFrame		=		str(intFrame).zfill(4)
			cmds.convertSolidTx( ShaderName, objectName, fileImageName=fileImageName+"_"+intFrame+'.'+imgFormat, fil =imgFormat,rx= int(imgres), ry= int(imgres))
			if normalCheck== 1 :
				cmds.convertSolidTx( surfShdr['surface'],objectName, fileImageName= fileImageName+"_nrml."+intFrame+'.'+imgFormat, fil = imgFormat,rx= int(imgres), ry= int(imgres))
			cmds.currentTime( mKcurentFrame+1, edit=True )
if __name__=='__main__':
	mkBakeExecution()