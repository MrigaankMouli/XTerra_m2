
from __future__ import annotations

from typing import TYPE_CHECKING

import torch

from isaaclab.assets import Articulation, RigidObject
from isaaclab.managers import SceneEntityCfg
from isaaclab.sensors import ContactSensor

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv
    from isaaclab.managers.command_manager import CommandTerm

"""
MDP terminations.
"""

def low_progress(
    env: ManagerBasedRLEnv,
    min_displacement: float = 0.25,
    grace_period_s: float = 3.0,
    command_name: str = "base_velocity",
    min_command: float = 0.2,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
) -> torch.Tensor:
    """Terminate if the robot has barely moved despite receiving a locomotion command."""

    asset: Articulation = env.scene[asset_cfg.name]

    # Distance travelled from the spawn position of the current episode
    displacement = torch.linalg.norm(
        asset.data.root_pos_w[:, :2] - env.scene.env_origins[:, :2],
        dim=1,
    )

    # Ignore the first few seconds
    grace_steps = int(grace_period_s / env.step_dt)

    # Only terminate if we actually asked the robot to move
    command = env.command_manager.get_command(command_name)
    cmd_mag = torch.linalg.norm(command[:, :2], dim=1)

    return (
        (env.episode_length_buf > grace_steps)
        & (cmd_mag > min_command)
        & (displacement < min_displacement)
    )