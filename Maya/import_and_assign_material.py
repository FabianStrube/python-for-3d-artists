# Import and assign material to selection | Supports: Maya Ascii/Binary
def import_and_assign_material(filepath):
    import maya.cmds as cmds

    # Get selected objects in the scene
    selected_objects = cmds.ls(selection=True)
    
    # Import the Maya binary file
    imported_nodes = cmds.file(filepath, i=True, type="mayaBinary", ignoreVersion=True, ra=True, mergeNamespacesOnClash=False, returnNewNodes=True)

    materials = cmds.ls(imported_nodes, materials=True)

    # Check if there are any materials found
    if not materials:
        cmds.warning("No materials found in the imported file.")
        return

    # If no objects are selected, assign the material to all objects in the scene
    if not selected_objects:
        selected_objects = cmds.ls(type="transform")

    # Assign the first found material to selected objects
    material_to_assign = materials[0]
    shading_group = cmds.listConnections(material_to_assign + '.outColor', type='shadingEngine')[0]

    # Filter out default shape nodes
    selected_objects = [obj for obj in selected_objects if cmds.nodeType(cmds.listRelatives(obj, shapes=True)[0]) != "defaultGeometry"]
    for obj in selected_objects:
        # Check if the object already has a material assigned
        if cmds.listRelatives(obj, shapes=True):
            cmds.sets(obj, edit=True, forceElement=shading_group)
        else:
            cmds.warning("Object {} has no shape node. Skipping material assignment.".format(obj))
