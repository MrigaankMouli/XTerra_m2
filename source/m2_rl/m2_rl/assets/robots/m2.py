# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import os

import isaaclab.sim as sim_utils
from isaaclab.actuators import ActuatorNetMLPCfg, DCMotorCfg, ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg
from isaaclab.utils import configclass

M2_USD_PATH = os.path.join(os.path.dirname(__file__), "usd", "m2_metal_description.usd")


@configclass
class M2ArticulationCfg(ArticulationCfg):
    """Configuration for M2 articulations."""

    joint_sdk_names: list[str] = None

    soft_joint_pos_limit_factor = 0.9


#Rigid body properties were taken from the M2_legged_rl repository
#Articulation Properties were kept the same as unitree_go2
@configclass
class M2UsdFileCfg(sim_utils.UsdFileCfg):
    activate_contact_sensors = True
    rigid_props = sim_utils.RigidBodyPropertiesCfg(
        disable_gravity=False,
        retain_accelerations=False,
        linear_damping=0.1,
        angular_damping=0.0,
        max_linear_velocity=1000.0,
        max_angular_velocity=1000.0,
        max_depenetration_velocity=1.0,
    )
    articulation_props = sim_utils.ArticulationRootPropertiesCfg(
        enabled_self_collisions=True, solver_position_iteration_count=8, solver_velocity_iteration_count=4
    )

M2_CFG = M2ArticulationCfg(
    # spawn=M2UrdfFileCfg(
    #     asset_path=f"{UNITREE_ROS_DIR}/robots/go2_description/urdf/go2_description.urdf",
    # ),
    spawn=M2UsdFileCfg(
        usd_path=M2_USD_PATH,
    ),
    #Joint Positions and Default Standing Positionswere taken from the M2_legged_rl repository
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.27),
        joint_pos={
            ".*_hip_joint": 0.0,
            ".*_thigh_joint": 0.9,
            "F[L,R]_calf_joint": -1.8,
            "R[L,R]_calf_joint": -1.8,
        },
        joint_vel={".*": 0.0},
    ),
    soft_joint_pos_limit_factor=0.9,
    actuators={
        "base_legs": DCMotorCfg(
            joint_names_expr=[".*_hip_joint", ".*_thigh_joint", ".*_calf_joint"],
            effort_limit=23.5,
            saturation_effort=23.5,
            velocity_limit=30.0,
            stiffness=20.0,
            damping=1.0,
            friction=1.0,
        ),
    },
    #Joint Names were taken from the M2_imu.usd file by inspecting the Stage in IsaacSim
        joint_sdk_names=[
        "RL_hip_joint", "RL_thigh_joint", "RL_calf_joint",
        "FL_hip_joint", "FL_thigh_joint", "FL_calf_joint",
        "RR_hip_joint", "RR_thigh_joint", "RR_calf_joint",
        "FR_hip_joint", "FR_thigh_joint", "FR_calf_joint",
    ],
)
