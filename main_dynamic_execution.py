import json
import os
import re
from Load_config import Todo_List_tools, Tools, tools_mapping, Main_Model, Helper_Model, Main_Model_Name, Helper_Model_Name

def print_model_response(response):
    print("Manus:")
    assistant_content = ""
    assistant_tool_calls = []

    for word in response:
        print(word.choices[0].delta.content, end="", flush=True)
        if word.choices[0].delta.content:
            assistant_content += word.choices[0].delta.content
        if word.choices[0].delta.tool_calls:
            assistant_tool_calls.extend(word.choices[0].delta.tool_calls)

    print("\n", end="")

    return assistant_content, assistant_tool_calls

def parse_todo_md(todo_content):
    tasks = []
    current_task = None
    current_step_list = None

    lines = todo_content.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("## "):
            if current_task:
                tasks.append(current_task)
            current_task = {"title": line[3:].strip(), "steps": []}
            current_step_list = current_task["steps"]
        elif line.startswith("- ") and current_step_list is not None:
            current_step_list.append(line[2:].strip())
        elif line.startswith("### "):
            # Handle sub-sections within a task if needed, for now treat as part of steps
            pass

    if current_task:
        tasks.append(current_task)
    return tasks

def execute_todo_task(todo_file_path, initial_messages):
    messages = list(initial_messages) # Create a mutable copy

    with open(todo_file_path, "r") as f:
        todo_content = f.read()

    tasks = parse_todo_md(todo_content)

    print(f"\nExecuting {len(tasks)} tasks from {todo_file_path}:")
    for i, task in enumerate(tasks):
        print(f"\n--- Task {i+1}: {task["title"]} ---")
        for step_index, step_description in enumerate(task["steps"]):
            print(f"  - Step {step_index+1}: {step_description}")

            # Re-prompt the model with the step description to get tool calls
            step_messages = list(messages) # Use current message history
            step_messages.append({"role": "user", "content": f"请执行以下步骤：{step_description}"})

            response = Main_Model.chat.completions.create(
                messages=step_messages,
                model=Main_Model_Name,
                tools=Tools, # Use the general Tools list for execution phase
                tool_choice="auto", # Allow model to decide whether to call a tool
                temperature=0.5,
                top_p=0.9,
                stream=True
            )

            assistant_content, assistant_tool_calls = print_model_response(response)

            if assistant_tool_calls:
                print(f"Manus called {len(assistant_tool_calls)} tools for this step:")
                for tool in assistant_tool_calls:
                    if tool_to_call := tools_mapping.get(tool.function.name):
                        print("|- Calling tool: ", tool.function.name)
                        arguments_dict = json.loads(tool.function.arguments)
                        try:
                            output = tool_to_call(**arguments_dict)
                            print("|  The tool returned: ", output)
                            messages.append({"role": "tool", "content": json.dumps(output)}) # Append tool output to messages
                        except Exception as e:
                            error_message = f"Tool execution failed: {e}"
                            print(f"|  Error: {error_message}")
                            messages.append({"role": "tool", "content": error_message}) # Append error to messages
                    else:
                        not_found_message = f"This tool not found: {tool.function.name}"
                        print(f"|-  {not_found_message}")
                        messages.append({"role": "tool", "content": not_found_message}) # Append not found to messages
            else:
                print("Manus didn\"t call any tools for this step.")
                if assistant_content:
                    messages.append({"role": "assistant", "content": assistant_content}) # Append assistant's response if no tool call

    return messages # Return the updated messages list


messages = []
messages.append({
    "role": "system",
    "content":
"""
你是一个人工智能助手，负责帮助用户完成复杂的任务。
你的工作分为两个阶段：
第一阶段：任务分解
  1. 当收到任务时，你首先需要为它制定解决方案。
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

user_task = "创建一个python文件，使它能够实现“Hello,world”"
messages.append({"role": "user", "content": user_task})

# Phase 1: Task Decomposition
print("\n--- Phase 1: Task Decomposition ---")
response = Main_Model.chat.completions.create(
    messages=messages,
    model=Main_Model_Name,
    tools=Todo_List_tools,
    tool_choice="required",
    temperature=0.5,
    top_p=0.9,
    stream=True
)

assistant_content, assistant_tool_calls = print_model_response(response)

if assistant_tool_calls:
    print(f"Manus called {len(assistant_tool_calls)} tools in Phase 1:")
    for tool in assistant_tool_calls:
        if tool_to_call := tools_mapping.get(tool.function.name):
            print("|- Calling tool: ", tool.function.name)
            arguments_dict = json.loads(tool.function.arguments)
            output = tool_to_call(**arguments_dict)
            print("|  The tool returned: ", output)
            messages.append({"role": "tool", "content": json.dumps(output)}) # Append tool output to messages
        else:
            print("|-  This tool not found: ", tool.function.name)
else:
    print("Manus didn\"t call any tools in Phase 1.")

# Assuming Todo.md is generated in Phase 1
todo_file_path = "Todo.md" # This should be the actual path where Make Todo.md saves the file

# Phase 2: Task Execution
print("\n--- Phase 2: Task Execution ---")
if os.path.exists(todo_file_path):
    final_messages = execute_todo_task(todo_file_path, messages)
    print("\n--- Task Execution Completed ---")
    print("\nFinal messages state (for debugging):")
    # print(final_messages) # Uncomment for full message history debugging
else:
    print(f"Error: {todo_file_path} not found. Cannot proceed with task execution.")

print("\n", end="")