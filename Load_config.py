import json
import openai
from Tools.Tools import Run_Linux_Terminal_Command, Make_Todo_File, Read_File, Write_File, Append_File

def load_config(json_path):
    data = ''
    with open(json_path, 'r') as f:
        data = f.read()
    data = data.replace('\n', '')
    return json.loads(data)

Tools_list = load_config('./Tools/Tools_Config.json')

Todo_List_tools = [Tools_list["Make Todo.md"]]

Tools = []
for tool in Tools_list:
    if (tool != "Make Todo.md"):
        Tools.append(Tools_list[tool])

tools_mapping = {
    'Run Linux Terminal Command': Run_Linux_Terminal_Command,
    'Make Todo.md': Make_Todo_File,
    'Write File': Write_File,
    'Append File': Append_File,
    'Read File': Read_File
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