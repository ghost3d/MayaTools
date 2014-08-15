#mkFixNormals 2009
def mkNrmlFix():
	from pymel import *
	##get List of objects
	listObj =ls(sl = True)
	##run normal comands
	for i in range (len(listObj)):
		polyAverageNormal (listObj [i], prenormalize = True, allowZeroNormal = False, postnormalize = False, distance = 0.1, replaceNormalXYZ =(1.0,0.0,0.0))
		polyNormal (listObj [i], nm = 2, unm = 0, ch =1)
		polySetToFaceNormal (listObj [i])
		polySoftEdge (listObj [i], angle = 30, ch = 1,)
		bakePartialHistory (listObj [i])