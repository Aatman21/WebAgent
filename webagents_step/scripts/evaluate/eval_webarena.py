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
import openai
import time
import sys
import random
import os
import glob, json

# Add the directory containing ‘webagents_step/src’ to the Python path
sys.path.append(os.path.abspath("./webagents-step/src"))

from webagents_step.utils.data_prep import *
from webagents_step.agents.prompt_agent import PromptAgent
from webagents_step.agents.step_agent import StepAgent
from webagents_step.prompts.webarena import flat_fewshot_template, step_fewshot_template
from webagents_step.environment.webarena import WebArenaEnvironmentWrapper

def run():
    parser = argparse.ArgumentParser(
        description="Only the config file argument should be passed"
    )
    parser.add_argument(
        "--config", type=str, required=True, help="yaml config file location"
    )
    args = parser.parse_args()
    with open(args.config, "r") as file:
        config = DotDict(yaml.safe_load(file))
    
    dstdir = f"{config.logdir}/{time.strftime('%Y%m%d-%H%M%S')}"
    os.makedirs(dstdir, exist_ok=True)
    shutil.copyfile(args.config, os.path.join(dstdir, args.config.split("/")[-1]))
    random.seed(42)
    
    config_file_list = []
    """folder_path should have the task that you want to run"""
    folder_path="./tasks/webarena"
    json_files = glob.glob(os.path.join(folder_path, "*.json"))
    config_file_list=json_files
    action_to_prompt_dict = {k: v for k, v in step_fewshot_template.__dict__.items() if isinstance(v, dict)}
    low_level_action_list = config.agent.low_level_action_list

    if config.agent.type == "step":
        agent_init = lambda: StepAgent(
        root_action = config.agent.root_action,
        action_to_prompt_dict = action_to_prompt_dict,
        low_level_action_list = low_level_action_list,
        max_actions=config.env.max_env_steps,
        verbose=config.verbose,
        logging=config.logging,
        debug=config.debug,
        model=config.agent.model_name,
        prompt_mode=config.agent.prompt_mode,
        )

    #####
    # Evaluate
    #####

    for config_file in config_file_list:
        print(config_file)
        env = WebArenaEnvironmentWrapper(config_file=config_file, 
                                        max_browser_rows=config.env.max_browser_rows, 
                                        max_steps=config.env.max_env_steps, 
                                        slow_mo=1, 
                                        observation_type="accessibility_tree", 
                                        current_viewport_only=False, 
                                        viewport_size={"width": 1920, "height": 1080}, 
                                        headless=True)
        
        agent = agent_init()
        objective = env.get_objective()
        status = agent.act(objective=objective, env=env)
        env.close()

        if config.logging:
            with open(config_file, "r") as f:
                task_config = json.load(f)
            log_file = os.path.join(dstdir, f"Re_eval_for_variance_Final_baseline_{task_config['task_id']}.json")
            log_data = {
                "task": config_file,
                "id": task_config['task_id'],
                "model": config.agent.model_name,
                "type": config.agent.type,
                "trajectory": agent.get_trajectory(),
            }
            summary_file = os.path.join(dstdir, "summary.csv")
            summary_data = {
                "task": config_file,
                "task_id": task_config['task_id'],
                "model": config.agent.model_name,
                "type": config.agent.type,
                "logfile": re.search(r"/([^/]+/[^/]+\.json)$", log_file).group(1),
            }
            summary_data.update(status)
            log_run(
                log_file=log_file,
                log_data=log_data,
                summary_file=summary_file,
                summary_data=summary_data,
            )

if __name__ == "__main__":
    run()
