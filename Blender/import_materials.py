# Imports all materials from a given .blend file

def import_materials(filepath):
    import bpy
    import os

    # Get the file extension
    file_extension = os.path.splitext(filepath)[1].lower()

    if file_extension == '.blend':
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            data_to.materials = data_from.materials
    else:
        print('Importing materials not supported for this file type')