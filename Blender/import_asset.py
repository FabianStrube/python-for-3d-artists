# Import assets into blender | Supports: fbx, gltf, obj, dae, abc

def import_asset(filepath):
    import bpy
    import os

    # Get the file extension
    file_extension = os.path.splitext(filepath)[1].lower()

    if file_extension == '.fbx':
        bpy.ops.import_scene.fbx(filepath = filepath)
    elif file_extension == '.gltf':
        bpy.ops.import_scene.gltf(filepath = filepath)
    elif file_extension == '.obj':
        bpy.ops.wm.obj_import(filepath = filepath)
    elif file_extension == '.dae':
        bpy.ops.wm.collada_import(filepath = filepath)
    elif file_extension == '.abc':
        bpy.ops.wm.alembic_import(filepath = filepath)
    else:
        print(f"Unsupported file format: {file_extension}")