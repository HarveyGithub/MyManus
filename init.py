from Tools.Tools import *
from openai import OpenAI
import json
import os
with open('./Config/model_config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

Main_Client = OpenAI(
        api_key=config["Main_Model"]["api_key"],
        base_url=config["Main_Model"]["base_url"],
    )

Main_Model_Name=config["Main_Model"]["Model_Name"]

with open('./Config/Tools_Config.json', 'r', encoding='utf-8') as f:
    Tool_Config = json.load(f)

Tool_Mapping={
    "Run_Command": Run_Command,
    "Read_File": Read_File,
    "Write_File": Write_File,
    "Edit_File": Edit_File
}

Message = []

