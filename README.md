# Project Setup and Evaluation Guide

This guide outlines the steps to set up the WebArena environment, generate specific tasks, store login states, generate datasets, create diffs, and evaluate your model.

## 1. Setting Up the WebArena Environment

1. Follow the setup instructions provided in the [WebArena Docker repository](https://github.com/web-arena-x/webarena/blob/main/environment_docker/README.md#environment-reset).
2. Download the `.tar` image and run the given commands in your command line interface to set up the environment.

## 2. Generating Website-Specific Tasks

1. After setting up the website, navigate to `WebArena/webarena/scripts/generate_test_data.py`.
2. Follow the comments within the script to generate tasks specific to your website.
3. The tasks will be saved in the `WebArena/webarena/config_files` folder.

## 3. Storing the Login State

1. Before running the evaluation script, log in to the website and store the current state post-login.
2. Use the script located at `webagents-step/scripts/setup/auto_login_webarena.py`.
3. This will create a folder named `.auth` containing a `.json` file with the stored login state, which will be used by each task.

## 4. Configuring the Root Agent

1. Open `webagents-step/configs/webarena/eval_openai_agent.yml`.
2. Change the root agent to correspond to your website. This configuration enables the model to use all prompts defined under this root agent.

## 5. Generating the Dataset

1. Navigate to `dataset_creation/finalexploration.py`.
2. Follow the comments within the script to generate `.json` files. These files will contain:
   - The complete name of the clicked link
   - The accessibility tree before the link was clicked
   - The accessibility tree after the link was clicked

## 6. Generating Diffs Using the OpenAI API

1. Use the script located at `/Users/aatmanj/Desktop/Enriched_Tree/diffs_creation/script_for_diffs.py`.
2. This script will generate a JSON file with:
   - The key as the complete link name
   - The value as the natural language description of the differences between the two accessibility trees

## 7. Integrating Diffs into the Helper Script

1. Navigate to `/Users/aatmanj/Desktop/Enriched_Tree/webagents-step/helper.py`.
2. Paste the JSON file containing the diffs corresponding to your website into this script.

## 8. Evaluating the Model

1. Run the evaluation script located at `/Users/aatmanj/Desktop/Enriched_Tree/webagents-step/scripts/evaluate/eval_webarena.py` to evaluate your model.# Enriched_model
