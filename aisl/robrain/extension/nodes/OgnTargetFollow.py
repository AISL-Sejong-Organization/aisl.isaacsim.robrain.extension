"""
This is the implementation of the OGN node defined in OgnIKFollowTarget.ogn
"""

# Array or tuple values are accessed as numpy arrays so you probably need this import
from typing import Optional
from pathlib import Path
from scipy.spatial.transform import Rotation as R

import os
import numpy as np

from omni.isaac.core_nodes import BaseResetNode
from omni.isaac.core.articulations import Articulation
from omni.isaac.manipulators import SingleManipulator
from omni.isaac.motion_generation import (
    ArticulationKinematicsSolver,
    LulaKinematicsSolver,
)
from omni.isaac.core.prims import XFormPrim
from omni.isaac.core.scenes import Scene
from omni.graph.core import Database

import carb

SCALE_FACTOR = 0.05

def quat_wxyz_to_rot_matrix(q: np.ndarray) -> np.ndarray:
    q_xyzw = np.array([q[1], q[2], q[3], q[0]])

    return R.from_quat(q_xyzw).as_matrix()


def get_translate_from_prim(
    translation_from_source: np.ndarray,
    source_prim,
    target_info: tuple[np.ndarray, np.ndarray],
) -> np.ndarray:

    robot_pos, robot_orient = source_prim.get_world_pose()

    cur_target_object_pos, current_target_object_ori = target_info

    R_robot = quat_wxyz_to_rot_matrix(robot_orient)
    T_robot2world = np.eye(4, dtype=float)
    T_robot2world[0:3, 0:3] = R_robot
    T_robot2world[0:3, 3] = robot_pos
    R_target = quat_wxyz_to_rot_matrix(current_target_object_ori)
    T_obj2world = np.eye(4, dtype=float)
    T_obj2world[0:3, 0:3] = R_target * SCALE_FACTOR
    T_obj2world[0:3, 3] = cur_target_object_pos

    T_robot2obj = np.linalg.inv(T_robot2world) @ T_obj2world

    target_pos = np.pad(translation_from_source, (0, 1), constant_values=1)
    target_cube_relative_coordinates = (target_pos @ np.transpose(T_robot2obj))[0:3]

    return target_cube_relative_coordinates

class KinematicsSolver(ArticulationKinematicsSolver):
    def __init__(
        self,
        robot_articulation: Articulation,
        robot_description_path: str,
        urdf_path: str,
        end_effector_frame_name: Optional[str] = None,
    ) -> None:
        self._kinematics = LulaKinematicsSolver(
            robot_description_path=robot_description_path,
            urdf_path=urdf_path,
        )
        end_effector_frame_name = "end_effector_link"
        ArticulationKinematicsSolver.__init__(
            self, robot_articulation, self._kinematics, end_effector_frame_name
        )


class OgnTargetFollowInit(BaseResetNode):
    def __init__(self):
        self.initialized = None
        self.robot_prim_path = None
        self.tcp_prim_path = None
        self.robot_name = None
        self.ee_name = None
        self.manipulator = None
        self.my_controller = None
        self.robot_description_path = None
        self.urdf_path = None
        super().__init__(initialize=False)

    def initialize_scene(self):
        self.scene = Scene()
        self.manipulator = SingleManipulator(
            prim_path=self.robot_prim_path,
            name=self.robot_name,
            end_effector_prim_name=self.ee_name,
        )
        self.scene.add(self.manipulator)
        self.manipulator.initialize()

        self.my_robot = self.scene.get_object(self.robot_name)
        self.my_controller = KinematicsSolver(
            robot_articulation=self.my_robot,
            robot_description_path=self.robot_description_path,
            urdf_path=self.urdf_path,
        )
        self.articulation_controller = self.my_robot.get_articulation_controller()
        self.initialized = True
        return

    def custom_reset(self):
        self.my_controller = None


class OgnTargetFollow:

    @staticmethod
    def internal_state():
        return OgnTargetFollowInit()

    @staticmethod
    def compute(db) -> bool:
        state = db.per_instance_state
        if not state.initialized:
            state.robot_prim_path = db.inputs.robot_prim_path
            state.target_prim_path = db.inputs.target_prim_path
            state.ee_name = "end_effector_link"
            state.robot_name = db.inputs.robot_prim_path.split("/")[-1]

            robot_cfg_path = Path(__file__).parent.parent / "robot" / state.robot_name
            state.robot_description_path = os.path.join(
                robot_cfg_path, state.robot_name + "_descriptor.yaml"
            )
            state.urdf_path = os.path.join(robot_cfg_path, state.robot_name + ".urdf")
            state.initialize_scene()
        robot_origin = XFormPrim(state.robot_prim_path)
        target_origin = XFormPrim(state.target_prim_path)

        pos, quaternion_orientation = target_origin.get_world_pose()
        current_target_obj_info = pos, quaternion_orientation

        target_cube_relative_coordinates = get_translate_from_prim(
            [0, 0, -3], robot_origin, current_target_obj_info
        )

        actions, succ = state.my_controller.compute_inverse_kinematics(
            target_position=np.array(target_cube_relative_coordinates),
            target_orientation=np.array(quaternion_orientation),
        )

        if succ:
            state.articulation_controller.apply_action(actions)
        else:
            carb.log_warn(
                f"IK did not converge to a solution for target {pos}. No action is being taken."
            )
        return True

    @staticmethod
    def release_instance(node, graph_instance_id):
        try:
            print("release_instance")
            state = Database.per_instance_internal_state(node)
        except Exception:
            state = None
            pass
        if state is not None:
            print("state is not None reset")
            state.reset()
