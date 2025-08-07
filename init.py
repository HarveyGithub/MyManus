from Tools.Tools import *
from openai import OpenAI
import json
import os
with open('./model_config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

Main_Model = OpenAI(
        api_key=config["Main_Model"]["api_key"],
        base_url=config["Main_Model"]["base_url"],
        model=config["Main_Model"]["Model_Name"]
    )


with open('./Tools_Config.json', 'r', encoding='utf-8') as f:
    Tool_Config = json.load(f)

Tool_Mapping={
    "Run_Command": Run_Command,
    "Read_File": Read_File,
    "Write_File": Write_File,
    "Edit_File": Edit_File
}

Message = []

