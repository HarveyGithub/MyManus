import os

def Make_Todo_File(Tittle, TodoList):
    with open("/home/noi/MyManus/WorkSpace/Todo.md", "w") as f:
        f.write(f"# {Tittle}\n")
        f.write("\n")
        f.write("---\n")
        f.write("\n")
        i = 0
        for todo in TodoList:
            if todo:
                f.write(f"[ ] {i + 1}.{todo}\n\n")
                i+=1