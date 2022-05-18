import maya.cmds as cmds
import maya.mel as mel
import re

#deletes old window and preference, if it still exists
if(cmds.window('uiWrapper_obj', q=1, ex=1)):
    cmds.deleteUI('uiWrapper_obj')
if(cmds.windowPref('uiWrapper_obj', q=1, ex=1)):
    cmds.windowPref('uiWrapper_obj', r=1)
    
def dirPath(filePath, fileType):
    cmds.textFieldButtonGrp('Dir', edit=True, text=str(filePath))
    return 1

def startExport(path):
    curentObjectSelection = cmds.ls(sl=1,fl=1)
    filePathStr = cmds.textFieldButtonGrp('Dir', query = True, text = True)
    for item in curentObjectSelection:
        exportDir = "%s/%s.obj"%(filePathStr, item)
        try:
            cmds.select(item)
            mel.eval('file -force -options "groups=0;ptgroups=0;materials=0;smoothing=1;normals=1" -typ "OBJexport" -pr -es "%s";'%(exportDir))
            print(exportDir)
        except:
            print("Ignoring object named: '%s'. Export failed, probably not a polygonal object. "%(item))
    print("Exporting Complete!")

def browseIt():
    cmds.fileBrowserDialog( m=4, fc=dirPath, ft='folder', an='Choose Folder')
    return
##import


    
def startImport():
    newGeos = []
    #int(startFrame) + int(4)
    objGroup = None

    files_to_import = cmds.fileDialog2(fileFilter =  '*.obj', dialogStyle = 2, caption = 'import multiple obj files', fileMode = 4)
    for i in files_to_import:
        returnedNodes = cmds.file('%s' % i, i = True, type = "OBJ", rnn=True, ignoreVersion = True, options = "mo=0",renameAll=True,  loadReferenceDepth  = "all"  )
        fileName = re.sub('[^0-9a-zA-Z]', '_', (i.split('/')[-1])[0:-4])
        newGeo = ('%s' % fileName)
        tempGeoName = fileName + "_polySurface1"

        if newGeo not in cmds.ls():
            newGeo = cmds.rename(tempGeoName, newGeo)
            newGeos.append(newGeo)
        else:
            
            newGeo = cmds.rename(tempGeoName,(("%s_"+ str (+1)) % newGeo))
            newGeos.append(newGeo)


def makeGui():
    uiWrapper_obj = cmds.window('uiWrapper_obj',width=300,title="Batch Imp Exp",height=180,menuBar=1,backgroundColor=[0.2, 0.2, 0.2])
    cmds.formLayout('uiWrapper_gui', w = 180, parent = 'uiWrapper_obj' )
    
    cmds.textFieldButtonGrp('Dir', text="Path to export folder",buttonLabel='Browse',backgroundColor=[0.1, 0.1, 0.1],highlightColor=[0.0, 0.0, 0.0], buttonCommand=browseIt, parent = 'uiWrapper_gui') 
    
    cmds.button('button1a', label='Export Selected',backgroundColor=[0.76, 0.67, 0.89],highlightColor=[0.0, 0.0, 0.0], command=startExport, parent = 'uiWrapper_gui', align='center', width=150, height=50) 
    cmds.button('button2b', label='Import Selected',backgroundColor=[0.76, 0.67, 0.89],highlightColor=[0.0, 0.0, 0.0], command=startImport, parent = 'uiWrapper_gui', align='center', width=150, height=50) 
    cmds.formLayout('uiWrapper_gui',e=1,attachForm=[['button1a', 'top', 40], ['button1a', 'left', 75], ['button2b', 'top', 110], ['button2b', 'left', 75]])
    cmds.showWindow('uiWrapper_obj')
makeGui()
