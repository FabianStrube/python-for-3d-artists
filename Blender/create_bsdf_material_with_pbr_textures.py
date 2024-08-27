# Creates a bsdf material from a given dictionary that includes information about a pbr-texture set

# Add entries to this dictionary and make sure the key value matchens the material_input dict keys below
material_dictionary = {
    "diffuse": "example/path/to/diffuse/texture.jpg",
    "roughness": "example/path/to/roughness/texture.jpg",
    "bump": "example/path/to/bump/texture.jpg",
    "displacement": "example/path/to/displacement/texture.jpg"
}

def create_bsdf_material_with_pbr_textures(material_dictionary):
    import bpy
    
    # Create material
    material = bpy.data.materials.new(name="NewBSDFMaterial")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create output node
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (1600, 0)  # Adjust the position as needed
    
    # Create principled BSDF node
    principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled_node.location = (1200, 0)  # Adjust the position as needed
    links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])
    
    # Dictionary mapping channel names to corresponding inputs in the shader nodes
    bsdf_inputs = {
        'diffuse': principled_node.inputs['Base Color'],
        'reflection': principled_node.inputs['Specular IOR Level'],
        'refraction': principled_node.inputs['Transmission Weight'],
        'subsurface': principled_node.inputs['Subsurface Weight'],
        'displacement': output_node.inputs['Displacement'],
        'roughness': principled_node.inputs['Roughness'],
        'metalness': principled_node.inputs['Metallic'],
        'opacity': principled_node.inputs['Alpha'],
        'emission': principled_node.inputs['Emission Color'],
        'bump': principled_node.inputs['Normal'],
        'normal': principled_node.inputs['Normal'],
        'coat': principled_node.inputs['Coat Weight']
        # Add more mappings as needed
    }
    
    # Add Maps that are color channels
    color_channel = ['diffuse', 'emission']
    
    # Create Texture coordinate and mapping node and connect mapping to texture vector
    mapping_node = nodes.new(type='ShaderNodeMapping')
    mapping_node.location = (0, 0)  # Adjust the position as needed
    texture_coordinate_node = nodes.new(type='ShaderNodeTexCoord')
    texture_coordinate_node.location = (-200, 0)  # Adjust the position as needed
    links.new(texture_coordinate_node.outputs['UV'], mapping_node.inputs['Vector'])

    # Set y coordinate
    y = 0
    
    for channel in bsdf_inputs.keys():
        if channel in material_dictionary:
            # Load image texture
            texture_node = nodes.new(type='ShaderNodeTexImage')
            texture_node.location = (400, y)  # Adjust the position as needed
            texture_node.image = bpy.data.images.load(material_dictionary[channel])
            
            if channel not in color_channel:
                # Set the color space to 'Non-Color'
                texture_node.image.colorspace_settings.name = 'Non-Color'

            links.new(mapping_node.outputs['Vector'], texture_node.inputs['Vector'])
                        
            # Adjust settings for normal map
            if channel == 'normal':
                normal_map_node = nodes.new(type='ShaderNodeNormalMap')
                normal_map_node.location = (800, y)
                links.new(texture_node.outputs['Color'], normal_map_node.inputs['Color'])
                if 'bump' in material_dictionary:
                    links.new(normal_map_node.outputs['Normal'], bump_node.inputs['Normal'])
                else:
                    links.new(normal_map_node.outputs['Normal'], principled_node.inputs['Normal'])
                
            # Adjust settings for bump map
            elif channel == 'bump':
                bump_node = nodes.new(type='ShaderNodeBump')
                bump_node.location = (800, y)
                links.new(texture_node.outputs['Color'], bump_node.inputs['Height'])
                links.new(bump_node.outputs['Normal'], principled_node.inputs['Normal'])

            # Adjust settings for displacement map
            elif channel == 'displacement':
                displacement_node = nodes.new(type='ShaderNodeDisplacement')
                displacement_node.location = (700, y)
                links.new(texture_node.outputs['Color'], displacement_node.inputs['Height'])
                links.new(displacement_node.outputs['Displacement'], output_node.inputs['Displacement'])

            else:
                # Connect texture node to material input
                links.new(texture_node.outputs[0], bsdf_inputs[channel])

            # Adjsut y coordiante
            y -= 400



            
