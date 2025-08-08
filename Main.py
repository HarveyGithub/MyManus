from Load_Config import *
from Load_Prompts import *

Messages = []

Terminals = TerminalManager()

def create_response(Message, Client, model, tools = [] ,tool_choice="required", stream=True):
    # print(f'Assistant: {Message}')
    response = Client.chat.completions.create(
        model=model,
        messages=Message,
        temperature=0.7,
        tools=tools,
        tool_choice=tool_choice,
        stream=stream
    )
    Agent_Content = ''
    Agent_Tool_Calls = []
    for word in response:
        print(word.choices[0].delta.content, end='', flush=True)
        if word.choices[0].delta.content:
            Agent_Content += word.choices[0].delta.content
        if word.choices[0].delta.tool_calls:
            Agent_Tool_Calls.extend(word.choices[0].delta.tool_calls)
    
    return Agent_Content, Agent_Tool_Calls

def tackle_tool_calls(assistant_tool_calls):
    if assistant_tool_calls:
        
        print(f'Manus called {len(assistant_tool_calls)} tools:')
        
        for tool in assistant_tool_calls:
            tool.function.name=tool.function.name.strip()
            if tool.function.name == "Task_Finish":
                print("|- Task finished.")
                return False

            if tool_to_call := Tools_Mapping.get(tool.function.name):
                print('|- Calling tool:', tool.function.name, flush=True)
                print('|  With arguments:', tool.function.arguments, flush=True)
                
                arguments_dict = json.loads(tool.function.arguments)
                
                if tool.function.name == "Send_Command" or tool.function.name == "View_Terminal":
                    output = tool_to_call(**arguments_dict, manager = Terminals)
                else:
                    output = tool_to_call(**arguments_dict)
                
                print('|  Tool returned:', output)
                Messages.append({'role': 'tool', 'content': output})

            else:
                print('|-  This tool not found:\"', tool.function.name,"\"")
    else:
        print('Manus didn\'t call any tools.')
    
    return True
    
load_prompts(Messages)
Messages.append({'role':'user','content':'请用python在写一个输出helloworld的程序，并测试。'})
# Messages.append({'role':'user', 'content':'您在一个任务循环中运行，通过哪些步骤迭代完成任务？'})
# print(Tools_List)

while True:

    Agent_Content, Agent_Tool_Calls = create_response(
        Message=Messages,
        Client=Main_Client,
        model=Main_Model_Name,
        tools=Tools_List,
        tool_choice="auto",
        stream=True
    )
    
    if not tackle_tool_calls(Agent_Tool_Calls):
        break