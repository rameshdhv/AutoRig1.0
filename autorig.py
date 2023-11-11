from imp import reload
import maya.cmds as cmds

import sys
pathname="F:/Scripts/armRIg"
if pathname not in sys.path:
    sys.path.append(pathname)
    
import rig_utils
reload(rig_utils)
import control_shape_library
reload(control_shape_library)

####################################################


prefixes=["_Skin_Jnt","_IK_Jnt","_FK_Jnt"]

LT_ArmGuides=cmds.ls("LT_Shoulder_Jnt","LT_Elbow_Jnt","LT_Wrist_Jnt")
RT_ArmGuides=cmds.ls("RT_Shoulder_Jnt","RT_Elbow_Jnt","RT_Wrist_Jnt")



for each in prefixes:
    cmds.select(cl=1)
    rig_utils.Arm_Joints_creator(each,LT_ArmGuides)
    cmds.select(cl=1)
    

for each in prefixes:
    cmds.select(cl=1)
    rig_utils.Arm_Joints_creator(each,RT_ArmGuides)
    cmds.select(cl=1)
    



  
######################################################


#####################################################


rig_utils.initialiseSetup()
########################
rig_utils.duplicatejoints("LT")
rig_utils.FKArmRigBuilder("LT")
rig_utils.IKArmRigBuilder("LT")
rig_utils.connectArmIKFK("LT")
rig_utils.stretchyIKArm("LT")
rig_utils.ArmHandRig("LT")


rig_utils.duplicatejoints("RT")
rig_utils.FKArmRigBuilder("RT")
rig_utils.IKArmRigBuilder("RT")
rig_utils.connectArmIKFK("RT")
rig_utils.stretchyIKArm("RT")
rig_utils.ArmHandRig("RT")

  
    
    


    

     


    
     



    