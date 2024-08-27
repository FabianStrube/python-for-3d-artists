# Opens scenefiles in maya | Supports: Maya Ascii/Binary

def kiosk_open_scene(filepath):
    import maya.cmds as cmds
    
    cmds.file(filepath, open=True, f=True)