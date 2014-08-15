# ------------------- Written by: Andrew Wilkoff, Mike Kirylo, Mike Romey------------------------------------------------
# ------------------- for Zoic Studios 
# ------------------- June 14 2012
# ------------------- This script is meant to easily turn on or off Vray render element on Maya's Render layers.
# -------imports ------------------------------------
import urllib2
import sys
import os
import shutil
import getpass
import maya.cmds as cmds
import maya.mel as mel
from pprint import pprint
import cPickle
import pickle
from string import strip

# ---------------------------------------------------------------------------------------------
# Shotgun
# ---------------------------------------------------------------------------------------------
sys.path.append( 'Q:/Tools/Shotgun/Scripts/python/' )
sys.path.append( 'Q:/Tools/maya/2012/scripts/python/' )
from shotgun_api3 import Shotgun
SERVER_PATH         = 'http://shotgun.zoicstudios.com'
SCRIPT_USER         = 'sgPublishBuildScene'
SCRIPT_KEY          = '87a551229d41397e84b9c7e16ad4b9e1fea27e04'
sg = Shotgun(SERVER_PATH, SCRIPT_USER, SCRIPT_KEY)

def log(msg):
	print time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()) +": "+msg

def connect():
	try:
		sg = Shotgun(SERVER_PATH, SCRIPT_USER, SCRIPT_KEY)
		return sg
	except Exception, e:
		log( "Unable to connect to Shotgun server. "+str(e) )
		exit(0)
sg = connect()
# #-------------------------------------------------------
# #----------------Vray render Elements-------------------
# #-------------------------------------------------------
vrayLayers =[{'label': 'DifChk', 'func': 'mkdif'}, 
	{'label': 'difClrChk', 'func': 'mkdifColor'},
	{'label': 'difRawChk', 'func': 'mkdifRaw'},
	{'label': 'giChk', 'func': 'mkGi'},
	{'label': 'nrmlChk', 'func': 'mkNrml'},
	{'label': 'reflChk', 'func': 'mkRefl'},
	{'label': 'refFiltrChk', 'func': 'mkReflFilter'},
	{'label': 'refRawChk', 'func': 'mkReflRaw'},
	{'label': 'refxChck', 'func': 'mkRfract'},
	{'label': 'refxFilterChk', 'func': 'mkRfractFilter'},
	{'label': 'refxRawChk', 'func': 'mkRfractRaw'},
	{'label': 'selfIllumChk', 'func': 'mkSelIllum'},
	{'label': 'shdChk', 'func': 'mkShdw'},
	{'label': 'shdMatChk', 'func': 'mkmatShdw'},
	{'label': 'shdRawChk', 'func': 'mkShdwRaw'},
	{'label': 'specChk', 'func': 'mkSpec'},
	{'label': 'sssChk', 'func': 'mkSSS'},
	{'label': 'atmoChk', 'func': 'mkAtmo'},
	{'label': 'bgChk', 'func': 'mkBG'},
	{'label': 'causticsChk', 'func': 'mkCaustics'},
	{'label': 'BumpChk', 'func': 'mkBumpNml'},
	{'label': 'coverageChk', 'func': 'mkCov'},
	{'label': 'DRChk', 'func': 'mkDr'},
	{'label': 'extraTexChk', 'func': 'mkExTex'},
	{'label': 'matIDChk', 'func': 'mkMatID'},
	{'label': 'materialSelectChk', 'func': 'mkMatSel'},
	{'label': 'multiMatChk', 'func': 'mkMultiMatte'},
	{'label': 'objIDchk', 'func': 'mkObjID'},
	{'label': 'renderIDChk', 'func': 'mkRenID'},
	{'label': 'sampleRateChk', 'func': 'mkSampleRate'},
	{'label': 'VelocityChck', 'func': 'mkVelocity'},
	{'label': 'ZdepthChk', 'func': 'mkZ'},
	{'label': 'LightSelectChk', 'func': 'mkLS'},
	{'label': 'FallOffCeck', 'func': 'createFalloffTexNode'},
	{'label': 'UVCheck', 'func': 'createUVTexNode'},
	{'label': 'XYZCheck', 'func': 'createXYZTexNode'},
	{'label': 'GrimeCheck', 'func': 'mkDirt'},
	{'label': 'Grime3dCheck', 'func': 'mkDirt3d'},
	]

# # ------------------------------------------------------
# # --------------- Launch UI      -----------------------
# # ------------------------------------------------------
def vrayReUI():
	if cmds.dockControl('vrayRendElem', exists=True):
		cmds.deleteUI('vrayRendElem', ctl=True)
	awVrayRETools = cmds.loadUI (f = 'Q:/Tools/maya/2012/scripts/python/UI/awRenderElem.ui')
	awVrayREPane = cmds.paneLayout (cn = 'single', parent = awVrayRETools)
	awVrayDock = cmds.dockControl ( 'vrayRendElem',allowedArea = ("right","left"), area = "right", floating = False ,con = awVrayRETools, label = 'Render Element tools')
	vrayUpdateUI()
	
def vrayUpdateUI():
	vrayUpdateInSceneUI()
	vrayUpdateActiveInLayerUI()
	renderLayerUpdateUI()
	# vrayUpdateInSceneElemUI("Buffers","PresetList")
	# vrayUpdateInSceneElemUI("Layers","PresetListRenderLayer")
	# awUpdateRenderLayerUI()
# # ------------------------------------------------------
# # --------------- Render Layers  -----------------------
# # ------------------------------------------------------
def awUpdateRenderLayerUI():
	cmds.textScrollList('PresetListRenderLayer_2',e=True, ra=True)
	layers = getRenderLayers()
	layers.sort()
	cmds.textScrollList('PresetListRenderLayer_2',e=True, append = layers)

def getRenderLayers():
	getRenderLayers = []
	getCurrentRenderLayer = cmds.editRenderLayerGlobals(q=True,currentRenderLayer=True)
	getAllRenderlayers = cmds.ls(':*', type='renderLayer')
	for entry in getAllRenderlayers:
		if not('defaultRenderLayer' in entry):
			getRenderLayers.append(entry)
	renderLayers = []
	if (getCurrentRenderLayer != 'defaultRenderLayer'):
	    renderLayers.append( getCurrentRenderLayer )
	for x in getRenderLayers:
		if ( x != getCurrentRenderLayer):
			renderLayers.append(x)
	return renderLayers
	
def changeRenderLayers():
	currentLayer = cmds.optionMenu('CurrentLayer', q=True, v=True)
	cmds.editRenderLayerGlobals(currentRenderLayer = currentLayer, eaa = True)
	vrayUpdateUI()
	
def renderLayerUpdateUI():
	renderLayers = getRenderLayers()
	itemsToDelete = cmds.optionMenu( 'CurrentLayer' , q=True, ill=True)
	if (itemsToDelete != None):
		for y in itemsToDelete:
			cmds.deleteUI(y, mi=True)
	for x in renderLayers:
		cmds.menuItem(p='CurrentLayer', label=x)
# # ------------------------------------------------------
# # ---------- Scene Render Elements ---------------------
# # ------------------------------------------------------
def getVrayRenderElements():
	vrayRE = cmds.ls( type='VRayRenderElement')
	return vrayRE
		
def vrayUpdateInSceneUI():
	reList = getVrayRenderElements()
	cmds.textScrollList('vraySceneRE', edit=True,removeAll=True)
	for x in reList:
		cmds.textScrollList('vraySceneRE', edit=True,append=x)
	
def vraySelectedSceneRE():
	selectedRenderElm = cmds.textScrollList('vraySceneRE',q=True, si=True)
	return selectedRenderElm
	
# # ------------------------------------------------------
# # ---------- Layer Render Elements ---------------------
# # ------------------------------------------------------
def vrayUpdateActiveInLayerUI():
	inSceneRE = getVrayRenderElements()
	activeRenderElem = []
	cmds.textScrollList('vrayLayerRE', edit=True,removeAll=True)
	for x in inSceneRE:
		reEnabled = cmds.getAttr((x + '.enabled'), asString=True)
		if ( reEnabled == True ):
			activeRenderElem.append(x)
	cmds.textScrollList('vrayLayerRE', edit=True,append=activeRenderElem)
	
def vraySelectedActiveRE():
	selectedActiveRenderElm = cmds.textScrollList('vrayLayerRE',q=True, si=True)
	return selectedActiveRenderElm
# # ------------------------------------------------------
# # ---------------- ACTION BUTTONS  ---------------------
# # ------------------------------------------------------
def vrayEditREButton ( buttonPush ):
	selectedSceneRE = vraySelectedSceneRE()
	selectedActiveRE = vraySelectedActiveRE()
	if (buttonPush == 'enable'):
		if (selectedSceneRE != None):
			for x in selectedSceneRE:
				attr = (x + '.enabled')
				cmds.editRenderLayerAdjustment(attr)
				cmds.setAttr(attr, 1);
			vrayUpdateUI()
		else:
			cmds.warning('No Render Elements are selected.  Please Select a Render Elements in Scene.')
	if (buttonPush == 'disable'):
		if (selectedActiveRE != None):
			for x in selectedActiveRE:
				attr = (x + '.enabled')
				cmds.editRenderLayerAdjustment(attr)
				cmds.setAttr(attr, 0);
			vrayUpdateUI()
		else:
			cmds.warning('No Render Elements are selected.  Please Select a Render in Render Layer.')
	if (buttonPush == 'delete'):
		if (selectedSceneRE != None):
			for x in selectedSceneRE:
				cmds.delete(x)
			vrayUpdateUI()
		else:
			cmds.warning('No Render Elements are selected.  Please Select a Render Elements in Scene.')
			
def batchLayers( button ):
	renderLayers = getRenderLayers()
	allRenderLayers = []
	for layer in renderLayers:
		if (layer != 'defaultRenderLayer'):
			allRenderLayers.append(layer)
	renderElements = getVrayRenderElements()
	selectedSceneRE = vraySelectedSceneRE()
	condition = 0
	warningTxt = ''
	if (selectedSceneRE == None):
		if ( button == 'add'):
			condition = 1
			warningTxt = 'All Vray Render elements have been enabled in All render layers.'
		if (button == 'remove'):
			condition = 0
			warningTxt = 'All Vray Render elements have been disable in All render layers.'
		for x in allRenderLayers:
			cmds.editRenderLayerGlobals(currentRenderLayer = x, eaa = True)
			for y in renderElements:
				attr = (y + '.enabled')
				cmds.editRenderLayerAdjustment(attr)
				cmds.setAttr(attr, condition);
				print (attr + ' '+str(condition))
	else:
		if ( button == 'add'):
			condition = 1
			warningTxt = 'Selected Vray Render elements have been enabled in All render layers.'
		if (button == 'remove'):
			condition = 0
			warningTxt = 'Selected Vray Render elements have been disable in All render layers.'
		for x in allRenderLayers:
			cmds.editRenderLayerGlobals(currentRenderLayer = x, eaa = True)
			for y in selectedSceneRE:
				attr = (y + '.enabled')
				cmds.editRenderLayerAdjustment(attr)
				cmds.setAttr(attr, condition)
				print (attr + ' '+str(condition))
	vrayUpdateUI()
	cmds.warning(warningTxt)

# #-------------------------
# #----- Create Vray Elements
# #-------------------------
def VrayCreateElem():
	for entry in vrayLayers:
		if cmds.checkBox(entry['label'],q=True,v=True):	
			CreatRE(entry,'func')
	vrayUpdateUI()

def CreatRE(entry,func):
	mkRunMel="source \"Q:/Tools/maya/2012/scripts/mel/mkVRayRenderElements.mel\"; "+entry[func]+";"
	mel.eval (mkRunMel)
	mel.eval ("source \"Q:/Tools/maya/2012/scripts/mel/mkVRayRenderElements.mel\"; awVrayReFix;")
	vrayUpdateUI()
# #------------------------------------------------------
# #-----Presets------------------------------------------
# #------------------------------------------------------
# def DelZoicPresets():
	# presetCode = cmds.textScrollList('PresetList',q=True,si=True)
	# DisableZoicPreset(presetCode)

def mkFixVrayNames():
	mel.eval ("source \"Q:/Tools/maya/2012/scripts/mel/mkVRayRenderElements.mel\"; awVrayReFix;")
#------------------------------
#--update preset list ui-------
#------------------------------
# buffers
def vrayUpdateInSceneElemUI(type,guiScrollList):
	fileInfo= awFileInfo()
	cmds.textScrollList(guiScrollList, edit=True,removeAll=True)
	mkProj = GetZoicPresets(type)
	mkProj.sort()
	for x in mkProj:
		if (x['display'] == 'Complex') or (x['display'] == 'Simple'):
			cmds.textScrollList(guiScrollList, edit=True,append=x["display"])
	for y in mkProj:
# 		if (y['display'] != 'Complex') and (y['display'] != 'Simple'):
		if not ((y['display'] == 'Complex') or (y['display'] == 'Simple')):
			cmds.textScrollList(guiScrollList, edit=True,append=y["display"])

# #-----------------------------------------------------
# #--------Save Preset----------------------------------
# #-----------------------------------------------------
def mkSavePreset(value,Type):
	if value == "new":
		mkType= Type
		if mkType == "Buffers":
			mkDicValue 			=[]
			cmds.promptDialog(t='Preset name',m='enter preset name')
			mkfilename			=cmds.promptDialog(query = True, text = True)
			mkfilename=mkfilename.replace(' ' , '_')
			for entry in vrayLayers:
				if cmds.checkBox(entry['label'],q=True,v=True):
					mkDicValue.append(entry)
			fileInfo=			awFileInfo()
			mkProj =			mkProjName(fileInfo)
			mkDir =				mkProj+"/assets/3D/data/Scripts/Presets"
			output =			mkProj+"/assets/3D/data/Scripts/Presets/"+mkfilename+"_Render_Element"
			if not os.path.exists(mkDir):
				os.makedirs(mkDir)
			createPickleFile( mkDicValue,output )
			createShotgunData( mkfilename+"_Render_Element", fileInfo, output,mkType)
			vrayUpdateUI()
		if mkType == "Layers":
			mkLayerName = []
			for i in range (int (RlCount)):
				mkRlName = cmds.textFieldGrp(TxtFg[i], text = True,query = True)
				mkLayerName.append(mkRlName)
			mkDicValue 			=mkLayerName
			cmds.promptDialog(t='Preset name',m='enter preset name')
			mkRpreFilename		=cmds.promptDialog(query = True, text = True)
			mkRpreFilename = mkRpreFilename.replace(' ','_')
			print mkRpreFilename
			fileInfo=			awFileInfo()
			mkProj =			mkProjName(fileInfo)
			mkDir =				mkProj+"/assets/3D/data/Scripts/Presets"
			output =			mkProj+"/assets/3D/data/Scripts/Presets/"+mkRpreFilename+"_Render_Layer"
			if not os.path.exists(mkDir):
				os.makedirs(mkDir)
			createPickleFile( mkDicValue,output )
			createShotgunData( mkRpreFilename+"_Render_Layer", fileInfo, output,mkType)
			vrayUpdateUI()
	if value == "exists":
		selectedFiles = cmds.textScrollList('PresetListRenderLayer_2',q=True, si=True)
		mkLayerName = selectedFiles
		mkType = "Layers"
		mkDicValue 			=mkLayerName
		cmds.promptDialog(t='Preset name',m='enter preset name')
		mkRLfilename			=cmds.promptDialog(query = True, text = True)
		fileInfo=			awFileInfo()
		mkProj =			mkProjName(fileInfo)
		mkDir =				mkProj+"/assets/3D/data/Scripts/Presets"
		output =			mkProj+"/assets/3D/data/Scripts/Presets/"+mkRLfilename+"_Render_Layer"
		if not os.path.exists(mkDir):
			os.makedirs(mkDir)
		createPickleFile( mkDicValue,output )
		createShotgunData( mkRLfilename+"_Render_Layer", fileInfo, output,mkType)
		vrayUpdateUI()

# #-----------------------------------------------------
# #--------file Info----------------------------------
# #-----------------------------------------------------
	
def awFileInfo():
	fileInfo		= cmds.file ( q = True, sceneName = True)
	if fileInfo == "":
		cmds.warning( 'no scene open')
		return "crd"
	else:
		fileInfo		= fileInfo.split ( "/" )
		return fileInfo
def mkProjName(fileInfo):
	ProjInfo = fileInfo[0:3]
	ProjInfo="/".join(ProjInfo)
	return ProjInfo
# #-----------------------------------------------------
# #--------Pickle Files----------------------------------
# #-----------------------------------------------------
def createPickleFile( data, path ):
	file =		open( path, 'w')
	pic =		cPickle.Pickler(file)
	pic.dump( data )
	file.close()
	return data
def getPickleFile( path ):
	file =		open( path, 'r')
	pic =		cPickle.Unpickler(file)
	data =		pic.load()
	return data
# #-----------------------------------------------------
# #--------Shotgun Upload----------------------------------
# #-----------------------------------------------------

def createShotgunData( presetCode, fileInfo, presetPath ,PressetType):

	linkType = fileInfo[3]
	link = {}
	if linkType == 'assets':
		link = sg.find_one("Asset",filters=[ ['code', 'is', fileInfo[6] ] ], fields=['id', 'project', 'sg_episode'],)
	else :
		link = sg.find_one("Shot",filters=[ ['code', 'is', fileInfo[6] ] ], fields=['id', 'project', 'sg_episode'],)

	presetInfo = {
		'project'			: { 'type' : link['project']['type'],		'id':link['project']['id'] },
		'sg_episode'		: { 'type' : link['sg_episode']['type'],	'id':link['sg_episode']['id'] },
		'sg_link'			: { 'type' : link['type'],					'id':link['id'] },
		'sg_status_list'	: 'act',
		'code'				: str(presetCode),
		'sg_type'			: PressetType,
	}

	# Upload Preset Data
	presetData = sg.find_one("CustomEntity16",filters=[ ['project', 'is', presetInfo['project'] ], ['code', 'is', presetInfo['code'] ] ], filter_operator ='all', fields=['all'],)
	if presetData == None :
		presetData = sg.create( 'CustomEntity16', presetInfo )
	else :
		presetData = sg.update( 'CustomEntity16', presetData['id'] , presetInfo )
	sg.upload("CustomEntity16", presetData['id'], presetPath, "sg_preference_file", "Buffer_Data")

# #-----------------------------------------------------
# #--------Loading presets----------------------------------
# #-----------------------------------------------------

def LoadZoicPresets(X):
	if X == "Buffers":
		presetDic =GetZoicPresets("Buffers")
		presetCode = cmds.textScrollList('PresetList',q=True,si=True)
		if presetCode != None :
			for y in presetDic:
				if (y["display"] == presetCode[0]):
					PreCode= y["code"]
					presetData = None
					if PreCode == "Simple":
						presetProj = { 'type' : 'Project', 'id' : 172 }
						presetData = sg.find_one("CustomEntity16",filters=[ ['code', 'is', 'Simple' ], [ 'project', 'is', presetProj ] ], fields=['sg_preference_file'],)
					elif PreCode == "Complex":
						presetProj = { 'type' : 'Project', 'id' : 172 }
						presetData = sg.find_one("CustomEntity16",filters=[ ['code', 'is', 'Complex' ], [ 'project', 'is', presetProj ] ], fields=['sg_preference_file'],)
						# pprint( presetData )
					else:
						presetProj = sg.find_one("Project",filters=[ ['name', 'is', awFileInfo()[2] ] ], fields=[ 'project'],)
						presetData = sg.find_one("CustomEntity16",filters=[ ['code', 'is', PreCode ], [ 'project', 'is', presetProj ] ], fields=['sg_preference_file'],)
					if presetData != None and presetData['sg_preference_file'] != None :
						url 	= presetData['sg_preference_file']['url'] + '/' + presetData['sg_preference_file']['name']
						url 	= url.split( '/file_serve/attachment/' ) #, '/storage/production/files/' )
						urlID	= int(os.path.dirname( url[1] ))
						urlID = str(1000000000000 + urlID)
						urlPath = url[0] + '/storage/production/files/' + urlID[1:5] + "/" + urlID[5:9] + "/" + urlID[9:13] + "/" + PreCode 
						pic = urllib2.urlopen( urlPath ).read()
						entryList = pickle.loads( pic )
						for entry in entryList:
							CreatRE(entry,'func')
					vrayUpdateUI()
	if X == "Layers":
		presetDic =GetZoicPresets("Layers")
		presetCode = cmds.textScrollList('PresetListRenderLayer',q=True,si=True)
		if presetCode != None :
			for y in presetDic:
				if (y["display"] == presetCode[0]):
					PreCode= y["code"]
					presetData = None
					if PreCode == "Simple":
						presetProj = { 'type' : 'Project', 'id' : 172 }
						presetData = sg.find_one("CustomEntity16",filters=[ ['code', 'is', 'Simple' ], [ 'project', 'is', presetProj ] ], fields=['sg_preference_file'],)
					elif PreCode == "Complex":
						presetProj = { 'type' : 'Project', 'id' : 172 }
						presetData = sg.find_one("CustomEntity16",filters=[ ['code', 'is', 'Complex' ], [ 'project', 'is', presetProj ] ], fields=['sg_preference_file'],)
						pprint( presetData )
					else:
						presetProj = sg.find_one("Project",filters=[ ['name', 'is', awFileInfo()[2] ] ], fields=[ 'project'],)
						presetData = sg.find_one("CustomEntity16",filters=[ ['code', 'is', PreCode ], [ 'project', 'is', presetProj ] ], fields=['sg_preference_file'],)
					if presetData != None and presetData['sg_preference_file'] != None :
						url 	= presetData['sg_preference_file']['url'] + '/' + presetData['sg_preference_file']['name']
						url 	= url.split( '/file_serve/attachment/' ) #, '/storage/production/files/' )
						urlID	= int(os.path.dirname( url[1] ))
						urlID = str(1000000000000 + urlID)
						urlPath = url[0] + '/storage/production/files/' + urlID[1:5] + "/" + urlID[5:9] + "/" + urlID[9:13] + "/" + PreCode
						pic = urllib2.urlopen( urlPath ).read()
						entryList = pickle.loads( pic )
						for entry in entryList:
							mkCreateRL(entry)
					vrayUpdateUI()

# #-----------------------------------------------------
# #--------get presets form shotgun---------------------
# #-----------------------------------------------------

def GetZoicPresets( preType):

	currentProject	= sg.find_one("Project",filters=[ ['name', 'is', awFileInfo()[2] ] ], fields=[ 'project'],)
	defaultProj		= { 'type' : 'Project', 'id' : 172 }
	presetData = []
	presetData.extend( sg.find("CustomEntity16",filters=[ [ 'project', 'is', currentProject ],[ 'sg_status_list', 'is', 'act' ],[ 'sg_type', 'is', preType ] ], fields=['code'],)  )
	#presetData.extend( sg.find("CustomEntity16",filters=[ [ 'project', 'is', defaultProj ],[ 'sg_status_list', 'is', 'act' ] ], fields=['code'],)  )
	if (preType == 'Buffers'):
		presetData.extend( sg.find("CustomEntity16",filters=[ [ 'project', 'is', defaultProj ],[ 'sg_status_list', 'is', 'act' ], [ 'sg_type', 'is', preType ]], fields=['code'],)  )
	presetList = []
	display = []
	presetDic =[]
	preTypeStr =[]
	for preset in presetData :
		presetList =( [ preset['code'] ] )
		for entry in presetList:
			if preType == "Buffers":
				display = (entry.replace("_Render_Element",""))
				preTypeStr =("Buffers")
				preList = entry
				presetDic.append({'type':preTypeStr,'code':preList, 'display':display})
			if preType == "Layers":
				display = (entry.replace("_Render_Layer",""))
				preTypeStr =("Layers")
				preList = entry
				presetDic.append({'type':preTypeStr,'code':preList, 'display':display})
	return presetDic

# #-----------------------------------------------------
# #--------number up Down-------------------------
# #-----------------------------------------------------

def awVersionButton( guiUpDown , guiBox ):
	value = cmds.textField( guiBox , q=True, tx=True)
	value = int(value)
	if(guiUpDown == 'Plus'):
		value = value + 1
	if(guiUpDown == 'Minus'):
		value = value -1
	value = str( value).zfill ( 3 )
	cmds.textField( guiBox, e=True,tx= value)

# #-----------------------------------------------------
# #--------Create REnder Layers-------------------------
# #-----------------------------------------------------

def mkGetRlCount():
	RLnumber = cmds.textField('awRenderLayerNumber',q=True,tx=True)
	RLnumber=int(RLnumber)
	mkMakeRlUI(RLnumber)
	return RLnumber

def mkMakeRlUI(count):
	global RlCount
	RlCount = count
	if cmds.window('mkRLWin', exists=True):
		cmds.deleteUI('mkRLWin', window=True)
	mkRenderLw = cmds.window ('mkRLWin',title = "mk make render layers",wh = (512,256))
	cmds.scrollLayout()
	global TxtFg
	TxtFg = []
	for i in range (int(count)):
		TxtFgTemp = cmds.textFieldGrp(label = "     "+'Render Layer'+"  " +'%d' %i+"            ", tx = 'enter_name', )
		TxtFg.insert(i,TxtFgTemp)
		cmds.separator ()
	cmds.separator ()
	cmds.columnLayout( adjustableColumn=True )
	cmds.rowLayout (nc = 4)
	cmds.button (label = 'Add to Scene',command ="import sys\nsys.path.append( 'Q:/Tools/maya/2012/scripts/python' )\nimport awVrayRenderElementHelper\nreload(awVrayRenderElementHelper)\nawVrayRenderElementHelper.mkApllyRL()")
	cmds.separator ()
	cmds.button (label = 'Save as Preset ',command = "import sys\nsys.path.append( 'Q:/Tools/maya/2012/scripts/python' )\nimport awVrayRenderElementHelper\nreload(awVrayRenderElementHelper)\nawVrayRenderElementHelper.mkSavePreset('new','Layers')")
	cmds.showWindow (mkRenderLw)
	
def mkApllyRL():
	mkLayerName = []
	for i in range (int (RlCount)):
		mkRlName = cmds.textFieldGrp(TxtFg[i], text = True,query = True)
		mkLayerName.append(mkRlName)
		mkRlexists = cmds.ls (mkRlName, type = 'renderLayer')
		if mkRlexists == []:
			cmds.createRenderLayer(n = mkRlName,empty = True)
	vrayUpdateUI()

def mkCreateRL(name):
	mkRlexists = cmds.ls (name, type = 'renderLayer')
	if mkRlexists == []:
		cmds.createRenderLayer(n = name,empty = True)
	vrayUpdateUI()


