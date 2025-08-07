from init import *
from prompts import *

def create_response(Message, Client, Model_Name ,tool_choice, Tool_Config):
    response = Client.chat.completions.create(
        model=Model_Name,
        messages=Message,
        temperature=0.7,
        tools=Tool_Config,
        tool_choice=tool_choice,
        stream=True
    )
    for chunk in response:
        if hasattr(chunk, "choices") and chunk.choices:
            choice = chunk.choices[0]
            if hasattr(choice, "delta") and hasattr(choice.delta, "tool_calls") and choice.delta.tool_calls:
                for tool_call in choice.delta.tool_calls:
                    print(f"Tool call: {tool_call}")

            if hasattr(choice, "delta") and hasattr(choice.delta, "content") and choice.delta.content:
                print(choice.delta.content, end="", flush=True)
    

make_prompts(Message)

Message.append({'role':'user','content':'你喜欢撸管吗？'})

create_response(Message,Main_Client,Main_Model_Name,"none",Tool_Config)

