import json
import openai
from Tools.Tools import *

def load_config(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {json_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file {json_path}: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error loading config file {json_path}: {str(e)}")

Tools_list = load_config('./Tools/Tools_Config.json')

Todo_List_tools = [Tools_list["Make Todo.md"]]

Tools = []
for tool in Tools_list:
    if (tool != "Make Todo.md"):
        Tools.append(Tools_list[tool])

tools_mapping = {
    'Make Todo.md': Make_Todo_File,
    'Write File': Write_File,
    'Append File': Append_File,
    'Read File': Read_File,
    'Run Command': Run_Command
}
   

config = load_config("./Config/config.json")

Main_Model = openai.OpenAI(
    api_key=config["Main_Model"]["api_key"],
    base_url=config["Main_Model"]["base_url"]
)
Helper_Model = openai.OpenAI(
    api_key=config["Helper_Model"]["api_key"],
    base_url=config["Helper_Model"]["base_url"]
)
Main_Model_Name = config["Main_Model"]["Model_Name"]
Helper_Model_Name = config["Helper_Model"]["Model_Name"]