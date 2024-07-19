import re
import time, json
import sys, time
import os
import json
import re


# Add the directory containing 'webarena' to the Python path
sys.path.append(os.path.abspath('./webarena'))

from browser_env import ScriptBrowserEnv, create_id_based_action
import random as random
from collections import deque

all_URL_deque = deque()
all_URL_set = set()
all_LINKS_data_set = set()
all_LINKS_set=set()
parent_child_dict = {}

count=0
def count_leading_tabs(s: str):
    count = 0
    for char in s:
        if char == "\t":
            count += 1
        else:
            return count
    return count

def strip_id(input_str):
    match = re.match(r"\[\d+\]\s*(.*)", input_str)
    if match:
        return match.group(1)
    return input_str

def list_idx_to_key(idx: int, content_: list):
    content=content_[0:idx+1]
    num_tabs_current=count_leading_tabs(content[idx])
    before_idx=idx-1
    while before_idx>=3:
        before_person=content[before_idx]
        num_tabs_before=count_leading_tabs(before_person)
        if num_tabs_current>num_tabs_before:
            return list_idx_to_key(before_idx, content)+"||--||"+strip_id(content[idx].strip())
        before_idx=before_idx-1
    return strip_id(content[idx].strip())

def linkList(tree: str, env):
    global all_LINKS_set
    tree_list = tree.strip().split('\n')
    links_list=[]
    for idx, row in enumerate(tree_list):
        tag_type = row.split()
        if len(tag_type)>1 and (tag_type[1] == 'link'):
            key = list_idx_to_key(idx, tree_list)
            if not (key in all_LINKS_set):
                all_LINKS_set.add(key)
                links_list.append(key)
    return links_list

def key_to_tag_bkd_id (key: str, tree: str)->(str):            
    tree_list = tree.strip().split('\n')[3:]
    key_list=key.strip().split('||--||')
    curr_itr = 0
    for row in tree_list:
        row_list = row.strip().split(' ')
        if len(row_list)>0 and strip_id(row.strip()) == key_list[curr_itr]:
            curr_itr = curr_itr + 1
            if curr_itr == len(key_list):
                return row_list[0]
    return '-1'


def key_to_env_state(key_list: list, tree: str, info: dict, key: str, env):
    global count
    tree_list = tree.strip().split('\n')[3:]
    curr_itr = 0
    iff = False
    action_id = "-1"
    for row in tree_list:
        row_list = row.strip().split(' ')
        if len(row_list)>1 and " ".join(row_list[1:]) == key_list[curr_itr].strip():
            iff = True
            curr_itr =curr_itr+1
            action_id = row_list[0]
            break
    
    if not iff:
        for row in tree_list:
            row_list = row.strip().split(' ')
            if len(row_list)>1 and (row_list[1] == 'link'):
                substring = (" ".join(row_list[2:])).strip()[:-1]
                superstring = (" ".join(key_list[curr_itr].strip().split(" ")[1:])).strip()
                if superstring.find(substring) == 0:
                    curr_itr = curr_itr + 1
                    iff = True
                    action_id = row_list[0]
                    break


    if iff :
        if len(row_list)>1 and (row_list[1] == 'link'):
            action = create_id_based_action("click "+action_id)
            obs, _, terminated, _, info = env.step(action)
            if curr_itr == len(key_list):
                if not (key in all_LINKS_data_set):
                    all_LINKS_data_set.add(key)
                    """Write in the output path in the following variable"""
                    dataFileName = './all_data_'+str(count)+'.json'
                    count=count+1
                    with open(dataFileName, 'w') as datafile:
                        json.dump({"key" : key, "before" : tree, "after" : obs['text']}, datafile)

                return obs['text'], info

            return key_to_env_state(key_list[curr_itr:], obs['text'], info, key, env)
        return key_to_env_state(key_list[curr_itr:], tree, info, key, env)
    return tree, info


def explore_url(url: str, env):
    global all_URL_deque
    global all_LINKS_data_set
    global count
    global all_URL_set
    global all_LINKS_set
    global parent_child_dict
    
    config_dict = {
    "storage_state": ".auth/shopping_state.json",
    "start_url": url,
    }

    temp_config_file = "./temp_config.json"
    with open(temp_config_file, 'w') as f:
        json.dump(config_dict, f)

    obs, info = env.reset(options={"config_file": temp_config_file})
    before_tree =obs['text']

    before_tree_links_list = linkList(before_tree, env)
    

    url_links=deque()
    url_links.extend(before_tree_links_list)

    while url_links:
        print('\t', url_links[0])

        link = url_links.popleft()

        obs, info = env.reset(options={"config_file": temp_config_file})
        newobs, newinfo = key_to_env_state(link.strip().split('||--||'), obs['text'], info, link, env)

        temp_url = str(newinfo['page']).split('\',')[0][18:]
        url_after_action = temp_url

        if not (url_after_action in all_URL_set):
            all_URL_set.add(url_after_action)
            all_URL_deque.append(url_after_action)
        else:
            new_tree = newobs
            new_tree_links_list = linkList(new_tree,env)
 
            parent_child_dict[link] = new_tree_links_list
            file = open("parent_child_dict_temporary.json", 'w')
            json.dump(parent_child_dict, file, indent = 4)
            file.close()
            url_links.extend(new_tree_links_list)

        if not (link in all_LINKS_data_set):
            all_LINKS_data_set.add(link)

            completed_links_file = open("completed_links.txt", 'a')
            completed_links_file.write(link)
            completed_links_file.close()

            dataFileName = './all_data_'+str(count)+'.json'
            count=count+1
            with open(dataFileName, 'w') as datafile:
                json.dump({"key" : link, "before" : before_tree, "after" : newobs}, datafile)

def main():
    global all_URL_deque
    env = ScriptBrowserEnv(
        headless=True,                             
        observation_type="accessibility_tree",
        current_viewport_only=True,
        viewport_size={"width": 1800, "height": 1920},
    )
    """Input the URL to the homepage on the website"""
    all_URL_deque.append("http://localhost:7770/")
    all_URL_set.add("http://localhost:7770/")

    log_file = open("log_file_temporary.txt", 'a')

    while all_URL_deque:
        curr_url = all_URL_deque.popleft()
        print(curr_url)
        explore_url(curr_url, env)
        url_file = open("all_explored_url.txt", 'a')
        url_file.write(curr_url)
        url_file.close()

if __name__=="__main__":
    main()
