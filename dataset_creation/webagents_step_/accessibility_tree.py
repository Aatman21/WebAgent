import os
import pandas as pd
import time
import re
import argparse
import itertools
from tqdm import tqdm
import os
import sys
import argparse
from typing import List
import shutil
import time
import random
# from src.webagents_step.environment.webarena import WebArenaEnvironmentWrapper
# from src.webagents_step.utils.data_prep import *
from src.webagents_step.hello import func
# print(sys.path)

func()

# def run():
#     parser = argparse.ArgumentParser(
#         description="Only the config file argument should be passed"
#     )
#     parser.add_argument(
#         "--config", type=str, required=True, help="yaml config file location"
#     )
#     args = parser.parse_args()
#     with open(args.config, "r") as file:
#         config = DotDict(yaml.safe_load(file))
    
#     dstdir = f"{config.logdir}/{time.strftime('%Y%m%d-%H%M%S')}"
#     os.makedirs(dstdir, exist_ok=True)
#     shutil.copyfile(args.config, os.path.join(dstdir, args.config.split("/")[-1]))
#     random.seed(42)
    
#     config_file_list = []
#     task_ids = config.env.task_ids

#     for task_id in task_ids:
#         config_file_list.append(f"tasks/webarena/{task_id}.json")


#     for config_file in config_file_list:
#             env = WebArenaEnvironmentWrapper(config_file=config_file, 
#                                             max_browser_rows=config.env.max_browser_rows, 
#                                             max_steps=config.env.max_env_steps, 
#                                             slow_mo=1, 
#                                             observation_type="accessibility_tree", 
#                                             current_viewport_only=True, 
#                                             viewport_size={"width": 1920, "height": 1080}, 
#                                             headless=config.env.headless)
#             objective = env.get_objective()
#             env.close()

#             # if config.logging:
#             #     with open(config_file, "r") as f:
#             #         task_config = json.load(f)
#             #     log_file = os.path.join(dstdir, f"{task_config['task_id']}.json")
#             #     log_data = {
#             #         "task": config_file,
#             #         "id": task_config['task_id'],
#             #     }
            
# if __name__ == "__main__":
#     run()
