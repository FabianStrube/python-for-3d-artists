# Imports assets into maya | Supports: Ascii/Binary/OBJ/FBX/Alembic

def import_asset(filepath):
    import maya.cmds as cmds
    import os

    extension = os.path.splitext(filepath)[1].lower()

    # Dictionary mapping file extensions to corresponding import types
    maya_import_types = {
        "ma": "MayaAscii",
        "mb": "MayaBinary",
        "obj": "OBJ",
        "fbx": "FBX",
        "abc": "Alembic",
        # Add more file extensions and import types as needed
    }

    if extension in maya_import_types:
        cmds.file(filepath, i=True, type=maya_import_types[extension], ignoreVersion=True, ra=True, mergeNamespacesOnClash=False, namespace=":", options="v=0;", pr=True)
    else:
        cmds.warning(f'Unknown import asset format: {extension}')