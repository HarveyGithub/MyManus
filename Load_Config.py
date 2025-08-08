# from Tools.Tools import *
from Tools.File_Operation import *
from Tools.Terminal import *
from openai import OpenAI
import json
import os

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

config = load_config('./Config/model_config.json')

Main_Client = OpenAI(
    api_key=config["Main_Model"]["api_key"],
    base_url=config["Main_Model"]["base_url"],
)

Main_Model_Name=config["Main_Model"]["Model_Name"]

Tools_Config = load_config('./Config/Tools_Config.json')

Tools_List = []
for tool in Tools_Config:
    Tools_List.append(Tools_Config[tool])

Tools_Mapping={
    "Read_File": Read_File,
    "Write_File": Write_File,
    "Edit_File": Edit_File,
    "Send_Command": Send_Command,
    "Send_Keys": Send_Keys,
    "Kill_Terminal": Kill_Terminal,
    "View_Terminal": View_Terminal
}