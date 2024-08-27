# Sets world enviroment and connects hdri. If a texture is already connected, it replaces the filepath | Supports: eevee/cycles

def import_environment_hdri(filepath):
    import bpy

    # Get the current scene
    current_scene = bpy.context.scene

    # Get the render engine
    current_renderer = current_scene.render.engine

    if current_renderer == "BLENDER_EEVEE" or current_renderer == "CYCLES":
        # Check if there is an existing world
        world = bpy.context.scene.world
        if not world:
            world = bpy.data.worlds.new("World")

        # Set the surface shader to 'background' for Eevee
        world.use_nodes = True
        bg_shader = world.node_tree.nodes.get('Background')
        if bg_shader is None:
            bg_shader = world.node_tree.nodes.new('ShaderNodeBackground')

        # Check if there's an existing texture node connected to the background shader
        existing_texture_node = None
        for node in world.node_tree.nodes:
            if node.type == 'TEX_ENVIRONMENT':
                existing_texture_node = node
                break

        if existing_texture_node:
            # Rename the existing texture node and update its path
            existing_texture_node.name = "Environment Texture"
            existing_texture_node.image = bpy.data.images.load(filepath)
        else:
            # Set up environment texture
            bg_texture_node = world.node_tree.nodes.new('ShaderNodeTexEnvironment')
            bg_texture_node.name = "Environment Texture"
            bg_texture_node.image = bpy.data.images.load(filepath)

            # Link texture to background shader
            world.node_tree.links.new(bg_texture_node.outputs['Color'], bg_shader.inputs['Color'])

        # Assign the world to the scene
        bpy.context.scene.world = world