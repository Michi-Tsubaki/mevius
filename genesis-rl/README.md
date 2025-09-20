# Mevius - Genesis Reinforcement Learning
This opensource project is originally prepared by Kento Kawaharazuka(JSK Robotics Lab, The University of Tokyo).
Michitoshi Tsubaki (@Michi-Tsubaki) extended to support Genesis World Simulator referring to Genesis RL examples for Go2 Locomotion (https://github.com/Genesis-Embodied-AI/Genesis/tree/main/examples/locomotion).
He also referred to https://qiita.com/tamashu/items/3591a76d61e97fb3e0dc. 

## Setup
1. Create vistural-env
```
python3 -m venv venv
```
If python3-venv has not been installed, you can install just by running `sudo apt install python3-venv` in your terminal.

2. Install dependencies
```
source venv/bin/activate
pip install -r requirements.txt
```

## How to train ?
3. Run following command from this directory.
```
./mevius_train.py
```
You can designate parameters from `get_train_cfg()` and `get_cfg()` in `mevius_train.py`.


## How to evaluate ?
4. Run following command from this directory. Before your own training, the pretrained model will run.
```
# Forward 0.3m/s
./mevius_eval.py --cmd_x 0.3 --ckpt 200

# Forward 0.5m/s
./mevius_eval.py --cmd_x 0.5 --ckpt 200

# Forward 0.0m/s
./mevius_eval.py --cmd_x 0.0 --ckpt 200
```
You can choose`--ckpt n`. Available `n` is listed like ./logs/mevius-walking/model_{n}.pt.
You can abort training, but if you abort it, `n` is limited. Default n is 999, so in that case, designation of skpt is mandatory.

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
