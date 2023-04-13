import os
from collections import OrderedDict
from typing import *

import torch

from modules.models import MODELS_DIR


def write_config(state_dict: Dict[str, Any], cfg: Dict[str, Any]):
    state_dict["config"] = [x for x in cfg.values()]
    state_dict["params"] = cfg


def save(ckpt: Dict[str, torch.Tensor], sr: int, if_f0: int, name: str, epoch: int):
    state_dict = OrderedDict()
    state_dict["weight"] = {}
    for key in ckpt.keys():
        if "enc_q" in key:
            continue
        state_dict["weight"][key] = ckpt[key].half()
    if sr == "40k":
        write_config(
            state_dict,
            {
                "spec_channels": 1025,
                "segment_size": 32,
                "inter_channels": 192,
                "hidden_channels": 192,
                "filter_channels": 768,
                "n_heads": 2,
                "n_layers": 6,
                "kernel_size": 3,
                "p_dropout": 0,
                "resblock": "1",
                "resblock_kernel_sizes": [3, 7, 11],
                "resblock_dilation_sizes": [[1, 3, 5], [1, 3, 5], [1, 3, 5]],
                "upsample_rates": [10, 10, 2, 2],
                "upsample_initial_channel": 512,
                "upsample_kernel_sizes": [16, 16, 4, 4],
                "spk_embed_dim": 109,
                "gin_channels": 256,
                "sr": 40000,
            },
        )
    elif sr == "48k":
        write_config(
            state_dict,
            {
                "spec_channels": 1025,
                "segment_size": 32,
                "inter_channels": 192,
                "hidden_channels": 192,
                "filter_channels": 768,
                "n_heads": 2,
                "n_layers": 6,
                "kernel_size": 3,
                "p_dropout": 0,
                "resblock": "1",
                "resblock_kernel_sizes": [3, 7, 11],
                "resblock_dilation_sizes": [[1, 3, 5], [1, 3, 5], [1, 3, 5]],
                "upsample_rates": [10, 6, 2, 2, 2],
                "upsample_initial_channel": 512,
                "upsample_kernel_sizes": [16, 16, 4, 4, 4],
                "spk_embed_dim": 109,
                "gin_channels": 256,
                "sr": 48000,
            },
        )
    elif sr == "32k":
        write_config(
            state_dict,
            {
                "spec_channels": 513,
                "segment_size": 32,
                "inter_channels": 192,
                "hidden_channels": 192,
                "filter_channels": 768,
                "n_heads": 2,
                "n_layers": 6,
                "kernel_size": 3,
                "p_dropout": 0,
                "resblock": "1",
                "resblock_kernel_sizes": [3, 7, 11],
                "resblock_dilation_sizes": [[1, 3, 5], [1, 3, 5], [1, 3, 5]],
                "upsample_rates": [10, 4, 2, 2, 2],
                "upsample_initial_channel": 512,
                "upsample_kernel_sizes": [16, 16, 4, 4, 4],
                "spk_embed_dim": 109,
                "gin_channels": 256,
                "sr": 32000,
            },
        )
    state_dict["info"] = f"{epoch}epoch"
    state_dict["sr"] = sr
    state_dict["f0"] = if_f0
    torch.save(state_dict, os.path.join(MODELS_DIR, "checkpoints", f"{name}.pth"))