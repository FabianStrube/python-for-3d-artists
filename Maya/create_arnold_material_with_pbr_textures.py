# Creates a standard surface material from a given dictionary that includes information about a pbr-texture set

# Add entries to this dictionary and make sure the key value matchens the material_input dict keys below
material_dictionary = {
    "diffuse": "example/path/to/diffuse/texture.jpg",
    "roughness": "example/path/to/roughness/texture.jpg",
    "bump": "example/path/to/bump/texture.jpg",
    "displacement": "example/path/to/displacement/texture.jpg"
}

def create_arnold_material_with_pbr_textures(material_dictionary):
    # Import Modules
    import maya.cmds as cmds
    import os

    # Create Material
    aiMaterial = cmds.shadingNode("aiStandardSurface", asShader=True, n="NewStandardSurface")
    aiMaterialSG = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, n="NewStandardSurface_SG")
    cmds.connectAttr('%s.outColor' % aiMaterial, '%s.surfaceShader' % aiMaterialSG)

    # Set Channels
    standard_surface_inputs = {
        'diffuse': [".outColor", ".baseColor"],
        'ao': [".outColor.outColorR", ".base"],
        'reflection': [".outColor.outColorR", ".specular"],
        'refraction': [".outColor.outColorR", ".transmission"],
        'subsurface': [".outColor", ".subsurfaceColor"],
        'displacement': [".outColor.outColorR", ".displacement"],
        'roughness': [".outColor.outColorR", ".specularRoughness"],
        'metalness': [".outColor.outColorR", ".metalness"],
        'opacity': [".outColor", ".opacity"],
        'emission': [".outColor", ".emissionColor"],
        'bump': [".outColor.outColorR", ".bumpMap"],
        'normal': [".outColor", ".input"],
        'coat': [".outColor.outColorR", ".coat"]
    }


    channelFileList = []

    # Loop over each channel
    for channel in standard_surface_inputs.keys():
        if channel in material_dictionary:
            # Create File Texture
            fileName = os.path.split(material_dictionary[channel])[0]
            file = cmds.shadingNode("aiImage", asTexture=True, n=fileName)
            
            # Set color space
            if standard_surface_inputs[channel][0] == ".outColor":
                cmds.setAttr(file + ".colorSpace", 'sRGB', type="string")
            else:
                cmds.setAttr(file + ".colorSpace", 'Raw', type="string")

            # Set file rules and path
            cmds.setAttr(file + ".ignoreColorSpaceFileRules", 1)
            cmds.setAttr(file + ".filename", material_dictionary[channel], typ="string")
            channelFileList.append(file)

            if channel == "bump":
                bumpNode = cmds.shadingNode("aiBump2d", asTexture=True, n=fileName + "_bumpNode")
                cmds.connectAttr(file + standard_surface_inputs[channel][0], bumpNode + standard_surface_inputs[channel][1])    
                cmds.connectAttr(bumpNode + ".outValue", aiMaterial + ".normalCamera")

            elif channel == "normal":
                normalNode = cmds.shadingNode("aiNormalMap", asTexture=True, n=fileName + "_normalNode")
                cmds.connectAttr(file + standard_surface_inputs[channel][0], normalNode + standard_surface_inputs[channel][1])
                
                if "bump" in material_dictionary:
                    cmds.connectAttr(normalNode + ".outValue", bumpNode + ".normal")

                else:
                    cmds.connectAttr(normalNode + ".outValue", aiMaterial + ".normalCamera")

            elif channel == "displacement":
                displacementNode = cmds.shadingNode("displacementShader", asShader=True, n=fileName + "_displacementNode")
                cmds.connectAttr(file + standard_surface_inputs[channel][0], displacementNode + standard_surface_inputs[channel][1])                  
                cmds.connectAttr(displacementNode + ".displacement", aiMaterialSG + ".displacementShader")

            else:
                cmds.connectAttr(file + standard_surface_inputs[channel][0], aiMaterial + standard_surface_inputs[channel][1])


    # Connect all file nodes to place 2d texture nodes
    if len(channelFileList) > 0:
        p2d = cmds.shadingNode('place2dTexture', name="place2d", asUtility=True)
        for file in channelFileList:
            cmds.connectAttr(p2d + ".outUV", file + ".uvcoords")
            cmds.connectAttr(p2d + ".offset.offsetU", file + ".soffset")
            cmds.connectAttr(p2d + ".offset.offsetV", file + ".toffset")
            cmds.connectAttr(p2d + ".repeatUV.repeatU", file + ".sscale")
            cmds.connectAttr(p2d + ".repeatUV.repeatV", file + ".tscale")
            cmds.connectAttr(p2d + ".mirrorU", file + ".sflip")
            cmds.connectAttr(p2d + ".mirrorV", file + ".tflip")


