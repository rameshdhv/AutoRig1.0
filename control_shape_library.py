




############################control shapes##############################
def pyramid_control(name,scl):
    
    import maya.cmds as cmds
    
    # Define the vertices (control points) of the cube
    vertices = [
    (0.353553, 0.5, -0.5),
    (0.353553, 0.5, 0.5),
    (0.353553, -0.5, 0.5),
    (0.353553, -0.5, -0.5),
    (0.353553, 0.5, -0.5),
    (-0.353553, 0, 0),
    (0.353553, 0.5, 0.5),
    (0.353553, -0.5, 0.5),
    (-0.353553, 0, 0),
    (0.353553, -0.5, -0.5),
    (0.353553, 0.5, -0.5),
    (-0.353553, 0, 0)

    ]
    
    # Create the pyramid curve
    pyramid_curve = cmds.curve(d=1, p=vertices, k=list(range(len(vertices))),n=name)
    cmds.setAttr(pyramid_curve+".overrideEnabled",1)
    cmds.setAttr(pyramid_curve+".overrideColor",21)
    cmds.scale(scl,scl,scl, pyramid_curve + ".cv[*]", relative=True)
def cube_control(name,scl):
    
    import maya.cmds as cmds
    
    # Define the vertices (control points) of the cube
    vertices = [
        (-0.5, 0.5, 0.5),
        (0.5, 0.5, 0.5),
        (0.5, 0.5, -0.5),
        (-0.5, 0.5, -0.5),
        (-0.5, 0.5, 0.5),
        (-0.5, -0.5, 0.5),
        (0.5, -0.5, 0.5),
        (0.5, -0.5, -0.5),
        (-0.5, -0.5, -0.5),
        (-0.5, -0.5, 0.5),
        (-0.5, 0.5, 0.5),
        (0.5, 0.5, 0.5),
        (0.5, -0.5, 0.5),
        (0.5, -0.5, -0.5),
        (0.5, 0.5, -0.5),
        (-0.5, 0.5, -0.5),
        (-0.5, -0.5, -0.5),
        (-0.5, -0.5, 0.5),
        (-0.5, 0.5, 0.5)
    ]
    
    # Create the cube curve
    cube_curve = cmds.curve(d=1, p=vertices, k=list(range(len(vertices))),n=name)
    cmds.setAttr(cube_curve+".overrideEnabled",1)
    cmds.setAttr(cube_curve+".overrideColor",17)
    cmds.scale(scl,scl,scl, cube_curve + ".cv[*]", relative=True)
    
    
def spear_control(name,scl):
    
    import maya.cmds as cmds
    
    # Define the vertices (control points) of the cube
    vertices = [
    (0, 2, 0),
    (0, 0, 2),
    (0, -2, 0),
    (0, 0, -2),
    (0, 2, 0),
    (0, -2, 0),
    (0, 0, 0),
    (0, 0, 2),
    (0, 0, -2),
    (2, 0, 0),
    (0, 0, 2),
    (-2, 0, 0),
    (0, 0, -2),
    (0, 0, 2),
    (0, 0, 0),
    (0, -2, 0),
    (2, 0, 0)
    ]
    
    # Create the pyramid curve
    spear_curve = cmds.curve(d=1, p=vertices, k=list(range(len(vertices))),n=name)
    cmds.setAttr(spear_curve+".overrideEnabled",1)
    cmds.setAttr(spear_curve+".overrideColor",25)
    cmds.scale(scl,scl,scl, spear_curve + ".cv[*]", relative=True)