import json
from Tools_Config import Todo_List_tools, Tools, tools_mapping
from Load_Models_Data import Main_Model, Helper_Model, Main_Model_Name, Helper_Model_Name

def print_model_response(response):
    print('Manus:')
    assistant_content = ''
    assistant_tool_calls = []

    for word in response:
        print(word.choices[0].delta.content, end='', flush=True)
        if word.choices[0].delta.content:
            assistant_content += word.choices[0].delta.content
        if word.choices[0].delta.tool_calls:
            assistant_tool_calls.extend(word.choices[0].delta.tool_calls)
            
    print('\n', end='')
    
    return assistant_content, assistant_tool_calls

messages = []
messages.append({
    'role': 'system',
    'content':
# """
# 你是一个全能的AI助手，你需要帮助用户解决问题或完成任务。
# 在解决问题或完成任务时，你可以调用工具来帮助你解决问题或完成任务。

# """
"""
你是一个专门负责规划任务的AI助手，
当收到user的任务时，你只需要为它制定解决方案，并生成名为Todo.md的Markdown文件来列出任务清单，将任务分解成若干个子任务，格式要十分清晰，请注意子任务们的先后顺序。
"""
})

user_task = input('请输入任务:')

messages.append({'role': 'user', 'content': user_task})

# messages.append({'role': 'user', 'content': }) # ，任务清单可能要包含检查等操作 '请你为：\'' + user_task + '\'任务制定解决方案，并生成名为Todo.md的Markdown文件来列出任务清单，将任务分解成若干个子任务，格式要十分清晰，请注意子任务们的先后顺序。'

response = Main_Model.chat.completions.create(
    messages=messages,
    model=Main_Model_Name,
    tools=Todo_List_tools,
    tool_choice='required',
    temperature=0.5,
    top_p=0.9,
    stream=True
)

# 编写一个python的贪吃蛇游戏


assistant_content, assistant_tool_calls = print_model_response(response)

# messages.append({'role': 'assistant', 'content': assistant_content + '\n\n\n' + assistant_tool_calls})

if assistant_tool_calls:
    print(f'Manus called {len(assistant_tool_calls)} tools:')
    for tool in assistant_tool_calls:
        if tool_to_call := tools_mapping.get(tool.function.name):
            print('|- Calling tool: ', tool.function.name)
            arguments_dict = json.loads(tool.function.arguments)
            output = tool_to_call(**arguments_dict)
            print('|  The tool returned: ', output)
            messages.append({'role': 'tool', 'content': output})
        else:
            print('|-  This tool not found: ', tool.function.name)
else:
    print('Manus didn\'t call any tools.')

print('\n', end='')

