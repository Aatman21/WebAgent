from typing import List

import sys
import os
# Add the directory containing ‘webagents_step’ to the Python path
sys.path.append(os.path.abspath("/Users/aatmanj/Desktop/Enriched_Tree/webagents-step"))
from helper import modify_observation

class Agent:
    global_history = ""
    idx=1
    def __init__(
        self,
        max_actions,
        verbose=0,
        logging=False,
        previous_actions: List = None,
        previous_reasons: List = None,
        previous_responses: List = None,
        previous_action_descriptions: List = None
    ):
        self.previous_actions = [] if previous_actions is None else previous_actions 
        self.previous_reasons = [] if previous_reasons is None else previous_reasons
        self.previous_responses = [] if previous_responses is None else previous_responses
        self.previous_action_descriptions = [] if previous_action_descriptions is None else previous_action_descriptions
        self.max_actions = max_actions
        self.verbose = verbose
        self.logging = logging
        self.trajectory = []
        self.data_to_log = {}

    def reset(self):
        self.previous_actions = []
        self.previous_reasons = []
        self.previous_responses = []
        self.previous_action_descriptions = []
        self.trajectory = []
        self.data_to_log = {}

    def get_trajectory(self):
        return self.trajectory
    
    def update_history(self, action, reason, action_description):
        if action:
            self.previous_actions += [action]
        if reason:
            self.previous_reasons += [reason]    
        if action_description:
            self.previous_action_descriptions += [action_description]

    def predict_action(self, objective, observation, url=None):
        pass

    def receive_response(self, response):
        self.previous_responses += [response]

    def act(self, objective, env):
        while not env.done():
            observation = env.observation()
            """Commenting the next line out will result in unenriched/baseline model to run"""
            observation=modify_observation(observation)
            action, reason, action_description = self.predict_action(
                objective=objective, observation=observation, url=env.get_url()
            )
            # print(f"Inside Agent.py: Action Description : {action_description}")
            # print(f"Inside Agent.py: Action: ")
            status = env.step(action)

            if self.logging:
                self.log_step(
                    objective=objective,
                    url=env.get_url(),
                    observation=observation,
                    action=action,
                    reason=reason,
                    action_description=action_description,
                    status=status,
                )

            if len(self.previous_actions) >= self.max_actions:
                print(f"Agent exceeded max actions: {self.max_actions}")
                break

        return status

    async def async_act(self, objective, env):
        while not env.done():
            observation = await env.observation()
            action, reason, action_description = self.predict_action(
                objective=objective, observation=observation, url=env.get_url()
            )
            status = await env.step(action)

            if self.logging:
                self.log_step(
                    objective=objective,
                    url=env.get_url(),
                    observation=observation,
                    action=action,
                    reason=reason,
                    action_description=action_description,
                    status=status,
                )

            if len(self.previous_actions) >= self.max_actions:
                print(f"Agent exceeded max actions: {self.max_actions}")
                break

        return status

    def log_step(self, objective, url, observation, action, reason, action_description, status):
        self.data_to_log['objective'] = objective
        self.data_to_log['url'] = url
        self.data_to_log['observation'] = observation
        self.data_to_log['previous_actions'] = self.previous_actions[:-1]
        self.data_to_log['previous_responses'] = self.previous_responses[:-1]
        self.data_to_log['previous_reasons'] = self.previous_reasons[:-1]
        self.data_to_log['previous_action_descriptions'] = self.previous_action_descriptions[:-1]
        self.data_to_log['action'] = action
        self.data_to_log['reason'] = reason
        self.data_to_log['action_description'] = action_description
        for (k, v) in status.items():
            self.data_to_log[k] = v
        self.trajectory.append(self.data_to_log)
        self.data_to_log = {}
