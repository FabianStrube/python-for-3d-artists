# References files into Maya 

def reference_asset(filepath):
    import maya.cmds as cmds

    # Prompt user to enter a namespace
    namespace = cmds.promptDialog(
        title='Namespace',
        message='Enter namespace for the reference:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel'
    )

    if namespace == 'OK':
        namespace = cmds.promptDialog(query=True, text=True)
        cmds.file(filepath, reference=True, namespace=namespace)