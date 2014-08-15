# Written by Michael Kirylo 2011
# find Glssy values of vray shaders
# -------imports ------------------------------------
import sys
import os
import maya.cmds as cmds
import maya.mel as mel
# -----------------------------------------------------
PyQtUIfile = os.path.join(os.path.dirname(__file__),'mkGlossyUI.ui')
# -----------------------------------------------------
def showUI():
        if (cmds.window('mkGlossyUI', exists=True) == True):
                cmds.deleteUI('mkGlossyUI')
        mkGlossyUI = cmds.loadUI (f = PyQtUIfile)
        cmds.showWindow(mkGlossyUI)
def getgloss():
        VRayshaders = mkFindShdrId()
        mkGettGlossy(VRayshaders)
def mkFindShdrId():
        mkAllShdr = cmds.ls(typ ="VRayMtl")
        return mkAllShdr

def mkGettGlossy(item):
        GlossValue                      =               cmds.textField('glossyValue',q=True,tx=True)
        for entry in (item):
                glossyValue = cmds.getAttr(entry+".reflectionGlossiness")
                if ( glossyValue < 0.6 ):
                        cmds.setAttr(entry+".reflectionGlossiness",float(GlossValue));
                        print entry+" glossy value to low!, value changed to 0.65 "
