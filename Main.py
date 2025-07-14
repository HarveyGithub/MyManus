import json
import os
from Load_config import Todo_List_tools, Tools, tools_mapping, Main_Model, Helper_Model, Main_Model_Name, Helper_Model_Name
# os.environ["http_proxy"] = "http://127.0.0.1:11434"
# os.environ["https_proxy"] = "http://127.0.0.1:11434"
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

def tackle_tool_calls(assistant_tool_calls):
    will_continue = True
    
    if assistant_tool_calls:
        print(f'Manus called {len(assistant_tool_calls)} tools:')
        for tool in assistant_tool_calls:
            if tool.function.name == "Finish Task":
                will_continue = False
            if tool_to_call := tools_mapping.get(tool.function.name):
                print('|- Calling tool: ', tool.function.name)
                print('|  With arguments: ', tool.function.arguments)
                arguments_dict = json.loads(tool.function.arguments)
                output = tool_to_call(**arguments_dict)
                print('|  Tool returned: ', output)
                messages.append({'role': 'tool', 'content': output})
            else:
                print('|-  This tool not found: ', tool.function.name)
    else:
        print('Manus didn\'t call any tools.')
    
    return will_continue

system_prompt = """
你是一个人工智能助手，负责帮助用户完成任务。
你的工作分为两个阶段：
第一阶段：任务分解
  1. 当收到用户的任务时，你首先需要为它制定解决方案。
  2. 将任务分解成若干个子任务，并确保子任务之间的先后顺序。
  3. 生成一个名为Todo.md的Markdown文件，文件内容必须包含以下要点：
      - 任务分解的完整结构。
      - 每个子任务必须有明确的执行步骤（即每一步要做什么，包括调用什么工具以及调用的参数）。
  4. 注意：必须调用'Make Todo.md'工具来生成这个文件，这是强制性的，不可跳过。
第二阶段：任务执行
  1. 在生成Todo.md之后，你需要自动按照文件中的顺序执行每一个子任务。
  2. 对于每个子任务，根据步骤描述调用相应的工具（只能使用预定义的工具）。
  3. 如果某个子任务需要多个步骤（例如先调用工具A，再调用工具B），则按步骤执行。
  4. 你只能使用预定义工具，不能使用也无法使用像vscode之类的桌面工具。
  5. 在执行过程中，将每个工具调用的结果记录下来，并作为下一步的上下文。
  6. 当所有子任务执行完毕后，向用户报告最终结果。
注意：
  - 在任务分解阶段，你只能使用'Make Todo.md'工具。
  - 在任务执行阶段，你可以使用所有预定义的工具（除了'Make Todo.md'）。
  - 请把工具调用请求写入tool_calls字段，而并不是content字段。
  - 如果某个子任务不需要调用工具（例如只需要生成一段文本），那么你可以直接生成文本，然后继续下一个子任务。
  - 在任务执行阶段，如果遇到错误（例如工具调用失败），你应该暂停并通知用户，等待用户的指示，或者尝试修复（如果有备用方案）。
"""
# 这是每个工具的具体调用功能和需要的参数（用json格式表示）：
messages.append({
    'role': 'system',
    'content': system_prompt
})

# user_task = input('请输入任务:')
# user_task = "编写一个python的贪吃蛇游戏"
user_task = "请创建一个python文件，使它能够实现“Hello,world”"

messages.append({'role': 'user', 'content': user_task})

response = Main_Model.chat.completions.create(
    messages=messages,
    model=Main_Model_Name,
    tools=Todo_List_tools,
    tool_choice="required",
    temperature=0.3,
    top_p=0.9,
    stream=True
)

# 编写一个python的贪吃蛇游戏

assistant_content, assistant_tool_calls = print_model_response(response)

messages.append({'role': 'assistant', 'content': assistant_content, 'tool_calls': assistant_tool_calls})

tackle_tool_calls(assistant_tool_calls)

messages.append({'role': 'system', 'content': '你现在进入了第二阶段，请按照Todo.md的步骤开始执行任务，可以调用相关工具'})

while True:
    response = Main_Model.chat.completions.create(
        messages=messages,
        model=Main_Model_Name,
        tools=Tools,
        tool_choice='auto',
        temperature=0.3,
        top_p=0.7,
        stream=True
    )
    # print(messages)
    assistant_content, assistant_tool_calls = print_model_response(response)
    messages.append({'role': 'assistant', 'content': assistant_content, 'tool_calls': assistant_tool_calls})
    if not tackle_tool_calls(assistant_tool_calls):
        break