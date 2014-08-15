# ------------------- Written by: Mike Kirylo, ------------------------------------------------
# ------------------- for Zoic Studios 
# ------------------- Oct 24 2012
# ------------------- This script is meant to convert bin files to vray proxy mesh files
# -------imports ------------------------------------
import sys
import pprint
import os
# -----------------------------------------------------
# Paths
# -----------------------------------------------------
vrExePath					=				'Q:/Tools/Vray/bin/vray.latest/Chaos Group/V-Ray/Maya 2012 for x64/bin'
vr2mesh						=				'ply2vrmesh.exe'
binPath						=				'"Q:/Series/onc/iis/ftp/freelance/mstasiuk-onc/in/20120322/zoic_ocean_dev_06a_meshes/zoic_ocean_dev_06a_meshes/'
meshname					=				'Realwave01_06a.*****.bin"'
filename					=				'waterTest.vrmesh'
def convBin2vMesh():
	os.chdir(vrExePath)
	cmd						=vr2mesh+ ' ' +binPath+meshname+ ' ' +binPath + filename+'",  -previewFaces 1500 -fps 24' 
	pprint.pprint (cmd)
	os.system(cmd)

def main( script ):
	convBin2vMesh()


if __name__ == '__main__':
	main(*sys.argv)