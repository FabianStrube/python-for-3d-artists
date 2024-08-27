# Creates arealight and connects texture to it | Supports: cycles/eevee

def create_area_light_with_texture(filepath):
    import bpy
    # Create a new area light
    bpy.ops.object.light_add(type='AREA', radius=1, align='WORLD', location=(0, 0, 2))
    # Get the newly created light object
    light_object = bpy.context.object

    # Add Use Nodes to the light object
    bpy.data.objects[light_object.name].data.use_nodes = True

    # Get the node tree of the light object
    node_tree = light_object.data.node_tree

    # Create a new texture node
    texture_node = node_tree.nodes.new('ShaderNodeTexImage')

    # Load the texture
    texture = bpy.data.images.load(filepath)
    texture_node.image = texture

    # Set the color space to 'Non-Color'
    texture_node.image.colorspace_settings.name = 'Non-Color'

    # Get the emission node
    emission_node = node_tree.nodes.get('Emission')

    # Connect the texture node to the color input of the emission node
    node_tree.links.new(texture_node.outputs['Color'], emission_node.inputs['Color'])