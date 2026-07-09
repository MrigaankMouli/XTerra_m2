# Reinforcement Learning codebase for M2 Swan

Isaac Lab workspace for the XTerra M2 Swan Quadruped locomotion training and evaluation.

This repository is a **M2 port** of the original Unitree RL Lab codebase.
The original authors and upstream project are:

- **Unitree Robotics**
- original project: `unitree_rl_lab`

This repo adapts that structure and training flow for the M2 robot and its
locomotion tasks.


<!-- ## Multi-Terrain Demonstration

<table>
<tr>
<td align="center" width="50%">
<img src="assets/videos/flat.gif" width="100%"></video>
<br><br>
<b>Flat Terrain Omnidirectional Locomotion</b>
</td>

<td align="center" width="50%">
<img src="assets/videos/rough.gif" width="100%"></video>
<br><br>
<b>Rough Terrain Omnidirectional Locomotion</b>
</td>
</tr>

<tr>
<td align="center" width="50%">
<img src="assets/videos/slopes.gif" width="100%"></video>
<br><br>
<b>Sloped Terrain Omnidirectional Locomotion</b>
</td>

<td align="center" width="50%">
<img src="assets/videos/stairs.gif" width="100%"></video>
<br><br>
<b>Stair Climbing Demonstration</b>
</td>
</tr>
</table> -->

## Installation

Prerequisite: install Isaac Lab separately and use its Python environment.

If the M2 USD path changes, update it in:

- `source/m2_rl/m2_rl/assets/robots/M2.py`

## Directory Structure

```text
.
├── scripts/
│   └── rsl_rl/
│       ├── train.py
│       └── play.py
├── source/
│   └── m2_rl/
│       └── m2_rl/
│           ├── assets/
│           │   └── robots/
│           │       └── M2.py
│           └── tasks/
│               └── locomotion/
│                   └── robots/
│                       ├── M2/
│                       ├── M2-rough/
|                       ├── M2-stairs/
|                       ├── M2-blocks/
|                       └── M2-eval/
├── logs/
├── docs/
└── m2_rl.sh
```

Key pieces:

- `source/m2_rl/m2_rl/assets/robots/M2.py`: M2 USD and actuator configuration
- `source/m2_rl/m2_rl/tasks/locomotion/mdp/rewards.py`: Reward Functions definition
- `source/m2_rl/m2_rl/utils/ood_merics.py`: OOD Metrics definition
- `source/m2_rl/m2_rl/tasks/locomotion/robots/[TASK-NAME]/velocity_env_cfg.py` : Task specific config file
- `scripts/rsl_rl/train.py`: RSL-RL training entrypoint
- `scripts/rsl_rl/play.py`: checkpoint visualization entrypoint
- `scripts/rsl_rl/teleop.py` : teleoperation with trained checkpoint entrypoint
- `m2_rl.sh`: wrapper for install, list, train, and play

## Training

Train a specific task:

```bash
./m2_rl.sh -t --task [TASK-NAME]
```

Registered Task are given below:

- M2-Velocity
- M2-Velocity-Rough
- M2-Velocity-Stairs
- M2-Velocity-Blocks

Warm-start training from a pre-trained checkpoint:

```bash
./m2_rl.sh -t \
  --task [TASK-NAME] \
  --resume \
  --checkpoint /abs/path/to/model.pt
```

## Playing

Play a checkpoint:

```bash
./m2_rl.sh -p \
  --task [TASK-NAME] \
  --checkpoint /abs/path/to/model.pt
```

Play a checkpoint with one environment in real time:

```bash
./m2_rl.sh -p \
  --task [TASK_NAME] \
  --checkpoint /abs/path/to/model.pt \
  --num_envs 1 \
  --real-time
```

## Teleoperation 

Teleoperate M2 with a checkpoint 

```bash
./m2_rl.sh --teleop \
  --task [TASK-NAME] \
  --checkpoint /abs/path/to/model.pt
```

## Documentation
 
| Document | Description |
|---|---|
| [Articulation Setup](docs/articulation.md) | Configuring M2 as an Isaac Lab articulation |
| [Task Setup](docs/task_setup.md) | Flat and rough terrain task registration and MDP design |
| [Policy & Training](docs/policy.md) | PPO architecture and hyperparameter reference |
| [Reward Functions](docs/rewards.md) | Reward terms, tuning rationale, and formulas |
| [OOD Findings](docs/OOD_findings.md) | OOD Metrics and Visual Comparisons between M2 baseline and Go2 baseline|
