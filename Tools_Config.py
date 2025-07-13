from Tools.Terminal import Run_Linux_Terminal_Command
from Tools.TodoFIle import Make_Todo_File

Todo_List_tools = [
    {
        "type": "function",
        "function": {
            "name": "Make Todo.md",
            "description": "创建Todo.md文件，并向里面写入任务清单",
            "parameters": {
                "type": "object",
                "properties": {
                    "Tittle": {
                        "type": "string",
                        "description": "Todo的标题"
                    },
                    "TodoList": {
                        "type": "map",
                        "description": "TodoList参数：必须为字典格式，包含：键：子任务序号+标题(如\"1. 需求分析\") 值：子任务详细步骤(换行分隔的字符串)"
                    }
                },
                "required": ["Tittle", "TodoList"]
            }
        }
    }
]

Tools = [
    {
        "type": "function",
        "function": {
            "name": "Run Linux Terminal Command",
            "description": "执行Linux终端命令，注意不要访问/home/noi/MyManus/WorkSpace/目录外的任何文件或目录，你无法调出显示类的窗口，默认在/home/noi/MyManus/WorkSpace/目录下执行，已经安装的python的包名为python3，python的版本为3.8.10",
            "parameters": {
                "type": "object",
                "properties": {
                    "Command": {
                        "type": "string",
                        "description": "要执行的Linux终端命令"
                    }
                },
                "required": ["Command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "Make Todo.md",
            "description": "创建Todo.md文件，并向里面写入任务清单",
            "parameters": {
                "type": "object",
                "properties": {
                    "Tittle": {
                        "type": "string",
                        "description": "Todo的标题"
                    },
                    "TodoList": {
                        "type": "list",
                        "description": "要写入的任务清单"
                    }
                },
                "required": ["Tittle", "TodoList"]
            }
        }
    }
]

tools_mapping = {
    'Run Linux Terminal Command': Run_Linux_Terminal_Command,
    'Make Todo.md': Make_Todo_File
}