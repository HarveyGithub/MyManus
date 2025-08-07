from Load_Config import *
from Load_Prompts import *

Message = []

def create_response(Message, Client, model, tools ,tool_choice="required", stream=True):
    response = Client.chat.completions.create(
        model=model,
        messages=Message,
        temperature=0.7,
        tools=tools,
        tool_choice=tool_choice,
        stream=stream
    )
    for chunk in response:
        if hasattr(chunk, "choices") and chunk.choices:
            choice = chunk.choices[0]
            if hasattr(choice, "delta") and hasattr(choice.delta, "tool_calls") and choice.delta.tool_calls:
                for tool_call in choice.delta.tool_calls:
                    print(f"Tool call: {tool_call}")

            if hasattr(choice, "delta") and hasattr(choice.delta, "content") and choice.delta.content:
                print(choice.delta.content, end="", flush=True)
    

load_prompts(Message)

Message.append({'role':'user','content':''})

create_response(
    Message=Message,
    Client=Main_Client,
    model=Main_Model_Name,
    tools=Tools_List,
    tool_choice="required",
)