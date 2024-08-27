# Opens scenefiles in blender | Supports: Blend

def open_scenefile(filepath):
    import bpy

    bpy.ops.wm.open_mainfile(filepath=filepath)