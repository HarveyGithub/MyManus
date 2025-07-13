import openai
import Load_config

config = Load_config.load_config("./Config/config.json")

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