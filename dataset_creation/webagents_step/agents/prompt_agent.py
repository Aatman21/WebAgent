from webagents_step.agents.agent import Agent
from typing import List
from webagents_step.utils.llm import fill_prompt_template, construct_llm_message_openai, call_openai_llm, parse_action_reason, calculate_cost_openai



class PromptAgent(Agent):
    
    def __init__(self, max_actions: int = 10, verbose: bool = False, logging: bool = False, 
                 debug: bool = False, prompt_template: str = None, model: str = "gpt-4-turbo", 
                 prompt_mode: str = "chat", previous_actions: List = None, previous_reasons: List = None, previous_responses: List = None, previous_action_descriptions: List = None):
        super().__init__(max_actions=max_actions, verbose=verbose, logging=logging, previous_actions=previous_actions, previous_reasons=previous_reasons, previous_responses=previous_responses)        
        self.debug = debug 
        self.prompt_template = prompt_template
        self.model = model
        self.prompt_mode = prompt_mode

    def previous_history(self):
        previous_history = []
        
        if len(self.previous_actions) == len(self.previous_responses) == len(self.previous_reasons):
            for action, response, action_description in zip(self.previous_actions, self.previous_responses, self.previous_action_descriptions):
                if response:
                    previous_history.append(f"Action Taken: {action_description}")
                else:
                    previous_history.append(f"Action Taken: {action_description}")
            previous_history = "\n".join(previous_history)
        else:
            if self.previous_actions is not None and self.previous_reasons is not None:
                previous_history = "\n".join(f"Action Taken: {action_description}" for action_description, reason in zip(self.previous_action_descriptions, self.previous_reasons) if action_description is not None)
            elif self.previous_actions is not None:
                previous_history = "\n".join(f"Action Taken: {action_description}" for action_description, reason in zip(self.previous_action_descriptions, self.previous_reasons) if action_description is not None)

        return PromptAgent.global_history
    
    def predict_action(self, objective, observation, url=None):
        prompt = fill_prompt_template(prompt_template=self.prompt_template, objective=objective, 
                                      observation=observation, url=url, 
                                      previous_history=Agent.global_history)
        messages = construct_llm_message_openai(prompt=prompt, prompt_mode=self.prompt_mode)
        # print(f"At prompt_agent.py: \n\n\n\n\n{messages}\n\n\n\n\n\n")
        model_response = call_openai_llm(messages=messages, model=self.model)
        # print(f"MODEL RESPONSE: {model_response}\n\n\n\n\n")
        action, reason, action_description = parse_action_reason(model_response)
                
        if self.logging:
            self.data_to_log['prompt'] = messages
        
        if self.verbose > 0:
            if self.verbose > 1:
                print(f"\n OBSERVATION: {observation}")
                print(f"\n RESPONSE: {model_response}")        
            print(f"\n OBJECTIVE: {objective}")
            print(f"\n URL: {url}")
            print(f"\n PREVIOUS HISTORY: {Agent.global_history}")
            print(f"\n REASON: {reason}")
            print(f"\n ACTION DESCRIPTION: {action_description}")
            print(f"\n ACTION: {action}")
        Agent.global_history+=f"Action taken at step {Agent.idx}: {action_description}\n"
        Agent.idx+=1
        if "stop" in action:
            Agent.global_history=""
            Agent.idx=1
        if self.debug:
            human_input = input()
            if human_input != "c":
                action = human_input
                reason = "None"

        self.update_history(action=action, reason=reason, action_description=action_description)
        return action, reason, action_description