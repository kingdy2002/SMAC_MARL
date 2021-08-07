import numpy as np
import os
from collections import abc
from os.path import dirname, abspath
from copy import deepcopy
import sys
import torch as th
from utils.logging import get_logger
import yaml
import random
from run import run


def _get_config(params, arg_name, subfolder):
    config_name = None
    for _i, _v in enumerate(params):
        if _v.split("=")[0] == arg_name:
            config_name = _v.split("=")[1]
            del params[_i]
            break

    if config_name is not None:
        with open(os.path.join(os.path.dirname(__file__), "config", subfolder, "{}.yaml".format(config_name)), "r") as f:
            try:
                config_dict = yaml.load(f)
            except yaml.YAMLError as exc:
                assert False, "{}.yaml error: {}".format(config_name, exc)
        return config_dict

def get_config(algorithm, minigame):
    config_dir = '{0}/{1}'
    config_dir2 = '{0}/{1}/{2}'

    with open(config_dir.format('config', "{}.yaml".format('default')), "r") as f:
        try:
            default_config = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            assert False, "default.yaml error: {}".format(exc)

    with open(config_dir2.format('config', 'envs', "{}.yaml".format('sc2_beta')), "r") as f:
        try:
            config_dict = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            assert False, "{}.yaml error: {}".format('sc2', exc)
        env_config = config_dict

    with open(config_dir2.format('config', 'algs', "{}.yaml".format(algorithm)), "r") as f:
        try:
            config_dict2 = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            assert False, "{}.yaml error: {}".format('sc2', exc)
        alg_config = config_dict2

    final_config_dict = recursive_dict_update(default_config, env_config)
    final_config_dict = recursive_dict_update(final_config_dict, alg_config)

    final_config_dict['env_args']['map_name'] = minigame

    return final_config_dict



def recursive_dict_update(d, u):
    for k, v in u.items():
        if isinstance(v, abc.Mapping):
            d[k] = recursive_dict_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def config_copy(config):
    if isinstance(config, dict):
        return {k: config_copy(v) for k, v in config.items()}
    elif isinstance(config, list):
        return [config_copy(v) for v in config]
    else:
        return deepcopy(config)


if __name__ == '__main__':
    logger = get_logger()
    algorithm = 'qmix'
    minigame = '2s3z'
    print(th.__version__)
    config = config_copy(get_config(algorithm,minigame))
    random_Seed = random.randrange(0, 16546)
    np.random.seed(random_Seed)
    th.manual_seed(random_Seed)
    config['env_args']['seed'] = random_Seed
    run(config, logger, minigame)