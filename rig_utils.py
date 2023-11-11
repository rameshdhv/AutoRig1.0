
from imp import reload
import sys
pathname="F:/Scripts/armRIg"
if pathname not in sys.path:
    sys.path.append(pathname)
    

import control_shape_library
reload(control_shape_library)


##############################################################
def initialiseSetup():
    import maya.cmds as cmds
    global settings_GRP,IK_GRP,FK_GRP,Deformers_GRP,Dynamics_GRP,sknjnts_GRP,plfactor
    
    
    main_ctrl=cmds.circle(ch=0,n="Global_Ctrl",r=8)
    settings_GRP=cmds.group(n="Settings_Group",em=1,p=main_ctrl[0])
    IK_GRP=cmds.group(n="IK_Rig_Group",em=1,p=main_ctrl[0])
    FK_GRP=cmds.group(n="FK_Rig_Group",em=1,p=main_ctrl[0])
    Deformers_GRP=cmds.group(n="Deformers_Group",em=1,p=main_ctrl[0])
    Dynamics_GRP=cmds.group(n="Dynamics_Group",em=1,p=main_ctrl[0])
    sknjnts_GRP=cmds.group(n="Skin_Joint_Group",em=1,p=main_ctrl[0])
    
    #placement scale control size
    placement_ctrl= "Placement_Reference_Ctrl"
    plfactor=cmds.getAttr(placement_ctrl+".scaleX")
    print(plfactor)
    cmds.makeIdentity(placement_ctrl,apply=True, translate=True, rotate=True, scale=True)
####################################################################

def Arm_Joints_creator(name,setname):
    import maya.cmds as cmds
    for i in setname:
        jnt=cmds.joint(n=i.replace("_Jnt",name))
        
        cmds.matchTransform(jnt,i)
        cmds.makeIdentity(jnt, apply=True, t=1, r=1, s=1, n=0)
        
########################################################################################################
def duplicatejoints(prefix):
    import maya.cmds as cmds
    comp_jnt= prefix+"_Hand_Jnt"
    if cmds.objExists(comp_jnt):
        newjointset=cmds.listRelatives(comp_jnt,ad=True)
        newjointset.insert(0,comp_jnt)
        parentskinjntset=[]
        skinjntset=[]
        
        for i in newjointset:
            try:
                component_jnt=cmds.createNode("joint",n=i.replace("_Jnt","_Skin_Jnt"))
                
                cmds.matchTransform(component_jnt,i)
                cmds.makeIdentity(component_jnt, apply=True, t=1, r=1, s=1, n=0)
                #each object will be print in list when using list relatives command.so adding [0] will remove the object from list
                parentobj=cmds.listRelatives(i,p=True)[0]
                parentskinjnt=parentobj.replace("_Jnt","_Skin_Jnt")
                parentskinjntset.append(parentskinjnt)
                skinjnt=i.replace("_Jnt","_Skin_Jnt")
                skinjntset.append(skinjnt)
                
                
            except:
                pass         
                    
                
                
    
        for each,each2 in zip(skinjntset,parentskinjntset):
            cmds.parent(each,each2)
    else:
        print("object not found....skipping component")        
###################################################################################################        
def FKArmRigBuilder(prefix):
    global fkrig_grp
    import maya.cmds as cmds
    ctlset=[]
    ctl_grpset=[]
    setname=[prefix+"_Shoulder_FK_Jnt",prefix+"_Elbow_FK_Jnt",prefix+"_Wrist_FK_Jnt"]
    for i in setname: 
    
    
        ctl=cmds.circle(ch=0,nr=(90,0,0),n=i.replace("_Jnt","_Ctrl"))[0]
        
        
        cmds.setAttr(ctl+".overrideEnabled",1)
        cmds.setAttr(ctl+".overrideColor",6)
        ctl_grp=cmds.group(ctl,n=i.replace("_Jnt","_Ctrl_Group"))
        
        cmds.matchTransform(ctl_grp,i)
        cmds.parentConstraint(ctl,i,mo=1)
        cmds.select(cl=1)
        ctlset.append(ctl)
        ctl_grpset.append(ctl_grp)
        
    # this parents the FK control groups in hierarchy    
    num=len(ctl_grpset)-1
    
        
    for sObj in range(len(ctl_grpset)):
        cmds.parent(ctl_grpset[num],ctlset[num-1])
        num-=1
        if num==0:
            break
    fkrig_grp=cmds.group(ctl_grpset[0],setname[0],n=prefix+"_Arm_FK_Rig_Group")
    
    
    
    
    
    
#####################################################################################


def IKArmRigBuilder(prefix):
    import maya.cmds as cmds
    global ikrig_grp
    #create Shoulder,polvector and Arm IK Controls
    #shoulder_ctrl = cmds.circle(nr=(90,0,0),n=prefix+"_Shoulder_Ctrl",ch=0)
    #cmds.setAttr(shoulder_ctrl[0]+".overrideEnabled",1)
    #cmds.setAttr(shoulder_ctrl[0]+".overrideColor",6)
    #shoulder_ctrl_grp = cmds.group(shoulder_ctrl,n=prefix+"_Shoulder_Ctrl_Grp")
    global ikrig_grp
    control_shape_library.cube_control(prefix+"_Arm_IK_Ctrl",plfactor)
    Arm_IK_ctrl=cmds.ls(prefix+"_Arm_IK_Ctrl")
    Arm_IK_ctrl_grp = cmds.group(Arm_IK_ctrl[0],n=prefix+"_Arm_IK_Ctrl_Grp")
    
    control_shape_library.pyramid_control(prefix+"_Arm_PV_Ctrl",plfactor)
    Arm_PV_ctrl=cmds.ls(prefix+"_Arm_PV_Ctrl")
    Arm_PV_ctrl_grp = cmds.group(Arm_PV_ctrl[0],n=prefix+"_Arm_PV_Ctrl_Grp")
    
    #cmds.matchTransform(shoulder_ctrl_grp,prefix+"_Shoulder_IK_Jnt")
    cmds.matchTransform(Arm_PV_ctrl_grp,prefix+"_Elbow_IK_Jnt")
    cmds.matchTransform(Arm_IK_ctrl_grp,prefix+"_Wrist_IK_Jnt")
    
    #ik rig
    
    IKhandle = cmds.ikHandle(sj=prefix+"_Shoulder_IK_Jnt",ee=prefix+"_Wrist_IK_Jnt",sol="ikRPsolver",n=prefix+"_Arm_IK_Handle",p=2)
    #polevector constraint
    cmds.poleVectorConstraint(prefix+"_Arm_PV_Ctrl",IKhandle[0])
    #parent ikhandle under ik control
    cmds.parent(IKhandle[0],prefix+"_Arm_IK_Ctrl")
    ikrig_grp=cmds.group(Arm_IK_ctrl_grp,Arm_PV_ctrl_grp,prefix+"_Shoulder_IK_Jnt",n=prefix+"_Arm_IK_Rig Group")
    
    
    
########################################################################################################################################
def connectArmIKFK(prefix):
    import maya.cmds as cmds
    global Arm_settings_ctrl
    control_shape_library.spear_control(prefix+"_Arm_Settings_Ctrl",plfactor)
    Arm_settings_ctrl=cmds.ls(prefix+"_Arm_Settings_Ctrl")
    Arm_settings_ctrl_grp = cmds.group(Arm_settings_ctrl[0],n=prefix+"_Arm_Settings_Ctrl_Group")
    
    for i in [".sx",".sy",".sz"]:
        cmds.setAttr(Arm_settings_ctrl_grp+i,0.5)
    
    #create an IKFK attribute
    
    cmds.addAttr(Arm_settings_ctrl[0],ln="IKFK",min=0,max=1,dv=0,k=1)
    cmds.matchTransform(Arm_settings_ctrl_grp,prefix+"_Wrist_Skin_Jnt")
    cmds.pointConstraint(prefix+"_Wrist_Skin_Jnt",Arm_settings_ctrl_grp,mo=1)
    
    
    #Connect IK,FK to skin joints
    
    Shoulder_const=cmds.parentConstraint(prefix+"_Shoulder_IK_Jnt",prefix+"_Shoulder_FK_Jnt",prefix+"_Shoulder_Skin_Jnt",mo=1)
    Elbow_const=cmds.parentConstraint(prefix+"_Elbow_IK_Jnt",prefix+"_Elbow_FK_Jnt",prefix+"_Elbow_Skin_Jnt",mo=1)
    Wrist_const=cmds.parentConstraint(prefix+"_Wrist_IK_Jnt",prefix+"_Wrist_FK_Jnt",prefix+"_Wrist_Skin_Jnt",mo=1)
    
    
    
    cmds.setAttr(Shoulder_const[0]+".interpType",2)
    cmds.setAttr(Elbow_const[0]+".interpType",2)
    cmds.setAttr(Wrist_const[0]+".interpType",2)    
    
    revnode=cmds.createNode("reverse",n=prefix+"Arm_REV")
    
    cmds.connectAttr(Arm_settings_ctrl[0]+".IKFK",Shoulder_const[0]+"."+prefix+"_Shoulder_FK_JntW1")
    cmds.connectAttr(Arm_settings_ctrl[0]+".IKFK",Elbow_const[0]+"."+prefix+"_Elbow_FK_JntW1")
    cmds.connectAttr(Arm_settings_ctrl[0]+".IKFK",Wrist_const[0]+"."+prefix+"_Wrist_FK_JntW1")
    
    cmds.connectAttr(Arm_settings_ctrl[0]+".IKFK",revnode+".inputX")
    
    cmds.connectAttr(revnode+".outputX",Shoulder_const[0]+"."+prefix+"_Shoulder_IK_JntW0")
    cmds.connectAttr(revnode+".outputX",Elbow_const[0]+"."+prefix+"_Elbow_IK_JntW0")
    cmds.connectAttr(revnode+".outputX",Wrist_const[0]+"."+prefix+"_Wrist_IK_JntW0")
    
    #connect ik fk ctrl vis to IKFKswitch
    cmds.connectAttr(Arm_settings_ctrl[0]+".IKFK",fkrig_grp+".visibility")
    cmds.connectAttr(revnode+".outputX",ikrig_grp+".visibility")
    
   
    cmds.parent(Arm_settings_ctrl_grp,settings_GRP)
    cmds.parent(ikrig_grp,IK_GRP)
    cmds.parent(fkrig_grp,FK_GRP)
    cmds.parent(prefix+"_Shoulder_Skin_Jnt",sknjnts_GRP)
    #cmds.parent(distance_node,Deformers_GRP)
    
    
    
def stretchyIKArm(prefix):
    import maya.cmds as cmds
    global dist_loc
    global distance_node
    
    #create distance dimension node
    shoulderpos=cmds.xform(prefix+"_Shoulder_IK_Jnt",q=1,ws=1,t=1)
    wristpos=cmds.xform(prefix+"_Wrist_IK_Jnt",q=1,ws=1,t=1)
    distance_node=cmds.distanceDimension(sp=shoulderpos,ep=wristpos)
    print(distance_node) 
    dist_loc=cmds.listConnections(distance_node,t="locator")
    
    
    
    
    #cmds.parentConstraint(prefix+"_Shoulder_IK_Jnt",loc01[0],mo=0)
    
    cmds.parent(dist_loc[1],prefix+"_Arm_IK_Ctrl")
    
    
    
    
    
   
    
    
   
    
    #cmds.connectAttr(dbw_upper+".distance",sumoflength+".input1D[0]",force=True)
   
   
    
    stretchMD=cmds.createNode("multiplyDivide",n=prefix+"_Arm_Stretch_MD")
    cmds.setAttr(stretchMD+".operation",2)
    #cmds.connectAttr(distance_node+".distance",stretchMD+".input1X",force=True)
    #the above line is replaced by scale compensate MD node distance value
    
    
    
    #create condition node for stretch logic
    
    armcondition=cmds.createNode("condition",n=prefix+"_Arm_Stretch_Condition")
    cmds.setAttr(armcondition+".operation",3)
    cmds.connectAttr(distance_node+".distance",armcondition+".firstTerm",force=True)
    
    
    cmds.connectAttr(stretchMD+".outputX",armcondition+".colorIfTrueR")
    cmds.setAttr(armcondition+".colorIfFalseR",1)
    
    
    #getAttr of elbow and wrist
    upperarm_dv=cmds.getAttr(prefix+"_Elbow_IK_Jnt"+".tx")
    lowerarm_dv=cmds.getAttr(prefix+"_Wrist_IK_Jnt"+".tx")
    
    #create a stretchy switch and blendcolors node
    
    cmds.addAttr(Arm_settings_ctrl[0],ln="Stretchy",min=0,max=1,k=1)
    cmds.addAttr(Arm_settings_ctrl[0],ln="UpperArm",k=1,dv=upperarm_dv)
    cmds.setAttr(Arm_settings_ctrl[0]+".UpperArm",l=1)
    cmds.addAttr(Arm_settings_ctrl[0],ln="LowerArm",k=1,dv=lowerarm_dv)
    cmds.setAttr(Arm_settings_ctrl[0]+".LowerArm",l=1)
    
    
    arm_BC=cmds.createNode("blendColors",n=prefix+"_Arm_Stretch_BC")
    
    #create Connections for BLend colors
    
    cmds.connectAttr(armcondition+".outColorR",arm_BC+".color1R")
    cmds.setAttr(arm_BC+".color1G",1)
    cmds.setAttr(arm_BC+".color1B",1)
    cmds.setAttr(arm_BC+".color2R",1)
    cmds.setAttr(arm_BC+".color2G",1)
    cmds.setAttr(arm_BC+".color2B",1)
    cmds.connectAttr(Arm_settings_ctrl[0]+".Stretchy",arm_BC+".blender")
    
    
    
    #create multiply Divide nodes for upper Arm and Lower Arm
    upperArmMD=cmds.createNode("multiplyDivide",n=prefix+"_UpperArm_MD")
    lowerArmMD=cmds.createNode("multiplyDivide",n=prefix+"_LowerArm_MD")
    cmds.setAttr(upperArmMD+".operation",1)
    cmds.setAttr(lowerArmMD+".operation",1)
    
    
    cmds.connectAttr(arm_BC+".outputR",upperArmMD+".input1X")
    
    
    cmds.connectAttr(arm_BC+".outputR",lowerArmMD+".input1X")
    cmds.connectAttr(Arm_settings_ctrl[0]+".UpperArm",upperArmMD+".input2X")
    cmds.connectAttr(Arm_settings_ctrl[0]+".LowerArm",lowerArmMD+".input2X")
    
        
    cmds.connectAttr(upperArmMD+".outputX",prefix+"_Elbow_IK_Jnt"+".translateX")
    cmds.connectAttr(lowerArmMD+".outputX",prefix+"_Wrist_IK_Jnt"+".translateX")
    
    #scale update/compensation
    armcompMD=cmds.createNode("multiplyDivide",n=prefix+"_Arm_Scale_Comp_MD")
    cmds.connectAttr(distance_node+".distance",armcompMD+".input1X")
    cmds.connectAttr("Global_Ctrl.scaleX",armcompMD+".input2X")
    cmds.setAttr(armcompMD+".operation",2)
    cmds.connectAttr(armcompMD+".outputX",stretchMD+".input1X",force=True)
    
    #updating after scale comp
    defarmlength=cmds.getAttr(stretchMD+".input1X")
    cmds.setAttr(stretchMD+".input2X",defarmlength)
    cmds.setAttr(armcondition+".secondTerm",defarmlength)
    
def ArmHandRig(prefix):
    
    #this block creates FK controls and parent them in hierarchy
    import maya.cmds as cmds
    
    comp_name=prefix+"_Hand_Jnt"
    if cmds.objExists(comp_name):
        setname= cmds.listRelatives(comp_name,ad=True)
        
        setname.insert(0,prefix+"_Hand_Jnt")    
        
        
        
        ctlset=[]
        ctl_grpset=[]
        
        
        for i in setname: 
            try:
        
                ctl=cmds.circle(ch=0,nr=(90,0,0),n=i.replace("_Jnt","_Ctrl"))[0]
                
                
                cmds.setAttr(ctl+".overrideEnabled",1)
                cmds.setAttr(ctl+".overrideColor",6)
                ctl_grp=cmds.group(ctl,n=i.replace("_Jnt","_Ctrl_Group"))
                
                cmds.matchTransform(ctl_grp,i)
                
                cmds.select(cl=1)
                ctlset.append(ctl)
                ctl_grpset.append(ctl_grp)
                cmds.parentConstraint(ctl,i.replace("_Jnt","_Skin_Jnt"),mo=1)
                cmds.scaleConstraint(ctl,i.replace("_Jnt","_Skin_Jnt"),mo=1)
                
            except:
                pass  
            
            #parent according to hierarchy
        newsetname=setname[1:]    
        for i in newsetname:
            try:
                parobj = cmds.listRelatives(i, parent=True)[0]
                if parobj:
                    
                    
                      # Access the first element of the list
                    ctrl_name = parobj.replace("_Jnt", "_Ctrl")
                    ctrl_group_name = i.replace("_Jnt", "_Ctrl_Group")
                    
                        # Check if the control and control group exist before parenting
                    if cmds.objExists(ctrl_name) and cmds.objExists(ctrl_group_name):
                        cmds.parent(ctrl_group_name,ctrl_name)
                    else:
                        print("Control or control group does not exist for i")
                else:
                    print("it has no parent.")
            
            except:
                pass
    
            
            
        handpc=cmds.parentConstraint(prefix+"_Wrist_Skin_Jnt",prefix+"_Hand_Ctrl_Group")
        handsc=cmds.scaleConstraint(prefix+"_Wrist_Skin_Jnt",prefix+"_Hand_Ctrl_Group")
        cmds.parent(prefix+"_Hand_Ctrl_Group",FK_GRP)    
    else:
        print("component object not found .....skipping")
#############################################################################################################    
    
    
    
    
    
    
    