# Creates file node and connects texture to it

def create_file_node(filepath):
    import maya.cmds as cmds
    import os

    fileNodeName = os.path.splitext(os.path.split(filepath)[1])[0]

    fileNode = cmds.shadingNode("file", asTexture=True, n=fileNodeName)
    cmds.setAttr(fileNode + ".fileTextureName", filepath, type="string")

    # Connect file node to place 2d texture
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