#!./venv/bin/python3
"""
## Usage
### Forward 0.3m/s
python mevius_eval.py --cmd_x 0.3 --ckpt 200

### Forward 0.5m/s
python mevius_eval.py --cmd_x 0.5 --ckpt 200

### Forward 0.0m/s
python mevius_eval.py --cmd_x 0.0 --ckpt 200

### Backward 0.2m/s
python mevius_eval.py --cmd_x -0.2 --ckpt 200   

## Description:
This opensource project is originally prepared by Kento Kawaharazuka(JSK Robotics Lab, The University of Tokyo).
Michitoshi Tsubaki (@Michi-Tsubaki) extended to support Genesis World Simulator referring to Genesis RL examples for Go2 Locomotion (https://github.com/Genesis-Embodied-AI/Genesis/tree/main/examples/locomotion).
He also referred to https://qiita.com/tamashu/items/3591a76d61e97fb3e0dc. 

## Citation:
@inproceedings{kawaharazuka2024mevius,
  author={K. Kawaharazuka and S. Inoue and T. Suzuki and S. Yuzaki and S. Sawaguchi and K. Okada and M. Inaba},
  title={{MEVIUS: A Quadruped Robot Easily Constructed through E-Commerce with Sheet Metal Welding and Machining}},
  booktitle={Proceedings of the 2024 IEEE-RAS International Conference on Humanoid Robots},
  year=2024,
}

@misc{Genesis,
  author = {Genesis Authors},
  title = {Genesis: A Generative and Universal Physics Engine for Robotics and Beyond},
  month = {December},
  year = {2024},
  url = {https://github.com/Genesis-Embodied-AI/Genesis}
}
"""

import argparse
import os
import pickle
from importlib import metadata

import torch

try:
    try:
        if metadata.version("rsl-rl"):
            raise ImportError
    except metadata.PackageNotFoundError:
        if metadata.version("rsl-rl-lib") != "2.2.4":
            raise ImportError
except (metadata.PackageNotFoundError, ImportError) as e:
    raise ImportError("Please uninstall 'rsl_rl' and install 'rsl-rl-lib==2.2.4'.") from e
from rsl_rl.runners import OnPolicyRunner

import genesis as gs

from mevius_env import MeviusEnv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--exp_name", type=str, default="mevius-walking")
    parser.add_argument("--ckpt", type=int, default=999, help="Checkpoint to load")
    parser.add_argument("--cmd_x", type=float, default=0.3, help="Forward velocity command [m/s]")
    parser.add_argument("--cmd_y", type=float, default=0.0, help="Lateral velocity command [m/s]")
    parser.add_argument("--cmd_yaw", type=float, default=0.0, help="Yaw velocity command [rad/s]")
    args = parser.parse_args()

    gs.init()

    log_dir = f"logs/{args.exp_name}"
    env_cfg, obs_cfg, reward_cfg, command_cfg, train_cfg = pickle.load(open(f"logs/{args.exp_name}/cfgs.pkl", "rb"))
    reward_cfg["reward_scales"] = {}

    env = MeviusEnv(
        num_envs=1,
        env_cfg=env_cfg,
        obs_cfg=obs_cfg,
        reward_cfg=reward_cfg,
        command_cfg=command_cfg,
        show_viewer=True,
    )

    runner = OnPolicyRunner(env, train_cfg, log_dir, device=gs.device)
    # Commandline argument --ckpt specifies which checkpoint to load, default is 100
    resume_path = os.path.join(log_dir, f"model_{args.ckpt}.pt")
    runner.load(resume_path)
    policy = runner.get_inference_policy(device=gs.device)

    obs, _ = env.reset()
    
    manual_commands = torch.tensor([[args.cmd_x, args.cmd_y, args.cmd_yaw]], 
                                   device=gs.device, dtype=gs.tc_float)
    env.commands[:] = manual_commands
    
    print(f"Running with commands: x={args.cmd_x}, y={args.cmd_y}, yaw={args.cmd_yaw}")
    
    with torch.no_grad():
        step_count = 0
        while True:
            actions = policy(obs)
            obs, rews, dones, infos = env.step(actions)
            
            env.commands[:] = manual_commands
            
            step_count += 1
            if step_count % 100 == 0:
                print(f"Step {step_count}, Reward: {rews[0]:.3f}")


if __name__ == "__main__":
    main()
