import json
from Load_config import Todo_List_tools, Tools, tools_mapping, Main_Model, Helper_Model, Main_Model_Name, Helper_Model_Name
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
# 你是一个人工智能助手，
# 当收到user的任务时，
# 你首先需要为它制定解决方案，
# 并生成名为Todo.md的Markdown文件来列出任务清单，
# 将任务分解成若干个子任务，格式要十分清晰，请注意子任务们的先后顺序。
# 请注意：
# 1.必须调用'Make Todo.md'工具
# 2.工具调用是强制性的，不可跳过
# 3.必须生成标准的Markdown格式
# 4.包含完整的任务分解结构
# 5.每个子任务必须有明确的执行步骤
# 6.你只能使用预定义的工具，不可自行添加或修改工具功能。
# 制定完任务。要分点执行，用户会发给你对应的步骤，你必须按照步骤执行，并将执行结果反馈给用户。
# 必要时调用工具
# ""
"""
你是一个人工智能助手，负责帮助用户完成复杂的任务。
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
  4. 在执行过程中，将每个工具调用的结果记录下来，并作为下一步的上下文。
  5. 当所有子任务执行完毕后，向用户报告最终结果。
注意：
  - 在任务分解阶段，你只能使用'Make Todo.md'工具。
  - 在任务执行阶段，你可以使用所有预定义的工具（除了'Make Todo.md'）。
  - 如果某个子任务不需要调用工具（例如只需要生成一段文本），那么你可以直接生成文本，然后继续下一个子任务。
  - 在任务执行阶段，如果遇到错误（例如工具调用失败），你应该暂停并通知用户，等待用户的指示，或者尝试修复（如果有备用方案）。
"""
})

# What are you doing???

# user_task = input('请输入任务:')
user_task = "创建一个python文件，使它能够实现“Hello,world”"

messages.append({'role': 'user', 'content': user_task})

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

print(assistant_tool_calls)

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
# 新增功能模块
MAX_STEPS = 10  # 防无限循环
execution_history = []  # 追踪任务状态

def safe_tool_call(tool_name, arguments):
    """安全执行工具并处理异常"""
    try:
        if tool := tools_mapping.get(tool_name):
            return tool(**arguments)
        return f"错误：未注册的工具 {tool_name}"
    except Exception as e:
        return f"工具执行错误：{str(e)}"

# 重构任务执行循环
def execute_task_plan():
    step_count = 0
    while step_count < MAX_STEPS:
        response = Main_Model.chat.completions.create(
            messages=messages,
            model=Main_Model_Name,
            tools=Tools if step_count > 0 else Todo_List_tools,
            tool_choice="required" if step_count == 0 else "auto",
            temperature=0.3,  # 执行阶段降低随机性
            stream=False  # 非流式保证工具调用完整性
        )
        
        msg = response.choices[0].message
        messages.append({
            "role": "assistant",
            "content": msg.content,
            "tool_calls": msg.tool_calls
        })
        
        # 工具调用处理
        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                result = safe_tool_call(tool_name, args)
                
                execution_history.append({
                    "step": step_count,
                    "tool": tool_name,
                    "status": "SUCCESS" if "错误" not in result else "FAILED",
                    "output": result[:300]  # 截断长输出
                })
                
                messages.append({
                    "role": "tool",
                    "content": result,
                    "tool_call_id": tool_call.id
                })
        else:  # 最终输出
            if "[TASK_COMPLETE]" in msg.content:
                save_final_report(execution_history)
                return True
        
        step_count += 1
    return False  # 超时终止

# 初始化后调用
if __name__ == "__main__":
    # ... (初始化代码)
    success = execute_task_plan()
    print(f"任务{'完成' if success else '中断'}")