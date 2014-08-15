# ------------------- Written by: Mike Kirylo, ------------------------------------------------
# ------------------- july 2013
# ------------------- This script will create light selects in your scene
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
		self.dlg = CustomDialog("Create Light Selects",parent=parent)
		self.dlg.addDescription("This tool will create a light select for each light in your scene. select either Diffuse or Specular to create that type of lightselect for each light. You can check both to get one of each.")
		self.dlg.addCheckBox("Diffuse", state = True)
		self.dlg.addCheckBox("Specular", state = False)
		self.dlg.addButton("Apply") # Buttons always go on the bottom
		self.dlg.addButton("Close") # Each button gets and index value returned on exit
		self.result = self.dlg.show() # result will be 0 for OK, and 1 for Close
# -----------------------------------------------------
# creat light selects
# -----------------------------------------------------
def CreatLS():
	Uiinfo				=		myclass()
	if Uiinfo.result == 0: # Apply
		DifBox		=		Uiinfo.dlg.getValue("Diffuse")
		SpecBox		=		Uiinfo.dlg.getValue("Specular")
		print DifBox
		print SpecBox
	LightInScene		=		cmds.ls (type = "VRayLightRectShape")
	LightInScene		+=		cmds.ls (type = "VRayLightSphereShape")
	LightInScene		+=		cmds.ls (type = "VRayLightIESShape")
	LightInScene		+=		cmds.ls (type = "VRayLightDomeShape")
	LightInScene		+=		cmds.ls (type = "VRaySunShape")
	LightInScene		+=		cmds.ls (lights = True)
	if DifBox			==		True:
		for entry in LightInScene :
			LightSelectElement=	mel.eval ("vrayAddRenderElement LightSelectElement;")
			mel.eval ("sets -edit -forceElement" '   '+ LightSelectElement +'  ' +entry+';')
			mel.eval ('setAttr "' +LightSelectElement+'.vray_type_lightselect" 2;')
			mel.eval ('setAttr -type "string"' +  LightSelectElement+'.vray_name_lightselect'+ '"'+entry+'_diff";')
			mel.eval ('rename   '+ LightSelectElement+ '"'+ entry +'_diff" ;')
	if SpecBox			==		True:
		for entry in LightInScene :
			LightSelectElement=	mel.eval ("vrayAddRenderElement LightSelectElement;")
			mel.eval ("sets -edit -forceElement" '   '+ LightSelectElement +'  ' +entry+';')
			mel.eval ('setAttr "' +LightSelectElement+'.vray_type_lightselect" 3;')
			mel.eval ('setAttr -type "string"' +  LightSelectElement+'.vray_name_lightselect'+ '"'+entry+'_spec";')
			mel.eval ('rename   '+ LightSelectElement+ '"'+ entry +'_spec" ;')

# -----------------------------------------------------
# execute
# -----------------------------------------------------
if __name__=='__main__':
	CreatLS()