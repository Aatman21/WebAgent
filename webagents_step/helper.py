import json

def count_leading_tabs(s: str):
    count = 0
    for char in s:
        if char == "\t":
            count += 1
        else:
            return count
    return count

import re

def strip_id(input_str):
    match = re.match(r"\[\d+\]\s*(.*)", input_str)
    if match:
        return match.group(1)
    return input_str

def call(idx: int, content_: list):
    content=content_[0:idx+1]
    # print(content)
    num_tabs_current=count_leading_tabs(content[idx])
    before_idx=idx-1
    while before_idx>=3:
        before_person=content[before_idx]
        num_tabs_before=count_leading_tabs(before_person)
        if num_tabs_current>num_tabs_before:
            return call(before_idx, content)+"||--||"+strip_id(content[idx].strip())
        before_idx=before_idx-1
    return strip_id(content[idx].strip())

import json
"""Paste the Diffs json file with format as key:diff
Example:
"menubar '' orientation: horizontal||--||generic '\\ue609 MARKETING Marketing \\ue62f Promotions Catalog Price Rule Cart Price Rules Communications Email Templates Newsletter Templates Newsletter Queue Newsletter Subscribers SEO & Search URL Rewrites Search Terms Search Synonyms Site Map User Content All Reviews Pending Reviews'||--||link '\\ue62f'": "It looks like the information provided is related to the structure of a web page, specifically the elements and their attributes. It seems to be a comparison of the web page structure before and after a specific action or event, possibly related to an admin panel in a Magento e-commerce platform.\n\nThe provided information includes details about various elements such as links, buttons, static texts, tablists, tabpanels, tables, and more, along with their attributes and properties.\n\nIf you have any specific questions or need assistance with understanding or interpreting this information, please feel free to ask!"
"""
jsonFile = open("./final_json_desc_dataset_new.json", 'r')
database_dict = json.load(jsonFile)


def modify_observation(observation: str):
    content=observation.strip().split('\n')
    for idx, row_ in enumerate(content):
        row=row_.strip().split(" ")
        if len(row)>1 and row[1]=='link':
            key_to_check=call(idx, content)
            if key_to_check in database_dict:
                enriched_row=row_+"\t[The functionality that this link serves is: "+database_dict[key_to_check]+"]"
                content[idx]=enriched_row
    return "\n".join(content)
