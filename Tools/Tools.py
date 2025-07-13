import subprocess

def Run_Linux_Terminal_Command(Command):
    result = subprocess.run(
        'cd /home/noi/MyManus/WorkSpace/ && ' + Command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout

def Make_Todo_File(Tittle, TodoList):
    with open("/home/noi/MyManus/WorkSpace/Todo.md", "w") as f:
        f.write(f"# {Tittle}\n")
        f.write("\n")
        i = 0
        # print(TodoList)
        for SubileTodo in TodoList:
            f.write(f"## {SubileTodo}\n")
            f.write("\n")
            if type(TodoList[SubileTodo]) == str:
                f.write(f"- [ ] {TodoList[SubileTodo]}\n")
                f.write("\n")
            else:
                for todo in TodoList[SubileTodo]:
                    f.write(f"- [ ] {todo}\n")
                    f.write("\n")
    f.close()
    
    return "Todo.md file created successfully."

# def Read_File(FilePath):
#     content = ""
#     with open(FilePath, "r") as f:
#         content = f.read()
#     f.close()
#     return content