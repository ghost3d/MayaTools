# Written by Michael Kirylo 2009
#import maya comands
# create uv's on multiple objects
import maya.cmds as cmds
# Create UI
def  mkAutoUi():
	mkautoUvUI= cmds.window (title = "mk_uvTools",wh = (256,256))
	cmds.columnLayout(adj = True)
	cmds.button (label = "Auto UV", command =  "mk_autoUV.mkAutoUv()")
	global mkAuto
	mkAuto = cmds.floatFieldGrp( numberOfFields=1, label='Planes 3,4,5,6,8 or 12 ',adjustableColumn = 1 )
	cmds.button (label = "Spherical", command =  "mk_autoUV.mkSphere()")
	cmds.button (label ="cylindrical", command =   "mk_autoUV.mkcyclinder()")
	cmds.button (label ="planar", command =  "mk_autoUV.mkPlanar()")
	global mkPlanarF
	mkPlanarF = cmds.textFieldGrp( label='x,y,z,or camera (p) ' )
	cmds.showWindow (mkautoUvUI)


def mkAutoUv():
 	mkObjList = cmds.ls (sl = True)
	mkAutoList = len(mkObjList)
	mkAutoV = cmds.floatFieldGrp(mkAuto,query = True, value1 = True)
	for i in range (0,mkAutoList,1):
		cmds.polyAutoProjection (mkObjList[i],planes = mkAutoV, layout = 2, ch = True)
def mkSphere():
	mkObjListS = cmds.ls (sl = True)
	mkAutoListS = len(mkObjListS)
	for i in range (0,mkAutoListS,1):
		cmds.polyProjection(mkObjListS[i],type='Spherical', ch = True,sf = True)
def mkcyclinder():
	mkObjListC = cmds.ls (sl = True)
	mkAutoListC = len(mkObjListC)
	for i in range (0,mkAutoListC,1):
		cmds.polyProjection(mkObjListC[i],type='Cylindrical', ch = True,sf = True)
def mkPlanar():
	mkObjListP = cmds.ls (sl = True)
	mkAutoListP = len(mkObjListP)
	mkPlanarV = cmds.textFieldGrp(mkPlanarF,query = True, text = True)
	for i in range (0,mkAutoListP,1):
		cmds.polyProjection(mkObjListP[i],type='Planar',md = mkPlanarV,  ch = True,sf = True)
		mkAuto