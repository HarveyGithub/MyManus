import subprocess

def Run_Linux_Terminal_Command(Command):
    result = subprocess.run(
        'cd ./WorkSpace/ && ' + Command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout

def Make_Todo_File(Tittle, TodoList):
    with open("./WorkSpace/Todo.md", "w") as f:
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

def Read_File(FilePath):
    try:
        with open("./WorkSpace/" + FilePath, "r") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return "Error: File not found"
    except Exception as e:
        return f"Error: {str(e)}"

def Write_File(FilePath, Content):
    try:
        with open("./WorkSpace/" + FilePath, "w") as f:
            f.write(Content)
        return "File written successfully"
    except Exception as e:
        return f"Error: {str(e)}"

def Append_File(FilePath, Content):
    try:
        with open("./WorkSpace/" + FilePath, "a") as f:
            f.write(Content)
        return "Content appended successfully"
    except Exception as e:
        return f"Error: {str(e)}"