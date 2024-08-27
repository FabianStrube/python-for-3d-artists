# Creates skydome and connects hdri, if skydome selected it changes the hdri path

def import_hdri(filepath):
    import maya.cmds as cmds
    import os

    selectionIsSkyDome = False
    # Get current selection
    sel = cmds.ls(selection=True)

    # Search in the selection for a aiSkyDomeLight shape
    if len(sel) > 0:
        for each in sel: 
            try:
                shape = cmds.listRelatives(each, shapes=True)[0]
                shapeType = cmds.objectType( shape )

                if shapeType == "aiSkyDomeLight":
                    selectionIsSkyDome = True
                    skyDome = shape
                    break
            except:
                pass

    # If a aiSkyDomeLight was found replace its connected texture path
    if selectionIsSkyDome:
        connections = cmds.listConnections( skyDome + ".color" )
        for c in connections:
            if cmds.objectType(c) == "file":
                cmds.setAttr(c + ".fileTextureName", filepath, typ="string")
                break

    # Else create a new aiSkyDome and a filenode and connect it
    else:
        skyDome = cmds.shadingNode("aiSkyDomeLight",asLight=True)
        skyDome = cmds.rename(skyDome, "aiSkyDomeLight")
        fileNode = cmds.shadingNode("file", asTexture=True, n=os.path.split(filepath)[1])
        cmds.setAttr(fileNode + ".colorSpace", "Raw", type="string")
        cmds.setAttr(fileNode + ".ignoreColorSpaceFileRules", 1)
        cmds.setAttr(fileNode + ".fileTextureName", filepath, typ="string")
        cmds.connectAttr(fileNode + ".outColor", skyDome + ".color")

        p2d = cmds.shadingNode('place2dTexture', name="place2d", asUtility=True)
        cmds.connectAttr(p2d + ".outUV", fileNode + ".uvCoord")
        cmds.connectAttr(p2d + ".outUvFilterSize", fileNode + ".uvFilterSize")
        cmds.connectAttr(p2d + ".vertexCameraOne", fileNode + ".vertexCameraOne")
        cmds.connectAttr(p2d + ".vertexUvOne", fileNode + ".vertexUvOne")
        cmds.connectAttr(p2d + ".vertexUvThree", fileNode + ".vertexUvThree")
        cmds.connectAttr(p2d + ".vertexUvTwo", fileNode + ".vertexUvTwo")
        cmds.connectAttr(p2d + ".coverage", fileNode + ".coverage")
        cmds.connectAttr(p2d + ".mirrorU", fileNode + ".mirrorU")
        cmds.connectAttr(p2d + ".mirrorV", fileNode + ".mirrorV")
        cmds.connectAttr(p2d + ".noiseUV", fileNode + ".noiseUV")
        cmds.connectAttr(p2d + ".offset", fileNode + ".offset")
        cmds.connectAttr(p2d + ".repeatUV", fileNode + ".repeatUV")
        cmds.connectAttr(p2d + ".rotateFrame", fileNode + ".rotateFrame")
        cmds.connectAttr(p2d + ".rotateUV", fileNode + ".rotateUV")
        cmds.connectAttr(p2d + ".stagger", fileNode + ".stagger")
        cmds.connectAttr(p2d + ".translateFrame", fileNode + ".translateFrame")
        cmds.connectAttr(p2d + ".wrapU", fileNode + ".wrapU")
        cmds.connectAttr(p2d + ".wrapV", fileNode + ".wrapV")